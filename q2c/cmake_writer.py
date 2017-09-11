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
        return "set({} {}".format(self.name, self.value)


class CMakeWriter:
    CMakeListsFileName='CMakeLists.txt'

    minimum = Version("3.0.0")
    project_name = ""
    vars = []
    cmakefile = ""

    def __init__(self, path):
        self.cmakefile = os.path.join(path, self.CMakeListsFileName)
        if os.path.isfile(self.cmakefile) is True:
            raise ValueError("CmakeWriter.__init__({}) file already exists".format(self.cmakefile))

    def setCMakeMinimum(self, minimum):
        self.cmake_minimum = Version(minimum)

    def setProjectName(self, project_name):
        self.project_name = project_name

    def setVar(self, var, value):
        self.vars.append(Var(var, value))

    def write(self):

        f = open(self.cmakefile, 'w')

        f.writelines("cmake_minimum_required(VERSION {} )\n".format(self.minimum.toString()))
        if len(self.project_name) > 0:
            f.writelines("project({})\n".format(self.project_name))
        f.close()
