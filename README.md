# QMakeToCMake [![Build Status](https://travis-ci.org/davidtazy/QMakeToCMake.svg?branch=master)](https://travis-ci.org/davidtazy/QMakeToCMake) [![Coverage Status](https://coveralls.io/repos/github/davidtazy/QMakeToCMake/badge.svg)](https://coveralls.io/github/davidtazy/QMakeToCMake)
Helper script to move qmake (Qt5) based subdirs/project to cmake

Warning: its not bullet proof, 
main goal is too speed up manual operation 

will be usefull if lots of pro file to convert

# Features:
- TEMPLATE=subdirs,  you may need to re-order add_subdirectoies lines
- TEMPLATE=app 
- TEMPLATE=lib
- TARGET will name the target 
- QT, will add find-packages, target_link_libraries for defined modules
- CMAKE_AUTO_RCC if qrc file defined
- CMAKE_AUTO_uic if .ui files defined
- CMAKE_AUTO_MOC if depends on Qt5Core

- if CONFIG contains c++11, wil add magic lines to enable it on CMakeLists.txt
- CONFIG-=qt , no Qt dependencies
- DEFINES
- INCLUDEPATH
- CONFIG values and custom variable can define new lines on cmakelist.txt with a json config file (see [example/config.json](example/config.json))
- 
# Examples

libToto.pro:
```
TEMPLATE=lib
QT += core gui
CONFIG+=c++11
TARGET=Toto
SOURCES=aaa.cpp\
  bbb.cpp\
  ccc.cpp
HEADERS=aaa.h\
  bbb.h\
  ccc.h
FORMS=a.ui
RESOURCES=r.qrc
```
CMakeLists.txt
```
make_minimum_required(VERSION 3.0.0 )
project(libToto)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
find_package(Qt5Core)
find_package(Qt5Gui)
set(src a.cpp
        b.cpp
        c.cpp)
set(headers a.h
        b.h
        c.h)
set(resources r.qrc)
set(forms a.ui)
add_library(Toto ${src} ${headers} ${resources} ${forms})
target_link_libraries(Toto PRIVATE Qt5::Core Qt5::Gui)
set_target_properties(Toto PROPERTIES DEBUG_POSTFIX "d")
install(TARGETS Toto DESTINATION Libs)
```
# Limitations

```
q2c does not read correctly conditionnal blocks:
CONTAINS(CONFIG,featureXXX): QT+= printsupport
will be omited during parse

CONTAINS(CONFIG,featureXXX){
blockIf
}else{
blockElse
}
blockIf AND blockElse will be parsed 
```

# Usage:

download or clone
```
cd to QMakeToCMake

pip install .
# will install commandline app named 'q2c'

usage: q2c [-h] [-n] [-r] [-s] [-c] path

positional arguments:
  path             directory or file

optional arguments:
  -h, --help       show this help message and exit
  -n, --dry-run    print conversion on the console
  -r, --recursive  all .pro in directory tree
  -s, --show       show result file(s) , use it with recursive option to survey operations
  -s, --config     json file defining dictionnary between CONFIG values in .pro file and cmake function
```
