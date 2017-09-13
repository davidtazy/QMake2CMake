from qmake_parser import QMakeParser
from cmake_writer import CMakeWriter
import os


class QMakeToCMake:
    Modules = ['Core', 'Widgets', 'Gui', 'Network', 'Sql', 'Multimedia', 'WebKit', 'Svg', 'OpenGL', 'PrintSupport',
               'Script', 'Xml', 'XmlPatterns', 'Qml', 'Positioning', 'Quick', 'Sensors', 'Sql', 'Declarative']
    LowerCaseModules = ['core', 'widgets', 'gui', 'network', 'sql', 'multimedia', 'webkit', 'svg', 'opengl',
                        'printsupport', 'script', 'xml', 'xmlPatterns', 'qml', 'positioning', 'quick', 'sensors', 'sql',
                        'declarative']

    def __init__(self):
        self.config_function = None
        self.cmakefile = None

    def register_config_function(self, function):
        self.config_function = function

    @staticmethod
    def ToQtModule(module):

        l_module = module.lower()
        if l_module not in QMakeToCMake.LowerCaseModules:
            return None

        return QMakeToCMake.Modules[QMakeToCMake.LowerCaseModules.index(l_module)]

    def convert(self, pro_file):
        qmake = QMakeParser()
        cmake = CMakeWriter(os.path.dirname(pro_file))
        self._do_convert(pro_file, qmake, cmake)

    def convertToStdOut(self, pro_file):
        qmake = QMakeParser()
        cmake = CMakeWriter()
        self._do_convert(pro_file, qmake, cmake)

    def _do_convert(self, pro_file, qmake, cmake):
        qmake.parse(pro_file)

        if qmake.isSubdirsProject():
            self.create_subdir_project(qmake, cmake)
        else:
            self.create_project(qmake, cmake)

    def create_subdir_project(self, qmake, cmake):
        print ('create subdir_project')

        cmake.setProjectName(qmake.PRO_FILE)

        for subdir in qmake.SUBDIRS:
            cmake.add_subdirectory(subdir)

        self.cmakefile = cmake.write()
        print('----------------\nsubdir created')

    def create_project(self, qmake, cmake):
        print ('create project')
        cmake.setProjectName(qmake.PRO_FILE)
        cmake.set_target_name(qmake.TARGET)

        depends_files = []

        if len(qmake.SOURCES):
            cmake.add_var("src", '\n\t'.join(qmake.SOURCES))
            depends_files.append('${src}')

        if len(qmake.HEADERS):
            cmake.add_var("headers", '\n\t'.join(qmake.HEADERS))
            depends_files.append('${headers}')

        if len(qmake.RESOURCES):
            cmake.add_var("resources", '\n\t'.join(qmake.RESOURCES))
            depends_files.append('${resources}')
            cmake.enable_qt_auto_rcc()

        if len(qmake.FORMS):
            cmake.add_var("forms", '\n\t'.join(qmake.FORMS))
            depends_files.append('${forms}')
            cmake.enable_qt_auto_uic()

        # todo  should parse .h and .cpp file to find for Q_OBJECT class
        if "core" in qmake.QT:
            cmake.enable_qt_auto_moc()

        if qmake.isTemplateLib():
            cmake.add_library(" ".join(depends_files))
        elif qmake.isTemplateApp():
            cmake.add_executable(" ".join(depends_files))

        #####Qtlib
        for qt_module in qmake.QT:
            cmake_module = self.ToQtModule(qt_module)
            if cmake_module:
                cmake.add_find_packages('Qt5%s' % (cmake_module))
                cmake.target_link_libraries('Qt5::%s' % (cmake_module))

        ### include path
        for include_path in qmake.INCLUDEPATH:
            cmake.add_include_path(include_path)

        ###defines
        for define in qmake.DEFINES:
            cmake.add_define(define)

        ### c++11 enabler
        if 'c++11' in qmake.CONFIG:
            cmake.enable_cpp11()

        # customize
        if self.config_function is not None:
            for config in qmake.CONFIG:
                self.config_function(cmake, qmake.CONFIG)

        self.cmakefile =cmake.write()
        print('----------------\nproject created')

    def get_cmakefile(self):
        return self.cmakefile

def get_pro_file_from_path(dir):

    if os.path.isfile(dir) and (dir.endswith(".pro") or dir.endswith(".pri")):
        return dir
    if os.path.isdir(dir) is False:
        raise ValueError('%s is not a directory'%(dir))

    candidates = []
    for file in os.listdir(dir):
        if file.endswith(".pro"):
            candidates.append(os.path.join(dir, file))

    if len(candidates) is 0:
        raise ValueError('%s does not contains .pro file' % (dir))

    if len(candidates) > 1:
        raise ValueError('%s does contains severals .pro file %s' % (dir, ' '.join(candidates)))

    return candidates[0]


import argparse
import webbrowser


def TryConvert(args):
    converter = QMakeToCMake()
    pro_file = get_pro_file_from_path(args.path)
    if args.dry_run is True:
        converter.convertToStdOut(pro_file)
    else:
        converter.convert(pro_file)
        if args.show:
            webbrowser.open_new_tab(pro_file)
            webbrowser.open_new_tab(converter.get_cmakefile())


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="directory or file")

    parser.add_argument('-n','--dry-run', help="print cmakelist.txt on the console",
                        action="store_true")

    parser.add_argument('-r', '--recursive', help="walk all subdirectories",
                        action="store_true")

    parser.add_argument('-s','--show',help="show result file(s)",
                        action="store_true")

    args = parser.parse_args()

    if args.recursive is False:
        TryConvert(args)
    else:
        #recursive mode
        print("recursive mode ")

        pro_files = []
        for dirpath, subdirs, files in os.walk(args.path):
            for x in files:
                if x.endswith(".pro"):
                    pro_files.append(os.path.join(dirpath, x))
                    break

        for pro_file in pro_files:
            print("start %s conversion\n"%(pro_file))
            args.path = pro_file
            TryConvert(args)
            if args.show is True:
               raw_input("press enter to continue")


