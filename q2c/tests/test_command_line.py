from unittest import TestCase
from q2c.command_line import get_pro_file_from_path,dict_from_json_file,get_all_pro_files_from_dir_tree,TryConvert
import tempfile
import shutil
import os
import json

class TestCommandLine(TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.json_file = os.path.join(self.temp_dir, "good_file.json")
        self.dico = {'libABC': {'function': 'target_link_libraries', 'arg': 'ABC'},
                'libDEF': {'function': 'target_link_libraries_not_defined', 'arg': 'ABC'},
                'libGHI': {'arg': 'ABC'},
                'weird_config': {'function': 'enable_cpp11'}}

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_get_pro_file_from_path(self):

        with self.assertRaises(ValueError):
            get_pro_file_from_path(self.temp_dir)

        #create .pro file
        open(os.path.join(self.temp_dir,"project.pro"), 'a').close()

        pro_file = get_pro_file_from_path(self.temp_dir)
        self.assertTrue(pro_file.endswith("project.pro"))

        #create second .pro file
        open(os.path.join(self.temp_dir, "second_project.pro"), 'a').close()

        # dir with more than 1 pro file fails
        with self.assertRaises(ValueError):
            get_pro_file_from_path(self.temp_dir)

        # define exact  .pro file succeed
        pro_file = get_pro_file_from_path(os.path.join(self.temp_dir, "second_project.pro"))
        self.assertTrue(pro_file.endswith("second_project.pro"))

        # create.pri file
        open(os.path.join(self.temp_dir, "third_project.pri"), 'a').close()

        # define exact  .pri file succeed
        pro_file = get_pro_file_from_path(os.path.join(self.temp_dir, "third_project.pri"))
        self.assertTrue(pro_file.endswith("third_project.pri"))




    def test_dict_from_json_file(self):

        with open(self.json_file, 'w') as outfile:
            json.dump(self.dico, outfile)

        retrieved_dico =  dict_from_json_file(self.json_file)
        self.assertDictEqual(self.dico, retrieved_dico)

    def test_dict_from_json_file_raise_exception_if_malformed_file(self):

        with open(self.json_file, 'w') as outfile:
            json.dump(self.dico, outfile)

        #remove first line from file
        self.remove_first_line_from_file()

        with self.assertRaises(ValueError): 
            dict_from_json_file(self.json_file)

    def remove_first_line_from_file(self):
        with open(self.json_file, 'r+') as outfile:
            d = outfile.readlines()
            outfile.seek(0)

            line = 0
            for i in d:
                if line != 0:
                    outfile.write(i)
            outfile.truncate()

    @staticmethod
    def touch( file):
        open(file , 'a').close()

    def test_get_all_pro_files_from_dir_tree(self):
        dir1 = os.path.join(self.temp_dir,'dir_1')
        os.mkdir(dir1)

        self.touch(os.path.join(self.temp_dir, 'root.pro'))
        self.touch(os.path.join(dir1,'truc.pro'))
        self.touch(os.path.join(dir1, 'bidule.txt'))

        files = get_all_pro_files_from_dir_tree(self.temp_dir)

        self.assertTrue(len(files) == 2)

    def test_try_convert_an_empty_dir_thow_exception(self):
        with self.assertRaises(ValueError):
            TryConvert(self.temp_dir,dry_run=False, show=False,config=None)


    def create_pro_file(self,filename):
        str = '''
                TEMPLATE=app
                CONFIG+=c++11
                CONFIG -= qt
                TARGET=appli_coucou
                SOURCES=aaa.h\\
                bbb.h
                '''
        pro_file = os.path.join(self.temp_dir, filename)
        with open(pro_file,'w') as f:
            f.write(str)


    def test_try_convert_generate_cmakefile(self):

        self.create_pro_file("proj.pro")

        TryConvert(self.temp_dir,dry_run=False, show=False,config=None)

        self.assertTrue(os.path.exists(os.path.join(self.temp_dir,"CMakeLists.txt")))

    def test_try_convert_dry_run_does_not_create_cmakefile(self):

        self.create_pro_file("proj.pro")

        TryConvert(self.temp_dir,dry_run=True, show=False,config=None)

        self.assertFalse( os.path.exists(os.path.join(self.temp_dir,"CMakeLists.txt")))




