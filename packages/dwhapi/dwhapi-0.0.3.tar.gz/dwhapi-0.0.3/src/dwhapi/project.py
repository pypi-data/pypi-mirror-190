from .settings import PROJECT_URL, PROJECT_INFO_URL
from .exceptions import PROJECT_EXCEPTIONS
from .base import BaseApi


class ProjectApi(BaseApi):

    def __init__(self, api_key) -> None:
        super(ProjectApi, self).__init__(api_key, PROJECT_EXCEPTIONS)

    def create_project(self, project_name: str):
        payload = {
            "project": {
                "name": project_name
            },
            "vendor": "snowflake"
        }
        return self._request('POST', PROJECT_URL, json=payload)

    def get_project_info(self, project_uuid: str):
        return self._request(
            'GET', PROJECT_INFO_URL.format(project_uuid=project_uuid))

    def get_project_list(self):
        return self._request('GET', PROJECT_URL)

