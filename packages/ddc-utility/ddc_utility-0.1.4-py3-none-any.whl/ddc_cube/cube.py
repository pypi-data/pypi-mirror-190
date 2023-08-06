from typing import Callable
import pandas as pd
import xarray as xr
import zarr

from .config import DdcCubeConfig, CustomCubeConfig
from .chunkstore import DanubeDataCubeChunkStore, CustomChunkStore
from .ddc import DanubeDataCube


def open_ddc_cube(
        cube_config: DdcCubeConfig,
        max_cache_size: int = 2 ** 30,
        danube_data_cube: DanubeDataCube = None,
        **ddc_kwargs) -> xr.Dataset:

    if danube_data_cube is None:
        danube_data_cube = DanubeDataCube(**ddc_kwargs)

    cube_store = DanubeDataCubeChunkStore(danube_data_cube,
                                          cube_config)

    if max_cache_size:
        cube_store = zarr.LRUStoreCache(cube_store, max_cache_size)

    return xr.open_zarr(cube_store)


def open_custom_cube(
        cube_config: CustomCubeConfig,
        max_cache_size: int = 2 ** 30,
        danube_data_cube: DanubeDataCube = None,
        **ddc_kwargs) -> xr.Dataset:

    if danube_data_cube is None:
        danube_data_cube = DanubeDataCube(**ddc_kwargs)

    cube_store = CustomChunkStore(danube_data_cube,
                                  cube_config)

    if max_cache_size:
        cube_store = zarr.LRUStoreCache(cube_store, max_cache_size)

    return xr.open_zarr(cube_store)


def set_valid_obs(dataarray: xr.DataArray) -> xr.DataArray:
    """
    Set valid observation Timestamps as new, MultiIndex coordinate.

    Args:
        dataarray (xr.DataArray): _description_
    """
    lst = (~dataarray.isnull().all(dim=['x', 'y']).values).astype(int)
    lst.append(dataarray.time.values)
    idx = pd.MultiIndex.from_arrays(lst, names=('valid_obs', 'time_obs'))

    arr = xr.DataArray(dataarray.values,
                       [("time", idx), ("y", dataarray.y.values),
                        ("x", dataarray.x.values)])

    return arr
