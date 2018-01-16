from unittest import TestCase
from q2c.config_visitor import ConfigVisitor
from q2c.qmake_to_cmake import QMakeToCMake
from q2c.qmake_parser import  QMakeParser
from q2c.cmake_writer import  CMakeWriter


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
    dico = dict(CONFIG={'libABC': {'function': 'target_link_libraries', 'arg': 'ABC'},
                        'libDEF': {'function': 'target_link_libraries_not_defined', 'arg': 'ABC'},
                        'libGHI': {'arg': 'ABC'},
                        'weird_config': {'function': 'enable_cpp11'}
                        }, MY_VAR={'libKLM': {'function': 'target_link_libraries', 'arg': 'KLM'}})

    def test_visit_target_link_libraries_well_defined(self):

        cv  = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        cv.visit(moc,'CONFIG','libABC')

        self.assertTrue(moc.call_count == 1)
        self.assertEqual(moc.arg, 'ABC')

    def test_visit_target_link_libraries_from_my_variable(self):

        cv  = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        cv.visit(moc,'MY_VAR','libKLM')

        self.assertTrue(moc.call_count == 1)
        self.assertEqual(moc.arg, 'KLM')

    def test_config_string_not_defined_in_visitor(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        cv.visit(moc, 'CONFIG','libNotInDico')
        self.assertTrue(moc.call_count == 0)

    def test_cmake_writer_function_does_not_exists(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()
        with self.assertRaises(AttributeError):
            cv.visit(moc,'CONFIG', 'libDEF')

    def test_cmake_writer_no_function_attributes(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()

        with self.assertRaises(ValueError):
            cv.visit(moc, 'CONFIG','libGHI')

    def test_cmake_writer_function_with_no_args(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()

        cv.visit(moc, 'CONFIG', 'weird_config')
        self.assertTrue(moc.cpp11_call_count == 1)

    def test_qmake_variable_not_in_dico(self):
        cv = ConfigVisitor(self.dico)
        moc = MocCMakeWriter()

        cv.visit(moc, 'QMAKE_VARIABLE_NOT_IN_DICO', 'weird_config')
        self.assertTrue(moc.cpp11_call_count == 0)
        self.assertTrue(moc.call_count == 0)

    def test_customize_cmake(self):
        qmake = QMakeParser()
        qmake.CONFIG=['libABC']
        qmake.user_variables_dict = {'MY_VAR': ['libKLM', 'DEF'], 'MY_SECOND_VAR': ['GHI']}

        cmake = MocCMakeWriter()
        cv = ConfigVisitor(self.dico)
        QMakeToCMake.customize(cv, qmake, cmake)

        self.assertEqual(cmake.call_count,2)


