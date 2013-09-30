#!/usr/bin/python
'''
This class will take a config file and compare it
against a base config file. The goal is to convert
the config file into an object with the types that
it is expected.
'''
import json
from ConfigTypes import ConfigType
from ConfigParser import SafeConfigParser

DELIMITER = ';'

class ConfigCheck():

    def __init__(self):
        """ Initializes config parsers
        """
        
        # Add variales to save parser info
        self.config1 = SafeConfigParser(allow_no_value=True)
        self.config2 = SafeConfigParser(allow_no_value=True)
        self.discrepencies = {}

    def __repr__(self):
        """ Print out current class instance
        """

        outl = 'class :' + self.__class__.__name__

        for attr in self.__dict__:
            outl += '\n\t' + attr + ' : ' + str(getattr(self, attr))

        return outl

    def compare_types(self, type_file, config_file):
        """ Compares config files
        """

        # Load the files info the config parsers
        self.config1.read(type_file)
        self.config2.read(config_file)

        # loop through the sections in config file and compare
        for section in self.config1.sections():
            if self.config2.has_section(section):
                for item in self.config1.items(section):
                    key = item[0]
                    if DELIMITER in item[1]:
                        temp_value = item[1].split(DELIMITER)

                        # have to check if the item is '' for NoneType
                        if temp_value[0] == '':
                            temp_value[0] = None
                        
                        expected = ConfigType(temp_value[0], bool(temp_value[1]))
                    else:
                        expected = ConfigType(item[1])

                    if self.config2.has_option(section, key):
                        value = self.config2.get(section,key)
                        
                        try:
                            config_file_value = ConfigType(value)
                        except ValueError, ve:
                            self.value_error(section, key, value, error=str(ve))
                            break
                        except TypeError, te:
                            self.type_error(section, key, value, error=str(te))
                            break
                        
                        if config_file_value.type.value != expected.type.value:
                            self.type_error(section,
                                            key,
                                            config_file_value.value,
                                            config_file_value.type.value,
                                            expected.type.value)
                    else:
                        if expected.required is True:
                            self.value_error(section, key, None, expected.type.value)
            else:
                self.section_mismatch(section)

    def compare_values(self, expected_value_file, value_file):
        """ Compares the values of two config files
        """

        # Load the files info the config parsers
        self.config1.read(expected_value_file)
        self.config2.read(value_file)

        # loop through the sections in config file and compare
        for section in self.config1.sections():
            if self.config2.has_section(section):
                for item in self.config1.items(section):
                    key = item[0]
                    expected_value = item[1]

                    # Check for a blank expected value
                    if expected_value == "":
                        expected_value = None

                    if self.config2.has_option(section, key):
                        actual_value = self.config2.get(section,key)
                        if actual_value != expected_value:
                            self.value_error(section,
                                             key,
                                             actual_value,
                                             expected_value)

                    else:
                        self.option_mismatch(section, key)
            else:
                self.section_mismatch(section)


    def section_mismatch(self, section, value=None):
        """ Adds a mismatched section to the discrepencies dictionary
        """

        if not self.discrepencies.has_key(section):
            self.discrepencies[section] = {}

    def option_mismatch(self, section, option):
        """ Adds a mismatched option to the discrepencies dictionary
        """

        self.section_mismatch(section)
        if not self.discrepencies[section].has_key(option):
            self.discrepencies[section][option] = {}

    def value_error(self, section, option, value,
                    expected=None, error=None):
        self.option_mismatch(section, option)
        if not error:
            error = "{0} found, {1} expected".format(value, expected)

        self.option_mismatch(section, option)
        if not self.discrepencies[section][option].has_key('value'):
            self.discrepencies[section][option]['value'] = value
        if not self.discrepencies[section][option].has_key('error'):
            self.discrepencies[section][option]['error'] = error

    def type_error(self, section, option, value,
                   value_type=None, expected=None, error=None):
        self.option_mismatch(section, option)

        if not error:
            error = "{0} has type {1}: {2} expected".format(value,
                                                            str(value_type),
                                                            str(expected))
        if not self.discrepencies[section][option].has_key('value'):
            self.discrepencies[section][option]['value'] = value
        if not self.discrepencies[section][option].has_key('error'):
            self.discrepencies[section][option]['error'] = error

    def pprint(self):
        """ Pretty prints the discrepencies dictionary
        """
        print json.dumps(self.discrepencies, sort_keys=True, indent=4)
