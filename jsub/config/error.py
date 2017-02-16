from jsub.error import JsubError

class ConfigError(JsubError):
    pass

class SyntaxError(ConfigError):
    pass

class UnknownConfigFormatError(ConfigError):
    pass

class ConfigFileNotFoundError(ConfigError):
    pass

class UnknownUpdateMethodError(ConfigError):
    pass
