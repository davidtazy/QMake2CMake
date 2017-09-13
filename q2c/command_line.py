from .qmake_to_cmake import QMakeToCMake
import os


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

def main():

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

if __name__ == '__main__':
    main()