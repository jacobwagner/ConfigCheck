#!/usr/bin/python

import os
from lib.ConfigCompare import ConfigCompare

type_file = os.path.join(os.path.dirname(__file__), 'test/configs', 'types.cfg')
test_file = os.path.join(os.path.dirname(__file__), 'test/configs', 'test.cfg')

compare = ConfigCompare()
compare.compare_types(type_file, test_file)
compare.pprint()
