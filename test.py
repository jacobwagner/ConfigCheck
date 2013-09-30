#!/usr/bin/python

import os
from lib.ConfigCheck import ConfigCheck

type_file = os.path.join(os.path.dirname(__file__), 'test/configs', 'types.cfg')
test_file = os.path.join(os.path.dirname(__file__), 'test/configs', 'test.cfg')

compare = ConfigCheck()
compare.compare_types(type_file, test_file)
print "Type Compare:"
compare.pprint()


test2_file = os.path.join(os.path.dirname(__file__), 'test/configs', 'test2.cfg')
compare2 = ConfigCheck()
compare2.compare_values(test_file, test2_file)
print "Value Compare:"
compare2.pprint()
