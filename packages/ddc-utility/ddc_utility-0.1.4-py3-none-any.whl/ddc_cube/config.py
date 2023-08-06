from __future__ import annotations
import math
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from dask.array.core import auto_chunks

from .assertions import assert_true
from .constants import (CRS_ID_TO_URI, DDC_MAX_CHUNK_SIZE,
                        DEFAULT_BBOX, DEFAULT_CRS, TIME_PERIODS)
from .ddc import DanubeDataCube


class Bbox:
    """"Class for bounding box represented by four number.

    Args:
        minx (Union[str, int, float]): Minimum coordinate in x direction.
        miny (Union[str, int, float]): Minimum coordinate in y direction.
        maxx (Union[str, int, float]): Maximum coordinate in x direction.
        maxy (Union[str, int, float]): Maximum coordinate in y direction.
        precision (int): presion applied at rounding.
    """

    def __init__(self,
                 minx: Union[str, int, float],
                 miny: Union[str, int, float],
                 maxx: Union[str, int, float],
                 maxy: Union[str, int, float],
                 precision: Optional[int] = None):

        try:
            minx, miny, maxx, maxy = tuple(map(float, (minx, miny,
                                                       maxx, maxy)))
        except (TypeError, ValueError) as error:
            raise ValueError('Invalid input parameters, coordinates '
                             'must be convertable to float number.') from error

        self._precision = precision
        self._minx = np.round(minx, self._precision)
        self._miny = np.round(miny, self._precision)
        self._maxx = np.round(maxx, self._precision)
        self._maxy = np.round(maxy, self._precision)

    @property
    def bbox(self):
        "Returns the bounding box as a tuple."
        return (self._minx, self._miny, self._maxx, self._maxy)

    @property
    def minx(self):
        return self._minx

    @minx.setter
    def minx(self, value):
        self._minx = np.round(float(value), self._precision)

    @property
    def miny(self):
        return self._miny

    @miny.setter
    def miny(self, value):
        self._miny = np.round(float(value), self._precision)

    @property
    def maxx(self):
        return self._maxx

    @maxx.setter
    def maxx(self, value):
        self._maxx = np.round(float(value), self._precision)

    @property
    def maxy(self):
        return self._maxy

    @maxy.setter
    def maxy(self, value):
        self._maxy = np.round(float(value), self._precision)


class TimeRange:
    """"Class for time range represented by two dates.

    Args:
        start_time (Union[str, pd.Timestamp]): Start date.
        end_time (Union[str, pd.Timestamp]): End date.
    """

    def __init__(self, start_time, end_time):
        try:
            start_time, end_time = tuple(map(self.convert_time,
                                             (start_time, end_time)))
            if start_time > end_time:
                raise ValueError('start_time must be smaller or '
                                 'equal to end_time')

        except (TypeError, ValueError) as error:
            raise ValueError(
                'Invalid input parameters, times '
                'must be convertable to pandas.TimeStamp.') from error

        self._start_time = start_time
        self._end_time = end_time

    @property
    def time_range(self):
        return (self._start_time, self._end_time)

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        start_time = self.convert_time(value)
        if start_time <= self.end_time:
            self._start_time = start_time
        else:
            raise ValueError('start_time must be smaller or '
                             'equal to end_time')

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        end_time = self.convert_time(value)
        if end_time >= self.start_time:
            self._end_time = end_time
        else:
            raise ValueError('end_time must be greater or '
                             'equal to start_time')

    def get_time_range_str(self, only_date=True):
        if only_date:
            return (self.start_time.isoformat(sep='T').split('T')[0],
                    self.end_time.isoformat(sep='T').split('T')[0])
        else:
            return (self.start_time.isoformat(sep='T'),
                    self.end_time.isoformat(sep='T'))

    @classmethod
    def convert_time(cls, datetime, utc=True):
        try:
            return pd.to_datetime(datetime, utc=utc)
        except Exception as error:
            raise ValueError('Could not convert datetime: '
                             f'{datetime} to pandas.Timestamp.') from error


