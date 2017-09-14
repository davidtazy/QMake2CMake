from unittest import TestCase
from q2c.config_visitor import ConfigVisitor

class MocCMakeWriter:
    def __init__(self):
        self.arg = None
        self.call_count = 0
        self.cpp11_call_count = 0

    def target_link_libraries(self,libraries):
        self.arg = libraries
        self.call_count += 1

    def enable_cpp11(self):
        self.cpp11_call_count += 1

class TestConfigVisitor(TestCase):
    dico = {'libABC': {'function': 'target_link_libraries', 'arg': 'ABC'},
            'libDEF': {'function': 'target_link_libraries_not_defined', 'arg': 'ABC'},
            'libGHI': { 'arg': 'ABC'},
            'weird_config': {'function': 'enable_cpp11'}}

    def test_visit_target_link_libraries_well_defined(self):

        cv  = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        cv.visit(moc,'libABC')

        self.assertTrue(moc.call_count == 1)
        self.assertEqual(moc.arg, 'ABC')

    def test_config_string_not_defined_in_visitor(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        cv.visit(moc, 'libNotInDico')
        self.assertTrue(moc.call_count == 0)

    def test_cmake_writer_function_does_not_exists(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        with self.assertRaises(AttributeError):
            cv.visit(moc, 'libDEF')

    def test_cmake_writer_no_function_attributes(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()

        with self.assertRaises(ValueError):
            cv.visit(moc, 'libGHI')

    def test_cmake_writer_function_with_no_args(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()

        cv.visit(moc, 'weird_config')
        self.assertTrue(moc.cpp11_call_count == 1)
