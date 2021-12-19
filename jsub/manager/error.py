from jsub.error import JsubError


class ExtensionNotFoundError(JsubError):
    pass

class BadConfigError(JsubError):
	pass

class ConfigNotSetupError(JsubError):
    pass


class ExtensionNotSetupError(JsubError):
    pass


class RepoNotSetupError(ExtensionNotSetupError):
    pass

class ContentNotSetupError(ExtensionNotSetupError):
    pass

class ScenarioNotSetupError(ExtensionNotSetupError):
    pass

class JobvarListNotSetupError(ExtensionNotSetupError):
    pass

class BackendNotSetupError(ExtensionNotSetupError):
    pass
