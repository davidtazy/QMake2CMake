from unittest import TestCase
from .qmake_to_cmake import QMakeToCMake

from .qmake_parser import  QMakeParser
from .cmake_writer import  CMakeWriter
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