class CubeConfig(ABC):
    """
    Cube configuration interface for various data collections.
    """

    @abstractmethod
    def __init__(self,
                 dataset_name: str,
                 variable_names: Optional[List[str]], optional=None):

        self._dataset_name = dataset_name
        self._variable_names = variable_names

    def to_dict(self) -> Dict[str, Any]:
        """
        Return CubeConfig as dictionary.
        """
        time_range = self.time_range.get_time_range_str(False)
        bbox = self.bbox.bbox
        datatype = str(self.datatype)

        return dict(dataset_name=self.dataset_name,
                    variable_names=self.variable_names,
                    bbox=bbox,
                    spatial_res=self.spatial_res,
                    size=self.size,
                    chunk_size=self.chunk_size,
                    num_chunks=self.num_chunks,
                    crs=self.crs,
                    time_range=time_range,
                    time_period=self.time_period,
                    datatype=datatype)

    @property
    def dataset_name(self) -> str:
        return self._dataset_name

    @property
    def variable_names(self) -> List[str, ...]:
        return self._variable_names

    @abstractmethod
    def get_spatial_res(self):
        """Abstract method for retrieving spatial resolution of the dataset"""
        pass

    @abstractmethod
    def get_bbox(self):
        """Abstract method for retrieving bbox of the dataset"""
        pass

    @abstractmethod
    def get_size(self):
        """Abstract method for retrieving size of the dataset"""
        pass

    @abstractmethod
    def get_xy_chunk_size(self):
        """Abstract method for retrieving the chunk size  in x and y dimension"""
        pass

    @abstractmethod
    def get_t_chunk_size(self):
        """Abstract method for retrieving the chunk size in the time dimension"""
        pass

    @abstractmethod
    def get_num_chunks(self):
        """Abstract method for retrieving number of chunks of the dataset"""
        pass

    @abstractmethod
    def get_crs(self):
        """Abstract method for retrieving the crs of the dataset"""
        pass

    @abstractmethod
    def get_time_range(self):
        """Abstract method for retrieving the time range of the dataset"""
        pass

    @abstractmethod
    def get_time_period(self):
        """Abstract method for retrieving the time_period of the dataset"""
        pass

    @abstractmethod
    def get_datatype(self):
        """Abstract method for retrieving the datatype of the dataset"""
        pass

    @ property
    @abstractmethod
    def bbox(self) -> Bbox:
        pass

    @ property
    @abstractmethod
    def spatial_res(self) -> float:
        pass

    @ property
    @abstractmethod
    def size(self) -> float:
        pass

    @ property
    @abstractmethod
    def chunk_size(self) -> float:
        pass

    @ property
    @abstractmethod
    def num_chunks(self) -> float:
        pass

    @ property
    @abstractmethod
    def crs(self) -> str:
        pass

    @ property
    @abstractmethod
    def time_range(self) -> TimeRange:
        pass

    @ property
    @abstractmethod
    def time_period(self) -> str:
        pass

    @ property
    @abstractmethod
    def datatype(self) -> np.dtype:
        pass

    @ property
    @abstractmethod
    def is_geographic_crs(self) -> bool:
        pass

    @property
    @abstractmethod
    def dataset_default_properties(self) -> Dict:
        pass


