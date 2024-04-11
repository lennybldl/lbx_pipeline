"""Manage the application's proxies to avoid manipulating the internal api."""


class Proxy(object):
    """Manage the base class for proxy objects."""

    __api_instance = None

    def __init__(self, source):
        """Initialize the object.

        Arguments:
            source (object): The source instance the proxy wraps.
        """
        if not source:
            raise ValueError("Can't create a proxy without a valid source")
        # keep the api instance in memory
        self.__api_instance = source

    def __repr__(self):
        """Override the __repr__ method.

        Returns:
            str: The new representation of the object.
        """
        return self.__api_instance.__repr__()

    # methods

    @staticmethod
    def __get_api_instance(arg):
        """Get the api instance of a given argument.

        Arguments:
            arg (-): The agrument to extract the api instance from.

        Returns:
            -: The api instance if possible, else the unconverted agument.
        """
        if isinstance(arg, Proxy):
            return arg._Proxy__api_instance
        return arg
