from unittest import TestCase
from q2c.cmake_writer import CMakeWriter, CMakeFileAlreadyExistsError
import tempfile
import shutil
import os

class TestCMakeWriter(TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_cannot_write_if_cmakelists_already_exists(self):

        file = os.path.join(self.temp_dir, CMakeWriter.CMakeListsFileName)
        f = open(file, 'w')
        f.close()

        with self.assertRaises(CMakeFileAlreadyExistsError):
            CMakeWriter(self.temp_dir)

    def test_write_cmakelists(self):
        w = CMakeWriter()

        w.setCMakeMinimum("3.2.0")
        w.setProjectName("testProjectConversion")
        w.set_target_name("libXXX")
        w.add_var("src", "src/libXXX.h src/libXXX.cpp")
        w.add_library("${src}")
        w.add_include_path("src")
        w.add_define("LIBRARY_XXX")
        w.enable_qt_feature(auto_moc=True)

        w.add_find_packages("Qt5Core")
        w.target_link_libraries("Qt5::Core")

        w.write()

        print('done')



