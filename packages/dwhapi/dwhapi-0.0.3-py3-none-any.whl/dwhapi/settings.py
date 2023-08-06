from logging import getLogger

LOGGER = getLogger("dwhlogger")

SERVER_URL = "https://api.dwh.dev"
API_PREFIX = "/api/v1"

PROJECT_URL = SERVER_URL + API_PREFIX + '/project'
PROJECT_INFO_URL = PROJECT_URL + '/{project_uuid}'

DDL_URL = SERVER_URL + API_PREFIX + '/ddl'
DDL_SOURCE_STATUS = DDL_URL + '/SOURCE/{source_uuid}/status'
DDL_SOURSE_MANIFEST_ADD_URL = DDL_URL + '/dbt'
