# This is a sample Python script.

# Press ^R to execute it or replace it with your code.
# Press Double to search everywhere for classes, files, tool windows, actions, and settings.

import sys, getopt

from dockerutils.exception import CmdError
from dockerutils.registrycleaner.main import RegistryCleaner, CleanRegCmdParser

SUB_CMDS = ['cleanreg', 'help']

def main(argv):
    subcmd = argv[0]
    if subcmd not in SUB_CMDS:
        help()
        exit(2)

    try:
        if 'cleanreg' == subcmd:
            command = CleanRegCmdParser.parse(argv[1:])
            command.execute()
        elif 'help' == subcmd:
            help()
            exit()
    except CmdError as err:
        print(err.help)
        exit(2)

def help():
    print('main.py <subcmd> [<options>]')
    print('Supported subcmd list: cleanreg, help')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv[1:])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
