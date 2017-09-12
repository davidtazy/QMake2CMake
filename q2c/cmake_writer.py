import semver as sv
import os


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


class CMakeWriter:
    CMakeListsFileName='CMakeLists.txt'

    minimum = Version("3.0.0")
    project_name = ""
    vars = []
    cmakefile = ""
    target_name=""
    add_binary="add_library_executable"
    target_sources=""
    link_libraries = []
    is_target_executable = False
    defines = []
    include_path=[]
    cpp11 = False

    enable_qt5_moc=False
    enable_qt5_uic=False
    enable_qt5_rcc =False


    find_packages = []

    def __init__(self, path):
        self.cmakefile = os.path.join(path, self.CMakeListsFileName)
        if os.path.isfile(self.cmakefile) is True:
            raise ValueError("CmakeWriter.__init__({}) file already exists".format(self.cmakefile))

        #ensure target name using directory name
        if len(self.target_name) is 0:
            self.target_name = os.path.basename(path)

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

    def write(self):

        f = open(self.cmakefile, 'w')

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

        f.writelines('set_target_properties({} PROPERTIES DEBUG_POSTFIX "d")\n'.format(self.target_name))

        #install
        dest = "Libs"
        if self.is_target_executable:
            des = "Bin"
        f.writelines("install(TARGETS {} DESTINATION {})\n".format(self.target_name,dest))


        f.close()
