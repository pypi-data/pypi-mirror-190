
DEFAULT_DDC_API_URL = 'https://api.cropomservices.com'
DEFAULT_DDC_TOKEN_URL = f'{DEFAULT_DDC_API_URL}/dynamic_data_cube/get_token'
DEFAULT_DDC_BINARY_URL = f'{DEFAULT_DDC_API_URL}/dynamic_data_cube/get_binary'
DEFAULT_DDC_METADATA_URL = f'{DEFAULT_DDC_API_URL}/dynamic_data_cube/get_meta'
CUSTOM_DDC_AOI_URL = f'{DEFAULT_DDC_API_URL}/aoi_manager/get_aoi'
CUSTOM_DDC_BINARY_URL = f'{DEFAULT_DDC_API_URL}/dynamic_data_cube/get_custom_binary'
CUSTOM_DDC_METADATA_URL = f'{DEFAULT_DDC_API_URL}/dynamic_data_cube/get_custom_meta'
DEFAULT_CRS = "EPSG:4326"

CRS_ID_TO_URI = {
    "EPSG:4326": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "WGS84": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "http://www.opengis.net/def/crs/EPSG/0/4326":
        "http://www.opengis.net/def/crs/EPSG/0/4326",
    "EPSG:3857": "https://www.opengis.net/def/crs/EPSG/0/3857",
    "https://www.opengis.net/def/crs/EPSG/0/3857":
        "https://www.opengis.net/def/crs/EPSG/0/3857",
    "EPSG:23700": "https://www.opengis.net/def/crs/EPSG/0/23700",
    "EOV": "https://www.opengis.net/def/crs/EPSG/0/23700",
    "https://www.opengis.net/def/crs/EPSG/0/23700":
        "https://www.opengis.net/def/crs/EPSG/0/23700",
    "EPSG:3035": "https://www.opengis.net/def/crs/EPSG/0/3035",
    "https://www.opengis.net/def/crs/EPSG/0/3035":
        "https://www.opengis.net/def/crs/EPSG/0/3035"
}

DDC_MAX_CHUNK_SIZE = 2000000

DEFAULT_BBOX = (15.0, 44.0, 24.0, 50.0)

DEFAULT_RETRY_BACKOFF_BASE = 1.5
DEFAULT_NUM_RETRIES = 3
DEFAULT_REQUEST_TIMEOUT = (3.05, 10)

TIME_PERIODS = ['D', '7D', 'M', 'MS', '1M', '1MS', '1Y', '1YS']
