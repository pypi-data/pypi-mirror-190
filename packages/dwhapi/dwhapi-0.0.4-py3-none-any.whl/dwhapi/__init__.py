from .ddl import DdlApi
from .project import ProjectApi


class Api:
    ddl: DdlApi
    project: ProjectApi

    def __init__(self, api_key):
        # self.ddl = DdlApi(api_key)
        self.project = ProjectApi(api_key)
        self.ddl = DdlApi(api_key)
