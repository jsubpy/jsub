class JsubError(Exception):
    pass

class SplitterError(JsubError):
    pass

class SplitterParamError(SplitterError):
    pass

class LauncherError(JsubError):
    pass

class LauncherNotFoundError(LauncherError):
    pass


class BackendError(JsubError):
    pass

class BackendNotFoundError(BackendError):
    pass


class TaskError(JsubError):
    pass

class TaskIdFormatError(TaskError):
    pass

class TaskNotFoundError(TaskError):
    pass


class RepoError(JsubError):
    pass

class RepoReadError(RepoError):
    pass

class RepoWriteError(RepoError):
    pass
