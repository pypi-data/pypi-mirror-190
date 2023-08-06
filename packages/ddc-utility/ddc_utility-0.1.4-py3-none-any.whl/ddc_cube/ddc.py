import json
import logging
import os
import platform
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.adapters import HTTPAdapter, Retry
from requests_oauthlib import OAuth2Session

from .__version__ import version
from .constants import (DEFAULT_DDC_API_URL, DEFAULT_DDC_BINARY_URL,
                        DEFAULT_DDC_METADATA_URL, DEFAULT_DDC_TOKEN_URL,
                        CUSTOM_DDC_AOI_URL, CUSTOM_DDC_METADATA_URL,
                        CUSTOM_DDC_BINARY_URL, DEFAULT_NUM_RETRIES,
                        DEFAULT_REQUEST_TIMEOUT, DEFAULT_RETRY_BACKOFF_BASE)
from .metadata import DanubeDataCubeMetadata


logger = logging.getLogger('danube-data-cube')


class DanubeDataCube():
    """Represents the Danube Data Cube data portal.

    Args:
        client_id (Optional[str]): Danube Data Cube client id.
        client_secret (Optional[str]): Danube Data Cube client secret.
        api_url (Optional[str]): Alternative Danube Data Cube API URL.
        token_url (Optional[str]): Alternative Danube Data Cube token API URL.
        binary_url (Optional[str]): Alternative Danube Data Cube data API URL.
        metadata_url (Optional[str]): Alternative Danube Data Cube
            metadata API URL.
        aoi_url (Optional[str]): Alternative Danube Data Cube AOI API URL.
        custom_binary_url (Optional[str]): Alternative Danube Data Cube
            custom data API URL.
        custom_metadata_url (Optional[str]): Alternative Danube Data Cube
            custom metadata API URL.
        num_retries (int): Number of retries for failed API
            requests, e.g. ```5`` times.
        retry_backoff_base (float): Request retry backoff base.
            Must be greater than one, e.g. ``1.5``.
        timeout (Tuple): Request timeout.
        session (Union["SerializableOAuth2Session", Any]):
            Optional request session object (mostly for testing).

    """

    METADATA = DanubeDataCubeMetadata()

    def __init__(self,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 token: Optional[str] = None,
                 api_url: Optional[str] = None,
                 token_url: Optional[str] = None,
                 binary_url: Optional[str] = None,
                 metadata_url: Optional[str] = None,
                 aoi_url: Optional[str] = None,
                 custom_binary_url: Optional[str] = None,
                 custom_metadata_url: Optional[str] = None,
                 num_retries: int = DEFAULT_NUM_RETRIES,
                 retry_backoff_base: float = DEFAULT_RETRY_BACKOFF_BASE,
                 timeout: Tuple = DEFAULT_REQUEST_TIMEOUT,
                 session: Union[OAuth2Session, Any] = None):

        # API URLs
        self.api_url = (
            api_url or
            os.environ.get('DDC_API_URL', DEFAULT_DDC_API_URL)
        )
        self.token_url = (
            token_url or
            os.environ.get('DDC_TOKEN_URL', DEFAULT_DDC_TOKEN_URL)
        )
        self.binary_url = (
            binary_url or
            os.environ.get('DDC_BINARY_URL', DEFAULT_DDC_BINARY_URL)
        )
        self.metadata_url = (
            metadata_url or
            os.environ.get('DDC_METADATA_URL', DEFAULT_DDC_METADATA_URL)
        )
        self.aoi_url = (
            aoi_url or
            os.environ.get('DDC_AOI_URL', CUSTOM_DDC_AOI_URL)
        )
        self.custom_binary_url = (
            custom_binary_url or
            os.environ.get('DDC_CUSTOM_BINARY_URL', CUSTOM_DDC_BINARY_URL)
        )
        self.custom_metadata_url = (
            custom_metadata_url or
            os.environ.get('DDC_CUSTOM_METADATA_URL', CUSTOM_DDC_METADATA_URL)
        )

        # Client credentials
        self.client_id = client_id or os.environ.get('DDC_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get(
            'DDC_CLIENT_SECRET')

        if not self.client_id or not self.client_secret:
            raise ValueError(
                'Both client_id and client_secret must be provided. '
                'Consider setting environment variables '
                'DDC_CLIENT_ID and DDC_CLIENT_SECRET.'
            )

        self.token = token

        self.session = session

        if session is None:
            # Create OAuth2 session
            self.session = self._get_session(
                timeout=timeout,
                total=num_retries,
                backoff_factor=retry_backoff_base,
                status_forcelist=[429, 500, 502, 503, 504])

            # use existing token if supplied
            self.session.token = self.token if self.token else \
                self._fetch_token(
                    self.token_url,
                    dict(client_id=self.client_id,
                         client_secret=self.client_secret)
                )

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    @ property
    def datasets(self) -> Dict:
        """Datasets available in Danube Data Cube."""
        return self.METADATA.datasets

    @ property
    def dataset_names(self) -> List[str]:
        """Names of the datasets available in Danube Data Cube."""
        return self.METADATA.dataset_names

    def dataset(self, dataset_name: str) -> Optional[Dict]:
        """
        Dataset specified by the name.

        Args:
            dataset_name (str): Name of the dataset.
        """
        return self.METADATA.dataset(dataset_name)

    def dataset_vars(self, dataset_name: str, default=None) -> Optional[Dict]:
        """Variables available specified by the dataset name.

        Args:
            dataset_name (str): Name of the dataset.
            default (Any): Default value to return.
        """
        return self.METADATA.dataset_vars(dataset_name, default)

    def dataset_vars_names(self, dataset_name: str,
                           default=None) -> Optional[List[str]]:
        """Names of the variables available specified by the dataset name.

        Args:
            dataset_name (str): Name of the dataset.
            default (Any): Default value to return.
        """
        return self.METADATA.dataset_vars_names(dataset_name, default)

    def dataset_var(self, dataset_name: str, variable_name: str,
                    default=None) -> Optional[Dict]:
        """Variable specified by the dataset name and variable name.

        Args:
            dataset_name (str): Name of the dataset.
            variable_name (str): Name of the variable.
            default (Any): Default value to return.
        """
        return self.METADATA.dataset_var(dataset_name, variable_name, default)

    def get_aoi(self, with_geometry: bool = True,
                mime_type: str = 'application_json') -> Dict[str, Any]:
        """
        Get user's area of interest (AOI).

        Args:
            with_geometry (bool, optional): Whether to retrive geomatry values.
                Defaults to True.
            mime_type (str): Media type, default is 'application/json'.
        """

        request = dict(user_id=self.client_id, with_geometry=with_geometry)
        headers = self._get_request_headers(mime_type)
        headers.update({'client_id': self.client_id})
        response = self.session.get(self.aoi_url,
                                    params=request,
                                    headers=headers)

        DanubeDataCubeError.raise_for_bad_response(
            response,
            f'Failed to fetch AOIs for user {self.client_id}.')

        aoi = json.loads(response.content)

        return aoi

    def get_properties(self,
                       dataset_name: str,
                       mime_type: str = 'application/json') -> Dict[str, Any]:
        """
        Get the properties of the dataset e.g. geographical and temporal
        extent, resolution, datatype etc..

        Args:
            dataset_name (str): Name of the dataset.
            mime_type (str): Media type, default is 'application/json'.
        """
        request = dict(dataset=dataset_name.lower())
        headers = self._get_request_headers(mime_type)
        headers.update({'client_id': self.client_id})

        response = self.session.get(self.metadata_url,
                                    params=request,
                                    headers=headers)

        DanubeDataCubeError.raise_for_bad_response(
            response,
            f'Failed to fetch properties of {dataset_name} '
            f'from {self.metadata_url}')

        properties = json.loads(response.content)

        bbox = properties.pop('bbox')
        spatial_res = float(properties.pop('spatial_res'))
        time_range_length = float(properties.pop('time_range_length'))
        datatypes = properties.pop('datatypes')
        time_period = properties.pop('time_freq')

        bbox = tuple(map(float, bbox.split(',')))

        properties.update({'bbox': bbox,
                           'spatial_res': spatial_res,
                           'time_range_length': time_range_length,
                           'datatypes': datatypes,
                           'time_period': time_period})
        return properties

    def get_custom_properties(self,
                              dataset_name: str,
                              mime_type: str = 'application/json') -> Dict[str, Any]:
        """
        Get the properties of user's custom zarr datset e.g. geographical and temporal
        extent, resolution, datatype etc..

        Args:
            dataset_name (str): Name of the custom zarr.
            mime_type (str): Media type, default is 'application/json'.
        """
        request = dict(dataset=dataset_name.lower())
        headers = self._get_request_headers(mime_type)
        headers.update({'client_id': self.client_id})

        response = self.session.get(self.custom_metadata_url,
                                    params=request,
                                    headers=headers)

        DanubeDataCubeError.raise_for_bad_response(
            response,
            f'Failed to fetch properties of {dataset_name} '
            f'from {self.metadata_url}')

        properties = json.loads(response.content)

        spatial_res = float(properties.pop('spatial_res'))
        size = properties.pop('dimensions')
        datatype = properties.pop('dtypes')
        time_period = properties.pop('time_freq')
        variable_names = properties.pop('bands')

        bbox = tuple(properties.pop('bbox'))

        properties.update({'bbox': bbox,
                           'spatial_res': spatial_res,
                           'size': size,
                           'datatype': datatype,
                           'time_period': time_period,
                           'variable_names': variable_names})
        return properties

    def get_data(self,
                 url: str,
                 request: Dict,
                 mime_type: str) -> Optional[requests.Response]:
        """
        Fetch data from backend.

        Args:
            dataset_name (str): Name of the dataset.
            mime_type (str): Media type, default is 'application/json'.
        """
        headers = self._get_request_headers(mime_type)
        headers.update({'client_id': self.client_id})

        response = None
        response_error = None
        start_time = time.time()

        try:
            response = self.session.get(url,
                                        params=request,
                                        headers=headers)
            response_error = None

        except Exception as e:
            response_error = e
            response = None

        if response is not None and response.ok:
            return response

        end_time = time.time()

        time_diff = end_time - start_time

        logger.error('Failed to fetch data from Danube Data Cube'
                     ' after %s seconds', time_diff,
                     exc_info=response_error)

        if response is not None:
            logger.error('HTTP status code was %s', response.status_code)

        if response_error:
            raise response_error
        elif response is not None:
            raise DanubeDataCubeError.raise_for_bad_response(
                response,
                f'Failed to fetch data from {url}')

        return response

    @ classmethod
    def _get_request_headers(cls, mime_type: str):
        return {
            'Accept': mime_type,
            'DDC-Tag': 'ddc_cube',
            'User-Agent': f'ddc_cube/{version} '
                          f'{platform.python_implementation()}/'
                          f'{platform.python_version()} '
                          f'{platform.system()}/{platform.version()}'
        }

    def _get_session(self,
                     timeout: Union[float, Tuple[float, float]],
                     total: int,
                     backoff_factor: float,
                     status_forcelist: List):

        client = BackendApplicationClient(client_id=self.client_id)
        session = OAuth2Session(client=client)

        max_retries = Retry(total=total,
                            backoff_factor=backoff_factor,
                            allowed_methods=None,
                            status_forcelist=status_forcelist)

        adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=max_retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def _fetch_token(self,
                     token_url: str,
                     auth_body: Dict,
                     mime_type: str = 'application/json'):

        session = self._get_session(
            timeout=3.05,
            total=3,
            backoff_factor=1.001,
            status_forcelist=[429, 500, 502, 503, 504])

        headers = self._get_request_headers(mime_type)
        headers.update({'client_id': self.client_id})

        with session as s:
            response = s.post(token_url, json=auth_body)

        DanubeDataCubeError.raise_for_bad_response(
            response,
            f'Failed to fetch token from {token_url}')

        token = json.loads(response.content)

        logger.info('fetched Danube Data Cube access token successfully')

        return token


class DanubeDataCubeError(ValueError):
    def __init__(self, *args, response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._response = response

    @ property
    def response(self):
        return self._response

    @ classmethod
    def raise_for_bad_response(cls,
                               response: requests.Response,
                               message: str = ''):
        try:
            response.raise_for_status()
        except requests.HTTPError as errh:
            raise DanubeDataCubeError(f'{message}',
                                      response=response) from errh

        except requests.ConnectionError as errc:
            raise DanubeDataCubeError(f'{message}',
                                      response=response) from errc

        except requests.Timeout as errt:
            raise DanubeDataCubeError(f'{message}',
                                      response=response) from errt


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        else:
            self.timeout = 5
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
