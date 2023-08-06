class DdlException(Exception):
    pass


class DdlNotfound(DdlException):
    pass


class DdlParsingInProgress(DdlException):
    pass


class DdlDuplicateSources(DdlException):
    pass


class DdlVersionError(DdlException):
    pass


class DdlCheckNotFound(DdlException):
    pass


class DdlIsEmpty(DdlException):
    pass


class DdlParseError(DdlException):
    pass


class DdlRelationsNotFound(DdlException):
    pass


class DdlObjectNotFound(DdlException):
    pass


class DdlSourceNotFound(DdlException):
    pass


class DdlParentBeforeCommit(DdlException):
    pass


class DdlVersionAlreadyExists(DdlException):
    pass


DDL_EXCEPTIONS = {"DDL_NOT_FOUND": DdlNotfound,
                  "DDL_PARSING_IN_PROGRESS": DdlParsingInProgress,
                  "DDL_VERSION_ALREADY_EXISTS": DdlVersionAlreadyExists,
                  "DDL_DUPLICATE_SOURCES": DdlDuplicateSources,
                  "DDL_VERSION_ERROR": DdlVersionError,
                  "DDL_CHECK_NOT_FOUND": DdlCheckNotFound,
                  "DDL_IS_EMPTY": DdlIsEmpty,
                  "DDL_PARSE_ERROR": DdlParseError,
                  "DDL_RELATIONS_NOT_FOUND": DdlRelationsNotFound,
                  "DDL_OBJECT_NOT_FOUND": DdlObjectNotFound,
                  "DDL_SOURCE_NOT_FOUND": DdlSourceNotFound,
                  "DDL_PARENT_BEFORE_COMMIT": DdlParentBeforeCommit}


class ProjectException(Exception):
    pass


class ProjectAlreadyExists(ProjectException):
    pass


class ProjectNotFound(ProjectException):
    pass


class ProjectEmpty(ProjectException):
    pass


class ProjectNameIsInvalid(ProjectException):
    pass


class ProjectActionForbidden(ProjectException):
    pass


PROJECT_EXCEPTIONS = {
    "PROJECT_ALREADY_EXISTS": ProjectAlreadyExists,
    "PROJECT_NOT_FOUND": ProjectNotFound,
    "PROJECT:EMPTY": ProjectEmpty,
    "PROJECT_NAME_IS_INVALID": ProjectNameIsInvalid,
    "PROJECT_ACTION_FORBIDDEN": ProjectActionForbidden
}


class UnsupportedException(Exception):
    pass


class ServiceError(Exception):
    pass
