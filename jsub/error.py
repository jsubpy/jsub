class JsubError(Exception):
    pass


class SplitterParamError(JsubError):
    pass

class LauncherNotFoundError(JsubError):
    pass


class TaskIdFormatError(JsubError):
    pass

class TaskNotFoundError(JsubError):
    pass


class RepoError(JsubError):
    pass

class RepoReadError(RepoError):
    pass

class RepoWriteError(RepoError):
    pass
