class MissingRequirement(Exception):
    """
    Raised if there is an error with the request
    """
    pass

class UnsupportedVersion(Exception):
    """
    Raised if the version is unsupported
    """
    pass