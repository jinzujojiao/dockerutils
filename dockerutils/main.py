# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import sys, getopt
from registrycleaner import RegistryCleaner

def main(argv):
    host = 'localhost'
    port = '5000'
    repo = None
    try:
        opts, args = getopt.getopt(argv, "hH:p:r:", ["host=", "port=", "repo="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-H", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-r", "--repo"):
            repo = arg

    if repo is None:
        help()
        sys.exit(2)

    cleaner = RegistryCleaner(host, port)
    cleaner.clean_repo(repo)

def help():
    print('main.py [-H <registry host>] [-p <registry port>] -r <repository name>')
    print('registry host default value is localhost, registry port default value is 5000')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
