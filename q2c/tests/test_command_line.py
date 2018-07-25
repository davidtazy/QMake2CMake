from unittest import TestCase
from q2c.command_line import get_pro_file_from_path,dict_from_json_file,get_all_pro_files_from_dir_tree,TryConvert,main,create_parser
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

    def test_parser_with_no_args_fails_with_system_exit(self):

        parser = create_parser()
        self.assertIsNotNone(parser)
        with self.assertRaises(SystemExit):
            parser.parse_args([])

    def test_parser_with_all_options_set(self):

        parser = create_parser()
        self.assertIsNotNone(parser)

        args =  parser.parse_args(["-n","-r","-s","-c", "file.json","."])

        self.assertTrue(args.recursive)
        self.assertTrue(args.dry_run)
        self.assertTrue(args.show)
        self.assertEqual(args.config,"file.json" )
        self.assertEqual(args.path,".")



    def test_main_file(self):

        self.create_pro_file("proj.pro")
        main(recursive=False,
             show=False,
             dry_run=False,
             config=None,
             path=self.temp_dir,
             wait_for_key_pressed_method=None,
             show_file_method=None)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "CMakeLists.txt")))


    def test_main_dir_and_recursive(self):

        class Functor(object):
            def __init__(self):
                self._was_called = False

            # This construct allows objects to be called as functions in python
            def __call__(self, x):
                self._was_called = True

            def was_called(self):
                return self._was_called

        func_input = Functor()
        func_show_file = Functor()

        self.create_pro_file("proj.pro")
        main(recursive=True,
             show=True,
             dry_run=False,
             config=None,
             path=self.temp_dir,
             wait_for_key_pressed_method=func_input,
             show_file_method=func_show_file)
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, "CMakeLists.txt")))
        self.assertTrue(func_input.was_called())
        self.assertTrue(func_show_file.was_called())

