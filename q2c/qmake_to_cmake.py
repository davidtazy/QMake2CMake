from .qmake_parser import QMakeParser
from .cmake_writer import CMakeWriter
import os


class QMakeToCMake:
    Modules = ['Core', 'Widgets', 'Gui', 'Network', 'Sql', 'Multimedia', 'WebKit', 'Svg', 'OpenGL', 'PrintSupport',
               'Script', 'Xml', 'XmlPatterns', 'Qml', 'Positioning', 'Quick', 'Sensors', 'Sql', 'Declarative','Test']
    LowerCaseModules = ['core', 'widgets', 'gui', 'network', 'sql', 'multimedia', 'webkit', 'svg', 'opengl',
                        'printsupport', 'script', 'xml', 'xmlPatterns', 'qml', 'positioning', 'quick', 'sensors', 'sql',
                        'declarative','testlib']

    def __init__(self):
        self.config_visitor = None
        self.cmakefile = None

    def register_config_visitor(self, config_visitor):
        self.config_visitor = config_visitor

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
        self.customize(self.config_visitor, qmake, cmake)

        self.cmakefile =cmake.write()
        print('----------------\nproject created')

    def get_cmakefile(self):
        return self.cmakefile

    @staticmethod
    def customize(config_visitor, qmake, cmake):
        if config_visitor is not None:
            for config in qmake.CONFIG:
                config_visitor.visit(cmake, 'CONFIG', config)
            for var in qmake.user_variables_dict:
                for val in qmake.user_variables_dict[var]:
                    config_visitor.visit(cmake, var, val)


