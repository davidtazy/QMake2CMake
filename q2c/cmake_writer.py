import semver as sv
import os
import sys
import contextlib

@contextlib.contextmanager
def smart_open(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()

class Version:
    version = sv.VersionInfo(0, 0, 0, None, None)

    def __init__(self, version_str):
        parts = sv.parse(version_str)
        parts['prerelease'] = None
        parts['build'] = None

        maj = parts['major']

        self.version = sv.VersionInfo(
            parts['major'], parts['minor'], parts['patch'],
            parts['prerelease'], parts['build'])

    def toString(self):
        return sv.format_version(self.version.major, self.version.minor, self.version.patch)


class Var:
    name = ""
    value = ""

    def __init__(self, var, val):
        self.name = var
        self.value = val

    def toString(self):
        return "set({} {})\n".format(self.name, self.value)


class CMakeFileAlreadyExistsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CMakeWriter:

    CMakeListsFileName='CMakeLists.txt'

    def __init__(self, path = None):

        self.minimum = Version("3.0.0")
        self.project_name = ""
        self.vars = []
        self.cmakefile = None
        self.target_name="undef_target_name"
        self.add_binary= None
        self.target_sources=""
        self.link_libraries = []
        self.subdirectories =[]
        self.is_target_executable = False
        self.defines = []
        self.include_path=[]
        self.cpp11 = False
        self.enable_qt5_moc=False
        self.enable_qt5_uic=False
        self.enable_qt5_rcc =False
        self.std_out = False
        self.find_packages = []

        if path is not None:
            self.cmakefile = os.path.join(path, self.CMakeListsFileName)
            if os.path.isfile(self.cmakefile) is True:
                raise CMakeFileAlreadyExistsError("CmakeWriter.__init__({}) file already exists".format(self.cmakefile))
            #ensure target name using directory name
            if len(self.target_name) is 0:
                self.target_name = os.path.basename(path)

    def isSubDirProject(self):
        return self.add_binary is None

    def isLibOrAppProject(self):
        return self.add_binary is not None

    def setCMakeMinimum(self, minimum):
        self.cmake_minimum = Version(minimum)

    def setProjectName(self, project_name):
        self.project_name = project_name


    def add_find_packages(self,package):
        self.find_packages.append(package)

    def add_var(self, var, value):
        self.vars.append(Var(var, value))

    def set_target_name(self,name):
        self.target_name = name

    def add_executable(self,  sources):
        self.add_binary = "add_executable"
        self.target_sources = sources
        self.is_target_executable = True


    def add_library(self,sources):
        self.add_binary = "add_library"
        self.target_sources = sources

    def add_include_path(self, path):
        self.include_path.append(path)


    def add_subdirectory(self, dir):
        self.subdirectories.append(dir)


    def add_define(self,define):
        self.defines.append(define)

    def target_link_libraries(self,libraries):
        if isinstance(libraries, list) is True:
            for lib in libraries:
                self.link_libraries.append(lib)
        else:
            self.link_libraries.append(libraries)


    def enable_qt_feature(self,auto_moc=False,auto_ui=False, auto_rcc=False):
        self.enable_qt5_rcc = auto_rcc
        self.enable_qt5_moc = auto_moc
        self.enable_qt5_uic = auto_ui

    def enable_qt_auto_uic(self):
        self.enable_qt5_uic = True

    def enable_qt_auto_moc(self):
        self.enable_qt5_moc = True

    def enable_qt_auto_rcc(self):
        self.enable_qt5_rcc = True

    def enable_cpp11(self):
        self.cpp11 = True

    def write(self):

        with smart_open(self.cmakefile) as f:

            f.writelines("cmake_minimum_required(VERSION {} )\n".format(self.minimum.toString()))
            if len(self.project_name) > 0:
                f.writelines("project({})\n".format(self.project_name))

            if self.enable_qt5_rcc or  self.enable_qt5_moc or  self.enable_qt5_uic:
                f.writelines("set(CMAKE_INCLUDE_CURRENT_DIR ON)\n")

            if self.enable_qt5_rcc :
                f.writelines("set(CMAKE_AUTORCC ON)\n")

            if   self.enable_qt5_uic:
                f.writelines("set(CMAKE_AUTOUIC ON)\n")

            if  self.enable_qt5_moc :
                f.writelines("set(CMAKE_AUTOMOC ON)\n")

            for package in self.find_packages:
                f.writelines(("find_package({})\n").format(package))

            #cpp11
            if self.cpp11 is True:
                f.writelines("set(CMAKE_CXX_STANDARD 11)\n")
                f.writelines("set(CMAKE_CXX_STANDARD_REQUIRED ON)\n")

            for v in self.vars:
                f.writelines(v.toString())

            #add_library or add_executable
            if self.isLibOrAppProject():
                f.writelines("{}({} {})\n".format(self.add_binary,self.target_name,self.target_sources))

            #link
            if len(self.link_libraries) > 0:
                f.writelines("target_link_libraries({} PRIVATE {})\n".format(self.target_name," ".join(self.link_libraries)))

            #include path
            for include in self.include_path:
                f.writelines('target_include_directories(%s PUBLIC  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/%s> $<INSTALL_INTERFACE:%s>)\n'%(self.target_name,include,include))

            #defines
            for define in self.defines:
                f.writelines("target_compile_definitions({} PRIVATE  {})\n"
                             .format(self.target_name,define))
            if self.isLibOrAppProject():
                f.writelines('set_target_properties({} PROPERTIES DEBUG_POSTFIX "d")\n'.format(self.target_name))

            #install
            if self.isLibOrAppProject():
                dest = "Libs"
                if self.is_target_executable:
                    dest = "Bin"
                f.writelines("install(TARGETS {} DESTINATION {})\n".format(self.target_name,dest))

            # add subdir
            for subdir in self.subdirectories:
                f.writelines("add_subdirectory({})\n".format(subdir))

        return self.cmakefile