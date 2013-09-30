#!/usr/bin/python
""" Takes a ConfigParser item object and determines what
ConfigType it is

This should be an enumeration
"""

import types

SIZE_APPEND = ('k', 'M', 'G')

class ConfigType():

    def __init__(self, value, required=False):
        """ Converts a string to the proper type method
        for that strings value
        """
        self.value = value
        self.required = required
        self.type = self._to_class(self.value)

    def __repr__(self):
        """ Prints out instance of class
        """

        outl = 'class :' + self.__class__.__name__

        for attr in self.__dict__:
            outl += '\n\t' + attr + ' : ' + str(getattr(self, attr))

        return outl

    def _to_class(self, value, required=False):
        """ Converts value to type method
        """

        if isinstance(value, types.NoneType):
            return NoneType()
        elif not isinstance(value, types.StringType):
            raise TypeError(
                "{0} should be of type {1}, it is type {2}".format(value,
                                                                   types.StringType,
                                                                   type(value)))

        # IntegerType
        if value.isdigit():
            return IntType()

        # All types that contain a .
        if '.' in value:
            
            # Gather the amount of . in the value
            period_count = value.count('.')

            # If a single . exist we have 1 of the following
            if period_count == 1:

                # LogFileType
                if 'log' in value:
                    return LogFileType()

                # LockFileType
                elif 'lock' in value:
                    return LockFileType()

                # SockFileType
                elif 'sock' in value:
                    return SockFileType()

                else:
                    is_float = value.split('.')
                    for item in is_float:
                        if not item.isdigit():
                            raise TypeError(
                                "{0} is not of type: {1}".format(item,
                                                                 types.IntType))
                    return FloatType()
            
            # If we have 4 periods we have an ipaddress
            elif period_count == 3:
                is_ip = value.split('.')
                for item in is_ip:
                    if not item.isdigit():
                        raise TypeError(
                            "{0} is not of type: {1}".format(item,
                                                             types.IntType))

                    # Check to make sure item is in the range 0..254
                    if not int(item) in range(255):
                        raise ValueError(
                            "{0} is not in a valid ip octet range".format(item))

                return IpAddressType()

            else:
                raise TypeError(
                    "Cannot find valid ConfigType for {0}".format(value))

        else:
            # Look at the last character in the value
            # If it is in SizeAppend we need to make
            # sure the rest of the value is a digit

            if value[-1] in SIZE_APPEND:
                size = value.rstrip(value[-1])
                if not size.isdigit():
                    raise TypeError(
                        "{0} is not of type: {1}".format(size,
                                                         types.IntType))
                return SizeType()
            else:
                return StringType()


class StringType():

    def __init__(self):
        self.value = types.StringType


class IntType():

    def __init__(self):
        self.value = types.IntType


class FloatType():

    def __init__(self):
        self.value = types.FloatType


class NoneType():

    def __init__(self):
        self.value = types.NoneType


class IpAddressType():

    def __init__(self):
        self.value = "IpAddress"


class SizeType():
    
    def __init__(self):
        self.value = "Size"


class LockFileType():
    
    def __init__(self):
        self.value = "LockFile"


class SockFileType():
    
    def __init__(self):
        self.value = "SockFile"


class LogFileType():
    
    def __init__(self):
        self.value = "LogFile"     