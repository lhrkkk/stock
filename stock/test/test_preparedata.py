#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

"""
Usage:

    tmpelate.py  [-q | --quiet] [-l | --log] [-d | --debug]
    tmpelate.py (-h | --help)
    tmpelate.py --version

Options:
    -h --help     Show this screen.
    --version     Show version.
    -l --log      Logging in makemd.log file.
    -q --quiet    Quiet output.
    -d --debug    Debug output.

Notes:
   my tmpelate
"""

import unittest
# from labkit.common import reflection, smartlog
from stock import origin_data

class TestPreparedata(unittest.TestCase):

    def setUp(self):
        pass
        # 测试pep_from_seq & encoding
        # 以及load
        # todo: config 的namespace的问题.
        # self.logger=smartlog.get_logger(level="DEBUG")


    def tearDown(self):
        pass
        # smartlog.clear_logger(self.logger)

    def test_get(self):
        pass




if __name__ == '__main__':
    unittest.main()


