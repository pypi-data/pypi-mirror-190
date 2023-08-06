from datetime import datetime, timedelta
import itertools
import json
import math
import re
from multiprocessing.sharedctypes import Value
import time
from abc import ABCMeta, abstractmethod
from collections.abc import MutableMapping
from typing import Any, Callable, Dict, Iterable, Iterator, KeysView, List, Tuple

import numpy as np
import pandas as pd
import pyproj
from numcodecs import Blosc

from .config import CubeConfig
from .ddc import DanubeDataCube
from .constants import DDC_MAX_CHUNK_SIZE


_STATIC_ARRAY_COMPRESSOR_PARAMS = dict(
    cname='zstd',
    clevel=1,
    shuffle=Blosc.SHUFFLE,
    blocksize=0
)

_STATIC_ARRAY_COMPRESSOR_CONFIG = dict(
    id='blosc',
    **_STATIC_ARRAY_COMPRESSOR_PARAMS
)

_REMOTE_ARRAY_COMPRESSOR_PARAMS = dict(
    cname='lz4',
    clevel=5,
    shuffle=Blosc.SHUFFLE,
    blocksize=0
)

_REMOTE_ARRAY_COMPRESSOR_CONFIG = dict(
    id='blosc',
    **_REMOTE_ARRAY_COMPRESSOR_PARAMS
)

_STATIC_ARRAY_COMPRESSOR = Blosc(**_STATIC_ARRAY_COMPRESSOR_PARAMS)


def _dict_to_bytes(d: Dict) -> bytes:
    return _str_to_bytes(json.dumps(d, indent=2))


def _bytes_to_dict(b: bytes) -> Dict:
    return json.loads(_bytes_to_str(b))


def _str_to_bytes(s: str):
    return bytes(s, encoding='utf-8')


def _bytes_to_str(b: bytes) -> str:
    return b.decode('utf-8')


