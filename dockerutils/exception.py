class CmdError(Exception):
    def __init_(self, msg, help):
        self.msg = msg
        self.help = help

