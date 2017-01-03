from jsub.error import JsubError


class ExtensionNotFoundError(JsubError):
    pass



class ConfigNotSetupError(JsubError):
    pass


class ExtensionNotSetupError(JsubError):
    pass


class RepoNotSetupError(ExtensionNotSetupError):
    pass

class ContentNotSetupError(ExtensionNotSetupError):
    pass

class AppNotSetupError(ExtensionNotSetupError):
    pass

class SplitterNotSetupError(ExtensionNotSetupError):
    pass

class BackendNotSetupError(ExtensionNotSetupError):
    pass