# MutableMapping, metaclass=ABCMeta):
class RemoteStore(MutableMapping, metaclass=ABCMeta):
    """
    A remote Zarr Store.
    :param cube_config: Cube configuration.
    :param observer: An optional callback function called when remote
        requests are mode: observer(**kwargs).
    :param trace_store_calls: Whether store calls shall be
        printed (for debugging).
    """

    _SAMPLE_TYPE_TO_DTYPE = {
        'uint8': '|u1',
        'uint16': '<u2',
        'uint32': '<u4',
        'int8': '|u1',
        'int16': '<u2',
        'int32': '<u4',
        'float32': '<f4',
        'float64': '<f8',
    }

    def __init__(self,
                 cube_config: CubeConfig):

        self._cube_config = cube_config
        # self._dataset_config = dataset_config
        self._time_ranges = self.get_time_ranges()
        self._bbox = self._cube_config.bbox.bbox

        if not self._time_ranges:
            raise ValueError('Could not determine any valid time stamps.')

        spatial_res = self._cube_config.spatial_res
        depth, width, height = self._cube_config.size
        x1, y1, x2, y2 = self._bbox
        chunk_depth, chunk_width, chunk_height = self._cube_config.chunk_size

        x_array = np.linspace(x1, x2, width, dtype=np.float64)
        y_array = np.linspace(y2, y1, height, dtype=np.float64)
        crs = pyproj.CRS.from_string(self._cube_config.crs)

        def time_stamp_to_str(ts: pd.Timestamp) -> str:
            """
            Convert to ISO string and strip timezone.
            Used to create numpy datetime64 arrays.
            We cannot create directly from pd.Timestamp because Numpy doesn't
            like parsing timezones anymore.
            """
            ts_str: str = ts.isoformat()
            if ts_str[-1] == 'Z':
                return ts_str[0:-1]
            try:
                i = ts_str.rindex('+')
                return ts_str[0: i]
            except ValueError:
                return ts_str

        t_array = np.array([time_stamp_to_str(ts)
                            for ts in self._time_ranges],
                           dtype='datetime64[s]').astype(np.int64)
        # t_bnds_array = np.array([[time_stamp_to_str(ts), time_stamp_to_str(ts)]
        # for ts in self._time_ranges],
        # dtype='datetime64[s]').astype(np.int64)

        self._size = depth, height, width
        self._chunk_size = chunk_depth, chunk_height, chunk_width

        time_coverage_start = self._cube_config.time_range.start_time
        time_coverage_end = self._cube_config.time_range.end_time

        global_attrs = dict(
            Conventions='CF-1.7',
            # coordinates='time_bnds',
            title=f'{self._cube_config.dataset_name} Data Cube Subset',
            history=[
                dict(
                    program=f'{self._class_name}',
                    cube_config=self._cube_config.to_dict(),
                )
            ],
            date_created=pd.Timestamp.now().isoformat(),
            time_coverage_start=time_coverage_start.isoformat(),
            time_coverage_end=time_coverage_end.isoformat(),
            time_coverage_duration=(
                time_coverage_end - time_coverage_start
            ).isoformat(),
        )

        if crs.is_geographic:
            x1, y1, x2, y2 = self._bbox
            global_attrs.update(geospatial_lon_min=x1,
                                geospatial_lat_min=y1,
                                geospatial_lon_max=x2,
                                geospatial_lat_max=y2)
        else:
            x1, y1, x2, y2 = self._bbox
            global_attrs.update(projected_x_min=x1,
                                projected_y_min=y1,
                                projected_x_max=x2,
                                projected_y_max=y2)

        # setup Virtual File System (vfs)
        self._vfs = {
            '.zgroup': _dict_to_bytes(dict(zarr_format=2)),
            '.zattrs': _dict_to_bytes(global_attrs)
        }

        if crs.is_geographic:
            x_name, y_name = 'lon', 'lat'
            x_attrs, y_attrs = (
                {
                    "_ARRAY_DIMENSIONS": ['lon'],
                    "units": "decimal_degrees",
                    "long_name": "longitude",
                    "standard_name": "longitude",
                },
                {
                    "_ARRAY_DIMENSIONS": ['lat'],
                    "units": "decimal_degrees",
                    "long_name": "latitude",
                    "standard_name": "latitude",
                }
            )
        else:
            x_name, y_name = 'x', 'y'
            x_attrs, y_attrs = (
                {
                    "_ARRAY_DIMENSIONS": ['x'],
                    "long_name": "x coordinate of projection",
                    "standard_name": "projection_x_coordinate",
                },
                {
                    "_ARRAY_DIMENSIONS": ['y'],
                    "long_name": "y coordinate of projection",
                    "standard_name": "projection_y_coordinate",
                }
            )

        time_attrs = {
            "_ARRAY_DIMENSIONS": ['time'],
            "units": "seconds since 1970-01-01T00:00:00Z",
            "calendar": "proleptic_gregorian",
            "standard_name": "time",
            # "bounds": "time_bnds",
        }
        # time_bnds_attrs = {
        # "_ARRAY_DIMENSIONS": ['time', 'bnds'],
        # "units": "seconds since 1970-01-01T00:00:00Z",
        # "calendar": "proleptic_gregorian",
        # "standard_name": "time",
        # }

        self._add_static_array(x_name, x_array, x_attrs)
        self._add_static_array(y_name, y_array, y_attrs)
        self._add_static_array('time', t_array, time_attrs)
        # self._add_static_array('time_bnds', t_bnds_array, time_bnds_attrs)

        crs_var_attrs = dict()
        # if not crs.is_geographic:
        self._add_static_array('crs', np.array(0), dict(
            _ARRAY_DIMENSIONS=[],
            **crs.to_cf(),
        ))
        crs_var_attrs['grid_mapping'] = 'crs'

        if crs.is_geographic:
            band_array_dimensions = ['time', 'lat', 'lon']
        else:
            band_array_dimensions = ['time', 'y', 'x']

        for var_name in self._cube_config.variable_names:

            var_encoding = self.get_band_encoding(var_name)
            var_attrs = self.get_var_attrs(var_name)
            var_attrs.update(_ARRAY_DIMENSIONS=band_array_dimensions)
            self._add_remote_array(var_name,
                                   [*self._size],
                                   [*self._chunk_size],
                                   var_encoding,
                                   {**var_attrs, **crs_var_attrs})

        self._consolidate_metadata()

    @abstractmethod
    def get_var_attrs(self, var_name: str) -> Dict[str, Any]:
        """
        Get any metadata attributes for variable var_name.
        """
        pass

    @abstractmethod
    def _fetch_chunk(self,
                     key: str,
                     band_name: str,
                     chunk_index: Tuple[int, ...]) -> bytes:
        """
        Fetch chunk data from remote.
        :param key: The original chunk key being retrieved.
        :param band_name: Band name.
        :param chunk_index: Chunk indexes being retrieved in zarr terminology.
        """
        pass

    def _add_static_array(self, name: str, array: np.ndarray, attrs: Dict):
        shape = list(map(int, array.shape))
        dtype = str(array.dtype.str)
        order = "C"
        array_metadata = {
            "zarr_format": 2,
            "chunks": shape,
            "shape": shape,
            "dtype": dtype,
            "fill_value": None,
            "compressor": _STATIC_ARRAY_COMPRESSOR_CONFIG,
            "filters": None,
            "order": order,
        }
        chunk_key = '.'.join(['0'] * array.ndim)
        self._vfs[name] = _str_to_bytes('')
        self._vfs[name + '/.zarray'] = _dict_to_bytes(array_metadata)
        self._vfs[name + '/.zattrs'] = _dict_to_bytes(attrs)
        self._vfs[name + '/' +
                  chunk_key] = _STATIC_ARRAY_COMPRESSOR.encode(array.tobytes(order=order))

    def _add_remote_array(self,
                          name: str,
                          shape: List[int],
                          chunks: List[int],
                          encoding: Dict[str, Any],
                          attrs: Dict):
        array_metadata = dict(zarr_format=2,
                              shape=shape,
                              chunks=chunks,
                              compressor=None,
                              fill_value=None,
                              filters=None,
                              order='C')
        array_metadata.update(encoding)
        self._vfs[name] = _str_to_bytes('')
        self._vfs[name + '/.zarray'] = _dict_to_bytes(array_metadata)
        self._vfs[name + '/.zattrs'] = _dict_to_bytes(attrs)
        nums = - (np.array(shape) // - np.array(chunks))
        indexes = itertools.product(*tuple(map(range, map(int, nums))))
        for index in indexes:
            filename = '.'.join(map(str, index))
            # noinspection PyTypeChecker
            self._vfs[name + '/' + filename] = name, index

    def get_time_ranges(self):
        time_start, time_end = self._cube_config.time_range.time_range
        time_period = self._cube_config.time_period

        time_ranges = pd.date_range(time_start, time_end,
                                    freq=time_period, normalize=True,
                                    inclusive='both', tz='UTC')
        time_ranges.freq = None

        return time_ranges.to_list()

    def get_band_encoding(self, var_name: str) -> Dict[str, Any]:

        if isinstance(self._cube_config.datatype, dict):
            sample_type = self._cube_config.datatype.get(var_name)
        else:
            sample_type = 'float32'

        # Convert to sample type name to Zarr dtype value
        dtype = self._SAMPLE_TYPE_TO_DTYPE.get(str(sample_type))
        if dtype is None:
            raise TypeError(f'Invalid sample type {sample_type!r},'
                            f' must be one of'
                            f' {tuple(self._SAMPLE_TYPE_TO_DTYPE.keys())}.')

        fill_value = None

        return dict(dtype=dtype,
                    fill_value=fill_value,
                    compressor=_REMOTE_ARRAY_COMPRESSOR_CONFIG,
                    order='C')

    def _consolidate_metadata(self):
        # Consolidate metadata to suppress warning:  (#69)
        #
        # RuntimeWarning: Failed to open Zarr store with consolidated
        # metadata, falling back to try reading non-consolidated
        # metadata. ...
        #
        metadata = dict()
        for k, v in self._vfs.items():
            if k == '.zattrs' or k.endswith('/.zattrs') \
                    or k == '.zarray' or k.endswith('/.zarray') \
                    or k == '.zgroup' or k.endswith('/.zgroup'):
                metadata[k] = _bytes_to_dict(v)
        self._vfs['.zmetadata'] = _dict_to_bytes(
            dict(zarr_consolidated_format=1, metadata=metadata)
        )

    @property
    def cube_config(self) -> CubeConfig:
        return self._cube_config

    @property
    def _class_name(self):
        return self.__module__ + '.' + self.__class__.__name__

    def __iter__(self) -> Iterator[str]:
        return iter(self._vfs.keys())

    def __len__(self) -> int:
        return len(self._vfs.keys())

    def __contains__(self, key) -> bool:
        return key in self._vfs

    def __getitem__(self, key: str) -> bytes:
        value = self._vfs[key]
        if isinstance(value, tuple):
            return self._fetch_chunk(key, *value)
        return value

    def __setitem__(self, key: str, value: bytes) -> None:
        raise TypeError(f'{self._class_name} is read-only')

    def __delitem__(self, key: str) -> None:
        raise TypeError(f'{self._class_name} is read-only')


class DanubeDataCubeChunkStore(RemoteStore):  # RemoteStore):
    """
    A remote Zarr Store using DanubeDataCube portal as backend for DDC datasets.
    """

    def __init__(self,
                 danube_data_cube: DanubeDataCube,
                 cube_config: CubeConfig):

        self._danube_data_cube = danube_data_cube
        super().__init__(cube_config)

    def get_var_attrs(self, var_name: str) -> Dict[str, Any]:
        band_metadata = self._danube_data_cube.dataset_var(
            self._cube_config.dataset_name,
            var_name,
            default={}
        )
        if 'fill_value' in band_metadata:
            band_metadata.pop('fill_value')
        return band_metadata

    def request_bbox(self,
                     x_chunk_index: int,
                     y_chunk_index: int) -> Tuple[float, float, float, float]:

        _, y_chunk_size, x_chunk_size, = self._chunk_size

        x_index = x_chunk_index * x_chunk_size
        y_index = y_chunk_index * y_chunk_size

        x01, _, _, y02 = self._bbox
        spatial_res = self._cube_config.spatial_res
        precision = self._cube_config.bbox._precision

        x1 = x01 + spatial_res * x_index
        x2 = x01 + spatial_res * (x_index + x_chunk_size - 1)
        y1 = y02 - spatial_res * (y_index + y_chunk_size - 1)
        y2 = y02 - spatial_res * y_index

        return tuple(np.round(n, precision) for n in (x1, y1, x2, y2))

    def request_time_range(self, time_chunk_index: int) -> Tuple[pd.Timestamp,
                                                                 pd.Timestamp]:

        t_chunk_size, _, _ = self._chunk_size
        start_index = time_chunk_index * t_chunk_size
        end_index = time_chunk_index * t_chunk_size + t_chunk_size - 1
        end_index = end_index if end_index < len(
            self._time_ranges) else len(self._time_ranges) - 1

        start_time = self._time_ranges[start_index]
        end_time = self._time_ranges[end_index]
        num_dates = len(self._time_ranges[start_index:end_index+1])

        return start_time, end_time, num_dates

    def _fetch_chunk(self,
                     key: str,
                     band_name: str,
                     chunk_index: Tuple[int, ...]) -> bytes:

        time_chunk_index, y_chunk_index, x_chunk_index = chunk_index

        request_bbox = self.request_bbox(x_chunk_index, y_chunk_index)
        start_date, end_date, num_dates = self.request_time_range(
            time_chunk_index)
        request_time_range = start_date, end_date
        time_period = self._cube_config.time_period
        t0 = time.perf_counter()
        try:
            exception = None
            chunk_data = self.fetch_chunk(key,
                                          band_name,
                                          bbox=request_bbox,
                                          time_range=request_time_range,
                                          time_period=time_period)

            if num_dates < self._chunk_size[0]:

                extend_nan = np.empty(
                    ((self._chunk_size[0] - num_dates)*self._chunk_size[1]
                     * self._chunk_size[2]), dtype='float32')
                extend_nan[:] = np.nan
                extend_nan = extend_nan.tobytes(order='C')
                chunk_data_ed = Blosc(
                    **_REMOTE_ARRAY_COMPRESSOR_PARAMS).decode(buf=chunk_data)
                chunk_data_ed += extend_nan
                chunk_data = Blosc(
                    **_REMOTE_ARRAY_COMPRESSOR_PARAMS).encode(
                        buf=chunk_data_ed)

        except Exception as e:
            exception = e
            chunk_data = None

        duration = time.perf_counter() - t0

        if exception:
            raise exception

        return chunk_data

    def fetch_chunk(self,
                    key: str,
                    band_name: str,
                    bbox: Tuple[float, float, float, float],
                    time_range: Tuple[pd.Timestamp, pd.Timestamp],
                    time_period: str) -> bytes:

        url = self._danube_data_cube.binary_url
        dataset = self.cube_config.dataset_name.lower()
        bbox = ','.join(map(str, bbox))

        start_time, end_time = time_range
        start_time, end_time = (start_time.isoformat(sep='T').split('T')[0],
                                end_time.isoformat(sep='T').split('T')[0])

        if time_period == self.cube_config.dataset_default_properties.get(
                'time_period'):
            time_period = 'original'

        request = dict(
            dataset=dataset,
            variable=band_name,
            time_range_start=start_time,
            time_range_end=end_time,
            time_period=time_period,
            bbox=bbox
        )

        response = self._danube_data_cube.get_data(
            url, request, mime_type='application/octet'
        )

        if response is None or not response.ok:
            message = (f'{key}: cannot fetch chunk for variable'
                       f' {band_name!r}, bbox {bbox!r}, and'
                       f' time_range {time_range!r}')
            if response is not None:
                message += f': {ValueError(response)}'
            raise KeyError(message)
        return response.content


class CustomChunkStore(RemoteStore):
    """
    A remote Zarr Store using DanubeDataCube portal as backend for
    Custom datasets.
    """

    def __init__(self,
                 danube_data_cube: DanubeDataCube,
                 cube_config: CubeConfig):

        self._danube_data_cube = danube_data_cube
        super().__init__(cube_config)

    def get_var_attrs(self, var_name: str) -> Dict[str, Any]:
        band_metadata = {}
        return band_metadata

    def _fetch_chunk(self,
                     key: str,
                     band_name: str,
                     chunk_index: Tuple[int, ...]) -> bytes:

        time_chunk_index, y_chunk_index, x_chunk_index = chunk_index

        t0 = time.perf_counter()
        try:
            exception = None
            chunk_data = self.fetch_chunk(key,
                                          band_name)

        except Exception as e:
            exception = e
            chunk_data = None

        duration = time.perf_counter() - t0

        if exception:
            raise exception

        return chunk_data

    def fetch_chunk(self,
                    key: str,
                    band_name: str) -> bytes:

        url = self._danube_data_cube.custom_binary_url
        dataset = self.cube_config.dataset_name.lower()

        request = dict(
            dataset=dataset,
            variable=band_name
        )

        response = self._danube_data_cube.get_data(
            url, request, mime_type='application/octet'
        )

        if response is None or not response.ok:
            message = (f'{key}: cannot fetch chunk for '
                       f'variable {band_name!r}.')
            if response is not None:
                message += f': {ValueError(response)}'
            raise KeyError(message)
        return response.content
