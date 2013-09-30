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
                            self.value_error(section, key, str(ve))
                        except TypeError, te:
                            self.type_error(section, key, str(te))
                        

                        if config_file_value.type.value != expected.type.value:
                            self.option_type_mismatch(section,
                                                      key,
                                                      config_file_value.value,
                                                      str(config_file_value.type.value),
                                                      str(expected.type.value))
                    else:
                        if expected.required is True:
                            self.option_type_mismatch(section, key, '',
                                                      str(ConfigType(None).type.value),
                                                      str(expected.type.value))
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
                            self.option_value_mismatch(section,
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

    def option_type_mismatch(self, section, option, value, value_type, expected_type):
        """ Adds a mismatched option type to discrepencies dictionary
        """

        self.option_mismatch(section, option)
        if not self.discrepencies[section][option].has_key('expected_type'):
            self.discrepencies[section][option]['expected_type'] = expected_type
        if not self.discrepencies[section][option].has_key('value'):
            self.discrepencies[section][option]['value'] = value
        if not self.discrepencies[section][option].has_key('value_type'):
            self.discrepencies[section][option]['value_type'] = value_type

    def option_value_mismatch(self, section, option, value, expected_value):
        """ Adds a mismatched option value to discrepencies dictionary
        """

        self.option_mismatch(section, option)
        if not self.discrepencies[section][option].has_key('value'):
            self.discrepencies[section][option]['value'] = value
        if not self.discrepencies[section][option].has_key('expected_value'):
            self.discrepencies[section][option]['expected_value'] = expected_value

    def value_error(self, section, option, error):
        self.option_mismatch(section, option)
        if not self.discrepencies[section][option].has_key('value_error'):
            self.discrepencies[section][option]['value_error'] = error

    def type_error(self, section, option, error):
        self.option_mismatch(section, option)
        if not self.discrepencies[section][option].has_key('type_error'):
            self.discrepencies[section][option]['type_error'] = error

    def pprint(self):
        """ Pretty prints the discrepencies dictionary
        """
        print json.dumps(self.discrepencies, sort_keys=True, indent=4)
