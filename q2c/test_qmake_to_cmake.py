from unittest import TestCase
import tempfile
import shutil
import os
from qmake_to_cmake import QMakeToCMake,get_pro_file_from_path
from qmake_parser import  QMakeParser
from cmake_writer import  CMakeWriter
__author__ = 'ddeda'


class TestQMakeToCMake(TestCase):

    def test_create_subdir_project(self):
        conv = QMakeToCMake()
        qmake = QMakeParser()
        cmake = CMakeWriter()

        qmake.QT = []
        qmake.TEMPLATE = 'subdirs'
        qmake.PRO_FILE = "common"
        qmake.SUBDIRS=['libA','libB']


        conv.create_subdir_project(qmake, cmake)


    def test_create_binary_project(self):
        conv = QMakeToCMake()
        qmake = QMakeParser()
        cmake = CMakeWriter()


        qmake.TEMPLATE = 'lib'
        qmake.PRO_FILE = "libToto"
        qmake.TARGET = "Toto"
        qmake.SOURCES = ["a.cpp","b.cpp","c.cpp"]
        qmake.HEADERS = ["a.h","b.h","c.h"]
        qmake.FORMS = ["a.ui"]
        qmake.RESOURCES = ["r.qrc"]
        conv.create_project(qmake,cmake)

    def test_QtLib(self):

        self.assertEqual(QMakeToCMake.ToQtModule('core'),'Core')
        self.assertEqual(QMakeToCMake.ToQtModule('printsupport'),'PrintSupport')
        self.assertIsNone(QMakeToCMake.ToQtModule('not_qt_module'))

    def test_get_pro_file_from_path(self):
        temp_dir = tempfile.mkdtemp()

        with self.assertRaises(ValueError):
            get_pro_file_from_path(temp_dir)

        #create .pro file
        open(os.path.join(temp_dir,"project.pro"), 'a').close()

        pro_file = get_pro_file_from_path(temp_dir)
        self.assertTrue(pro_file.endswith("project.pro"))

        #create second .pro file
        open(os.path.join(temp_dir, "second_project.pro"), 'a').close()

        # dir with more than 1 pro file fails
        with self.assertRaises(ValueError):
            get_pro_file_from_path(temp_dir)

        # define exact  .pro file succeed
        pro_file = get_pro_file_from_path(os.path.join(temp_dir, "second_project.pro"))
        self.assertTrue(pro_file.endswith("second_project.pro"))

        # create.pri file
        open(os.path.join(temp_dir, "third_project.pri"), 'a').close()

        # define exact  .pri file succeed
        pro_file = get_pro_file_from_path(os.path.join(temp_dir, "third_project.pri"))
        self.assertTrue(pro_file.endswith("third_project.pri"))

        shutil.rmtree(temp_dir)
