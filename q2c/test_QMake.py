from unittest import TestCase
from decoder import QMake
__author__ = 'ddeda'
import tempfile
import shutil
import os
import re

class TestQMake(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_remove_antislash(self):
        str='''SUBDIRS +=\\
aaa\\
bbb'''
        print(str)
        str = str.replace("\\\n"," ")

        self.assertTrue(str =="SUBDIRS += aaa bbb",str)


    def test_regex(self):

        string = "SUBDIRS += aaa bbb"
        pattern = '^\s*(\w+)\s*([-+]?=)\s*(.*)$'

        matchObj  = re.match(pattern,string)

        self.assertTrue( matchObj.group(1) == "SUBDIRS")
        self.assertTrue( matchObj.group(2) == "+=")
        self.assertTrue( matchObj.group(3) == "aaa bbb")

    def test_fail_regex(self):

        string = "SUBDIRS "
        pattern = '^\s*(\w+)\s*([-+]?=)\s*(.*)$'

        matchObj  = re.match(pattern,string)
        self.assertIsNone(matchObj)

    def test_qmake_parser(self):

        str ='''
TEMPLATE=app
CONFIG+=c++11
TARGET=appli_coucou
SOURCES=aaa.h\\
bbb.h
'''
        os.path.join(self.temp_dir,"appli_coucou.pro")
        with f =

