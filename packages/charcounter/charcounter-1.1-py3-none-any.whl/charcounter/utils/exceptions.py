class CustomTypeErrorException(Exception):
    """Raised when type(value) is not expected"""
    pass


class CustomFileNotFoundException(Exception):
    """Raised when file or directory is not exist"""
    pass


class CommandLineArgumentsException(Exception):
    """Raised when required arguments was not passed"""
    pass
