import os

import time

from libs.LuaExecuter import LuaExecuter


class LuaInterpreterExecuter(LuaExecuter):

    def __init__(self, script_path, protocol, debug=False):
        LuaExecuter.__init__(self, "lua", script_path,protocol)
        if debug:
            self.debug = debug
            self.stdout = "/tmp/.ildb_stdout"
            self.stderr = "/tmp/.ildb_stderr"
            if os.path.isfile(self.stdout):
                os.remove(self.stdout)
            if os.path.isfile(self.stderr):
                os.remove(self.stderr)
            self.cmd = "{} {} 1>{} 2>{}".format(self.executer_path, self.script_path,self.stdout,self.stderr)
        else:
            self.cmd = "{} {}".format(self.executer_path, self.script_path)

    def read_output(self):
        time.sleep(1)
        fh = open(self.stdout,"r")
        stdout = fh.read()
        fh.close()
        fh = open(self.stderr,"r")
        stderr = fh.read()
        fh.close()
        return stdout,stderr
