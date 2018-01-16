

import re
import os

class QMakeParser:

    def __init__(self):
        self.DESTDIR = ""
        self.CONFIG = ["qt" , "warn_on" , "release" , "incremental" , "link_prl"]
        self.QT = [ "core" , "gui"]
        self.DEFINES =[]
        self.SOURCES =[]
        self.HEADERS =[]
        self.FORMS =[]
        self.DISTFILES =[]
        self.INCLUDEPATH =[]
        self.LIBS =[]
        self.RESOURCES =[]
        self.SUBDIRS =[]
        self.PRO_FILE = ""
        self.TARGET = ""
        self.TEMPLATE =["app"]
        self.TRANSLATIONS =[]
        self.need_moc = False
        self.user_variables_dict = dict()

    def isSubdirsProject(self):
        return self.TEMPLATE == "subdirs"

    def isTemplateLib(self):
        return self.TEMPLATE == "lib"

    def isTemplateApp(self):
        return self.TEMPLATE == "app"

    def parse(self,pro_file):

        self.PRO_FILE = os.path.basename(pro_file).split('.')[0]

        work = ""
        with open(pro_file, 'r') as f:
            work = f.read()

        #simple hack to variable lists
        work = work.replace("\\\n"," ")

        lines = work.split('\n')

        pattern = '^\s*(\w+)\s*([-+*]?=)\s*(.*)$'

        for line in lines:
            if len(line) is 0:
                continue
            matchObj  = re.match(pattern,line)

            if (matchObj is not None) and (matchObj.lastindex == 3):
                if matchObj.group(1) == "TEMPLATE":
                    self.TEMPLATE = matchObj.group(3)
                elif matchObj.group(1) == "TARGET":
                    self.TARGET = matchObj.group(3)

                elif matchObj.group(1) == "DESTDIR":
                    self.DESTDIR = matchObj.group(3);

                else:
                    sl = None
                    op = 0
                    if matchObj.group(2) == "-=":
                        op = -1;
                    elif matchObj.group(2) == "+=" or matchObj.group(2) == "*=":
                        op = +1
                    else:
                        op = 0


                    if matchObj.group(1) == "CONFIG":
                        sl = self.CONFIG
                    elif matchObj.group(1) == "QT":
                        sl = self.QT
                    elif matchObj.group(1) == "DEFINES":
                        sl = self.DEFINES
                    elif matchObj.group(1) == "SOURCES":
                        sl = self.SOURCES
                    elif matchObj.group(1) == "HEADERS":
                        sl = self.HEADERS
                    elif matchObj.group(1) == "FORMS":
                        sl = self.FORMS
                    elif matchObj.group(1) == "DISTFILES":
                        sl = self.DISTFILES
                    elif matchObj.group(1) == "INCLUDEPATH":
                        sl = self.INCLUDEPATH
                    elif matchObj.group(1) == "LIBS":
                        sl = self.LIBS
                    elif matchObj.group(1) == "RESOURCES":
                        sl = self.RESOURCES
                    elif matchObj.group(1) == "SUBDIRS":
                        sl = self.SUBDIRS
                    elif matchObj.group(1) == "TRANSLATIONS":
                        sl = self.TRANSLATIONS
                    else:
                        self.addUserVariable(matchObj.group(1),op, matchObj.group(3))

                    if sl is not None:
                        self.operateOnVar(sl, op, matchObj.group(3) );

        if 'qt' not in self.CONFIG:
            self.QT = []
        else:
            #remove duplicates
            self.QT = list(set(self.QT))


    def operateOnVar(self,sl,op,val):
        values = val.split()

        if op is -1:
            for val in values:
                if val in sl:
                    sl.remove(val)
        elif op is 0:
            while len(sl) > 0:
                del(sl[0])
            for val in values:
                sl.append(val)
        else:
            for val in values:
                sl.append(val)

    def addUserVariable(self,var_name,op,values ):
        if var_name not in self.user_variables_dict:
            self.user_variables_dict[var_name] = []
        self.operateOnVar(self.user_variables_dict[var_name],op,values)





