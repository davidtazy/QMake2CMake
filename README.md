# QMakeToCMake
helper script to move qmake based project to cmake
alpha

usage:
/path/to/QMakeToCMake> python q2c\qmake_to_cmake.py -h
usage: qmake_to_cmake.py [-h] [-n] [-r] [-s] path

positional arguments:
  path             directory or file

optional arguments:
  -h, --help       show this help message and exit
  -n, --dry-run    print cmakelist.txt on the console
  -r, --recursive  walk all subdirectories
  -s, --show       show result file(s)

