import re

class QMake:
    DESTDIR = "";
    CONFIG = {"qt" , "warn_on" , "release" , "incremental" , "link_prl"}
    QT = { "core" , "gui"}
    DEFINES =[]
    SOURCES =[]
    HEADERS =[]
    FORMS =[]
    DISTFILES =[]
    INCLUDEPATH =[]
    LIBS =[]
    RESOURCES =[]
    SUBDIRS =[]
    TARGET = ""
    TEMPLATE =["app"]
    TRANSLATIONS =[]
    need_moc = False


    def parse(self,pro_file):
        work = ""
        with open(pro_file, 'r') as f:
            work = f.read()

        #simple hack to variable lists
        work = work.replace("\\\n"," ")

        lines = work.split('\n')

        pattern = '^\s*(\w+)\s*([-+]?=)\s*(.*)$'

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
                    op=0
                    if matchObj.group(2) == "-=":
                        op = -1;
                    elif matchObj.group(2) == "+=":
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

                    if sl is not none:
                        self.operateOnVar(sl,op,matchObj.group(3));

    def operateOnVar(self,sl,op,val):
        sl.append(val)


    """
    bool Converter::parseProFile(QString proFile)
{
    QFile file(proFile);
    QStringList lines;
    QString work;
    QRegExp liner("^\\s*(\\w+)\\s*([-+]?=)\\s*(.*)$",Qt::CaseInsensitive,QRegExp::RegExp2);
    int op; QStringList *sl;

    if(file.open(QIODevice::ReadOnly))
    {
        work = file.readAll();
        file.close();
        qDebug()<< "parsing QMake file:" << proFile.section('/',-1);
        // make multilines simple
        work.remove("\\\n");
        // get the lines
        lines = work.split('\n',QString::SkipEmptyParts);

        initQMakeVars();
        // now parse the lines ...
        while(lines.count())
        {
            // capture all the contents...
            lines.first().indexOf(liner);
            // cap(1) is the variable, cap(2) is the operator
            if(liner.numCaptures() > 0)
            {
                if(liner.cap(1) == "TEMPLATE")
                {
                    TEMPLATE = liner.cap(3);
                }
                else if(liner.cap(1) == "TARGET")
                {
                    TARGET = liner.cap(3);
                }
                else if(liner.cap(1) == "DESTDIR")
                {
                    DESTDIR = liner.cap(3);
                }
                else
                {
                    sl = 0;
                    if(liner.cap(2) == "-=") {
                        op = -1;
                    } else if(liner.cap(2) == "+=") {
                        op = +1;
                    } else op = 0;

                    if(liner.cap(1) == "CONFIG")
                        sl = &CONFIG;
                    else if(liner.cap(1) == "QT")
                        sl = &QT;
                    else if(liner.cap(1) == "DEFINES")
                        sl = &DEFINES;
                    else if(liner.cap(1) == "SOURCES")
                        sl = &SOURCES;
                    else if(liner.cap(1) == "HEADERS")
                        sl = &HEADERS;
                    else if(liner.cap(1) == "FORMS")
                        sl = &FORMS;
                    else if(liner.cap(1) == "DISTFILES")
                        sl = &DISTFILES;
                    else if(liner.cap(1) == "INCLUDEPATH")
                        sl = &INCLUDEPATH;
                    else if(liner.cap(1) == "LIBS")
                        sl = &LIBS;
                    else if(liner.cap(1) == "RESOURCES")
                        sl = &RESOURCES;
                    else if(liner.cap(1) == "SUBDIRS")
                        sl = &SUBDIRS;
                    else if(liner.cap(1) == "TRANSLATIONS")
                        sl = &TRANSLATIONS;

                    if(sl) operateOnVar(sl,op,liner.cap(3));
                }
            }
            else    // nothing captured with our regex - parsing the line needed!
            {
                //TODO: write something complicated here ...
            }
            lines.takeFirst();  //just that the loop won't be infinite...
        }
        if(TEMPLATE.isEmpty()) TEMPLATE = "app";
        qDebug()<<"CONFIG:"<<CONFIG;
        qDebug()<<"QT:"<<QT;
        qDebug()<<"DEFINES:"<<DEFINES;
        qDebug()<<"DISTFILES:"<<DISTFILES;
        qDebug()<<"LIBS:"<<LIBS;
        qDebug()<<"SUBDIRS:"<<SUBDIRS;
        qDebug()<<"INCLUDEPATH:"<<INCLUDEPATH;
        qDebug()<<"TEMPLATE:"<<TEMPLATE<<", TARGET:"<<TARGET<<", DESTDIR:"<<DESTDIR;
    } else return false;
    return true;
}"""


