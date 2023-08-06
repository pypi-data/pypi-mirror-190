from .base import BaseApi
from .exceptions import DDL_EXCEPTIONS
from .settings import DDL_URL, DDL_SOURCE_STATUS, DDL_SOURSE_MANIFEST_ADD_URL
from typing import Literal
import os

REQUEST_TYPE = Literal['GET_DDL', 'CUSTOM']
FILE_TYPE = Literal['SQL', 'CSV', 'TSV']


class DdlApi(BaseApi):
    def __init__(self, api_key) -> None:
        super(DdlApi, self).__init__(api_key, DDL_EXCEPTIONS)

    def add_source(self, database_uuid: str, source: str, request_type: REQUEST_TYPE, file_type: FILE_TYPE = 'SQL',
                   environment='development', branch='main',
                   rebuild_etl=True, rebuild_report=True):
        print(source)
        payload = {
            "database": {
                "uuid": database_uuid,
                "environment": environment,
                "branch": {
                    "name": branch
                }
            },
            "source": source,
            "type": request_type,
            "filetype": file_type,
            "rebuild": {
                "etl": rebuild_etl,
                "report": rebuild_report
            }
        }
        return self._request('POST', DDL_URL, json=payload)

    def add_source_from_file(self, database_uuid: str, file_name: str, request_type: REQUEST_TYPE,
                             file_type: FILE_TYPE = 'SQL',
                             environment='development', branch='main',
                             rebuild_etl=True, rebuild_report=True):
        if not os.path.exists(file_name):
            raise FileExistsError("File %s doesn't exist")

        with open(file_name, 'r') as fd:
            source = fd.read()
            return self.add_source(database_uuid, source, request_type, file_type, environment, branch, rebuild_etl,
                                   rebuild_report)

    def get_source_status(self, source_uuid: str):
        return self._request('GET', DDL_SOURCE_STATUS.format(source_uuid=source_uuid))

    def add_dbt_manifest(self, database_uuid: str, manifest: str, environment: str = 'development',
                         branch: str = 'main'):
        payload = {
            "database": {
                "uuid": database_uuid,
                "environment": environment,
                "branch": {
                    "name": branch
                }
            },
            "source": manifest,
            "type": "MANIFEST"
        }
        return self._request('GET', DDL_SOURSE_MANIFEST_ADD_URL, json=payload)
