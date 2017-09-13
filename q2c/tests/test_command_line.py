from unittest import TestCase
from q2c.command_line import get_pro_file_from_path
import tempfile
import shutil
import os

class TestCommandLine(TestCase):


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