class CustomCubeConfig(CubeConfig):
    """
    Cube configuration for Custom datasets.

    Args:
        dataset_name (str): Name of the custom zarr dataset, with '.zarr'
            extension at the end.
        variable_names (Optional[List[str]], optional): Variable names
            of the dataset.
        danube_data_cube: Optional instance of DanbeDataCube,
            the object representing the DanubeDataCube API.
        param ddc_kwargs: Optional keyword arguments passed to the
            DanubeDataCube constructor. Only valid if
            *danube_data_cube* is not given.
    """

    def __init__(self,
                 dataset_name: str,
                 variable_names: Union[str, List[str], None] = None,
                 danube_data_cube: Optional[DanubeDataCube] = None,
                 **ddc_kwargs):

        if danube_data_cube is None:
            danube_data_cube = DanubeDataCube(**ddc_kwargs)
        elif ddc_kwargs:
            raise ValueError(f'Unexpected keyword-arguments:'
                             f' {", ".join(ddc_kwargs.keys())}')

        # Check config parameters
        # Check if user has the dataset specified
        # if dataset_name not in danube_data_cube.dataset_names:
        #     raise ValueError(
        #         f'Invalid dataset_name: {dataset_name}')

        dataset_default_properties = danube_data_cube.get_custom_properties(
            dataset_name)

        if variable_names is None:
            variables = dataset_default_properties.get('variable_names')
        else:
            variables = sorted(set(variable_names)) if isinstance(
                variable_names, list) else sorted(set([variable_names]))
            for var in variables:
                if var not in dataset_default_properties.get('variable_names'):
                    variables.remove(var)
        if not variables:
            raise ValueError('Invalid variable_names:'
                             f'{variable_names}')
        variable_names = variables

        self._dataset_name = dataset_name
        self._variable_names = variable_names
        self._danube_data_cube = danube_data_cube
        self._dataset_default_properties = dataset_default_properties

        self._spatial_res = self.get_spatial_res()
        self._crs = self.get_crs()
        self._time_period = self.get_time_period()
        self._datatype = self.get_datatype()
        self._bbox = self.get_bbox()
        self._time_range = self.get_time_range()

        depth, width, height = self.get_size()
        chunk_width, chunk_height = self.get_xy_chunk_size(width, height)
        chunk_depth = self.get_t_chunk_size(depth)
        num_chunks = self.get_num_chunks(depth, chunk_depth,
                                         width, chunk_width,
                                         height, chunk_height)

        self._size = depth, width, height
        self._chunk_size = chunk_depth, chunk_width, chunk_height
        self._num_chunks = num_chunks

    def get_spatial_res(self):
        sr = self._dataset_default_properties.get('spatial_res')
        assert_true(sr > 0.0, f'Invalid spatial_res: {sr}.')
        return sr

    def get_bbox(self):
        bbox = self._dataset_default_properties.get('bbox')

        precision = min(len(str(bbox[0]).split('.')[-1]),
                        len(str(bbox[1]).split('.')[-1]),
                        len(str(bbox[2]).split('.')[-1]),
                        len(str(bbox[3]).split('.')[-1]))

        try:
            bbox = Bbox(*bbox, precision=precision)
        except (TypeError, ValueError) as error:
            raise ValueError(f'Invalid bbox: {bbox} -- '
                             'must be a tuple of 4 numbers') from error
        return bbox

    def get_crs(self):
        crs = self._dataset_default_properties.get('crs')
        assert_true(crs in CRS_ID_TO_URI, f'Invalid crs: {crs}.')
        return crs

    def get_time_range(self):

        time_range = (
            self._dataset_default_properties.get('start_date'),
            self._dataset_default_properties.get('end_date')
        )

        start_date, end_date = time_range

        try:
            time_range = TimeRange(start_date, end_date)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f'Invalid time_range: {start_date, end_date}') from error
        return time_range

    def get_time_period(self):

        time_period = self._dataset_default_properties.get('time_period')
        assert_true(time_period in TIME_PERIODS,
                    f'Invalid time_period: {time_period}.')

        return time_period

    def get_datatype(self):
        datatype = self._dataset_default_properties.get('datatype')
        # Hardcode datatype #! fix metadata backend

        try:
            datatype = {k: np.dtype(datatype.get(k))
                        for k in self._variable_names}
        except (TypeError, ValueError) as error:
            raise ValueError(f'Invalid datatype {datatype}') from error

        return datatype

    def get_size(self):
        dimensions = self._dataset_default_properties.get('size')
        depth = dimensions.get('time')
        width = dimensions.get('x')
        height = dimensions.get('y')
        return depth, width, height

    def get_xy_chunk_size(self,
                          width: int,
                          height: int) -> Tuple[int, int, int]:
        chunk_width = width
        chunk_height = height

        return chunk_width, chunk_height

    def get_t_chunk_size(self, depth: int) -> Tuple[int, int, int]:
        chunk_depth = depth

        return chunk_depth

    def get_num_chunks(self,
                       depth, chunk_depth,
                       width, chunk_width,
                       height, chunk_height):

        return (math.ceil(depth / chunk_depth),
                width // chunk_width,
                height // chunk_height)

    @ property
    def bbox(self) -> Bbox:
        return self._bbox

    @ property
    def spatial_res(self) -> float:
        return self._spatial_res

    @ property
    def size(self) -> float:
        return self._size

    @ property
    def chunk_size(self) -> float:
        return self._chunk_size

    @ property
    def num_chunks(self) -> float:
        return self._num_chunks

    @ property
    def crs(self) -> str:
        return self._crs

    @ property
    def time_range(self) -> TimeRange:
        return self._time_range

    @ property
    def time_period(self) -> str:
        return self._time_period

    @ property
    def datatype(self) -> np.dtype:
        return self._datatype

    @ property
    def is_geographic_crs(self) -> bool:
        return self._crs in ('CRS84', 'WGS84', 'EPSG:4326')

    @property
    def dataset_default_properties(self) -> Dict:
        return self._dataset_default_properties


class DdcCubeConfig(CubeConfig):
    """
    Cube configuration for DDC datasets.

    Args:
        dataset_name (str): Name of the dataset.
        variable_names (Optional[List[str]], optional): Variable names
            of the dataset.
        bbox (Optional[Bbox], optional): Bounding box, tuple of 4 numbers:
            (minx, miny, maxx, maxy).
        time_range (Optional[TimeRange], optional): Time range tuple:
            (start time, end time).
        time_period (Optional[str, None], optional): A string denoting
            the temporal aggregation period, such as "8D", "1W", "1M".
        danube_data_cube: Optional instance of DanbeDataCube,
            the object representing the DanubeDataCube API.
        param ddc_kwargs: Optional keyword arguments passed to the
            DanubeDataCube constructor. Only valid if
            *danube_data_cube* is not given.
    """

    def __init__(self,
                 dataset_name: str,
                 variable_names: Union[str, List[str], None] = None,
                 bbox: Optional[Tuple[float, float, float, float]] = None,
                 time_range: Optional[TimeRange] = None,
                 time_period: Optional[str] = None,
                 danube_data_cube: Optional[DanubeDataCube] = None,
                 **ddc_kwargs):

        if danube_data_cube is None:
            danube_data_cube = DanubeDataCube(**ddc_kwargs)
        elif ddc_kwargs:
            raise ValueError(f'Unexpected keyword-arguments:'
                             f' {", ".join(ddc_kwargs.keys())}')

        # Check config parameters
        if dataset_name not in danube_data_cube.dataset_names:
            raise ValueError(
                f'Invalid dataset_name: {dataset_name}')

        if variable_names is None:
            variables = danube_data_cube.dataset_vars_names(dataset_name)
        else:
            variables = sorted(set(variable_names)) if isinstance(
                variable_names, list) else sorted(set([variable_names]))
            for var in variables:
                if var not in danube_data_cube.dataset_vars_names(
                        dataset_name):
                    variables.remove(var)
        if not variables:
            raise ValueError('Invalid variable_names:'
                             f'{variable_names}')
        variable_names = variables

        self._dataset_name = dataset_name
        self._variable_names = variable_names
        self._danube_data_cube = danube_data_cube
        self._dataset_default_properties = self._danube_data_cube.get_properties(
            dataset_name)
        self._spatial_res = self.get_spatial_res()
        self._crs = self.get_crs()
        self._time_period = self.get_time_period(time_period)
        self._datatype = self.get_datatype()

        bbox = self.get_bbox(bbox)

        time_range = self.get_time_range(time_range)

        depth, width, height = self.get_size(time_range.time_range, bbox.bbox)

        chunk_width, chunk_height, _ = self.get_xy_chunk_size(width, height)

        # Adjust bbox, time_ranges, size, chunk_size
        if width < 1.5 * chunk_width:
            chunk_width = width
        else:
            width = self._adjust_size(width, chunk_width)
        if height < 1.5 * chunk_height:
            chunk_height = height
        else:
            height = self._adjust_size(height, chunk_height)

        x2, y2 = (bbox.minx + (width-1) * self._spatial_res,
                  bbox.miny + (height-1) * self._spatial_res)

        bbox.maxx = x2
        bbox.maxy = y2

        chunk_depth = self.get_t_chunk_size(chunk_width,
                                            chunk_height,
                                            depth,
                                            width,
                                            height)

        if depth < 1.5 * chunk_depth:
            chunk_depth = depth
        # else:
            # depth = self._adjust_size(depth, chunk_depth)

        date_range = pd.date_range(
            time_range.start_time, periods=depth,
            freq=self._time_period, normalize=True, inclusive='both')
        date_range.freq = None
        end_time = date_range[-1]

        time_range.end_time = end_time

        num_chunks = self.get_num_chunks(depth, chunk_depth,
                                         width, chunk_width,
                                         height, chunk_height)

        self._bbox = bbox
        self._time_range = time_range
        self._size = depth, width, height
        self._chunk_size = chunk_depth, chunk_width, chunk_height
        self._num_chunks = num_chunks

    def get_spatial_res(self):
        sr = self._dataset_default_properties.get('spatial_res')
        assert_true(sr > 0.0, f'Invalid spatial_res: {sr}.')
        return sr

    def get_bbox(self,
                 bbox: Optional[Tuple[float, float, float, float]] = None):

        ds_bbox = self._dataset_default_properties.get('bbox')

        if not bbox:
            bbox = ds_bbox
        else:
            x1 = bbox[0] if bbox[0] >= ds_bbox[0] else ds_bbox[0]
            y1 = bbox[1] if bbox[1] >= ds_bbox[1] else ds_bbox[1]
            x2 = bbox[2] if bbox[2] <= ds_bbox[2] else ds_bbox[2]
            y2 = bbox[3] if bbox[3] <= ds_bbox[3] else ds_bbox[3]
            bbox = (x1, y1, x2, y2)

        precision = len(str(self._spatial_res).split('.')[-1])

        try:
            bbox = Bbox(*bbox, precision=precision)
        except (TypeError, ValueError) as error:
            raise ValueError(f'Invalid bbox: {bbox} -- '
                             'must be a tuple of 4 numbers') from error
        return bbox

    def get_crs(self):
        crs = self._danube_data_cube.dataset(self._dataset_name).get('crs')
        assert_true(crs in CRS_ID_TO_URI, f'Invalid crs: {crs}.')
        return crs

    def get_time_range(self, time_range: Optional[TimeRange] = None):

        ds_time_range = (
            self._dataset_default_properties.get('start_date'),
            self._dataset_default_properties.get('end_date')
        )
        ds_time_range = tuple(map(TimeRange.convert_time, ds_time_range))

        start_date, end_date = (time_range if time_range is not None
                                else (None, None))
        if not start_date:
            start_date = ds_time_range[0]
        else:
            start_date = TimeRange.convert_time(start_date)
            start_date = (start_date if start_date >= ds_time_range[0]
                          else ds_time_range[0])

        if not end_date:
            end_date = ds_time_range[1]
        else:
            end_date = TimeRange.convert_time(end_date)
            end_date = (end_date if end_date <= ds_time_range[1]
                        else ds_time_range[1])

        try:
            time_range = TimeRange(start_date, end_date)
        except (TypeError, ValueError) as error:
            raise ValueError(
                f'Invalid time_range: {start_date, end_date}') from error
        return time_range

    def get_time_period(self, time_period: Optional[str] = None):
        if not time_period:
            time_period = self._dataset_default_properties.get('time_period')
            assert_true(time_period in TIME_PERIODS,
                        f'Invalid time_period: {time_period}.')
        else:
            if time_period not in TIME_PERIODS:
                raise ValueError(f'Invalid time_period: {time_period} -- '
                                 f'valid periods are {TIME_PERIODS}')
        return time_period

    def get_datatype(self):
        dt = self._dataset_default_properties.get('datatype')
        # Hardcode datatype #! fix metadata backend
        dt = 'float32'
        try:
            dt = np.dtype(dt)
        except (TypeError, ValueError) as error:
            raise ValueError(f'Invalid datatype {dt}') from error

        return dt

    def get_size(self, time_range, bbox):
        depth = self._get_t_size(time_range, self._time_period)
        width, height = self._get_xy_size(bbox, self._spatial_res)
        return depth, width, height

    def get_xy_chunk_size(self,
                          width: int,
                          height: int) -> Tuple[int, int, int]:

        item_size = self._datatype.itemsize
        num_pixels_per_chunk = DDC_MAX_CHUNK_SIZE / item_size
        chunk_width = math.ceil(
            math.sqrt(width * num_pixels_per_chunk / height))
        chunk_height = math.ceil((
            num_pixels_per_chunk + chunk_width - 1) // chunk_width)

        return chunk_width, chunk_height, num_pixels_per_chunk

    def get_t_chunk_size(self,
                         chunk_width: int,
                         chunk_height: int,
                         depth: int,
                         width: int,
                         height: int) -> Tuple[int, int, int]:

        chunk_depth, chunk_width, chunk_height = auto_chunks(
            ('auto', chunk_width, chunk_height),
            (depth, width, height), DDC_MAX_CHUNK_SIZE, self._datatype)

        if isinstance(chunk_depth, tuple):
            chunk_depth = chunk_depth[0]

        return chunk_depth

    def get_num_chunks(self,
                       depth, chunk_depth,
                       width, chunk_width,
                       height, chunk_height):

        return (math.ceil(depth / chunk_depth),
                width // chunk_width,
                height // chunk_height)

    def _get_xy_size(self,
                     bbox: Tuple[float, float, float, float],
                     spatial_res: float) -> Tuple[int, int]:

        x1, y1, x2, y2 = bbox
        x_array = np.arange(x1, x2, spatial_res, dtype=np.float64)
        y_array = np.arange(y1, y2, spatial_res, dtype=np.float64)
        width, height = x_array.size, y_array.size
        return width, height

    def _get_t_size(self,
                    time_range: Tuple[pd.Timestamp, pd.Timestamp],
                    time_period: str) -> int:

        start_time, end_time = time_range
        t_array = pd.date_range(start_time, end_time,
                                freq=time_period, normalize=True,
                                inclusive='both', tz='UTC')
        depth = len(t_array)
        return depth

    def _adjust_size(self, size: int, chunk_size: int) -> int:
        if size > chunk_size:
            num_chunk = size // chunk_size
            size = num_chunk * chunk_size
        return int(size)

    @ property
    def bbox(self) -> Bbox:
        return self._bbox

    @ property
    def spatial_res(self) -> float:
        return self._spatial_res

    @ property
    def size(self) -> float:
        return self._size

    @ property
    def chunk_size(self) -> float:
        return self._chunk_size

    @ property
    def num_chunks(self) -> float:
        return self._num_chunks

    @ property
    def crs(self) -> str:
        return self._crs

    @ property
    def time_range(self) -> TimeRange:
        return self._time_range

    @ property
    def time_period(self) -> str:
        return self._time_period

    @ property
    def datatype(self) -> np.dtype:
        return self._datatype

    @ property
    def is_geographic_crs(self) -> bool:
        return self._crs in ('CRS84', 'WGS84', 'EPSG:4326')

    @property
    def dataset_default_properties(self) -> Dict:
        return self._dataset_default_properties
