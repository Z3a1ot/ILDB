import os
import string

import subprocess

import time

from libs.DebuggerProtocol import DebuggerProtocol


class FileBasedDebuggerProtocol(DebuggerProtocol):

    def __init__(self):
        self.cmd_file = "/tmp/.ildb_cmd"
        self.lock_file = "/tmp/.ildb_lock"
        self.state_file = "/tmp/.ildb_state"
        self.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        if os.path.isfile(self.cmd_file):
            os.remove(self.cmd_file)
        if os.path.isfile(self.lock_file):
            os.remove(self.lock_file)
        if os.path.isfile(self.state_file):
            os.remove(self.state_file)

    def send_cmd(self, cmd):
        #print("send cmd: " + cmd)
        cmd = string.replace(cmd,"'","\\\'")
        #print("send after replace cmd: " + cmd)
        subprocess.Popen("sh sync_write.sh '{}' '{}' '{}'".format(self.lock_file, self.cmd_file, cmd), shell=True,
                         stdout=subprocess.PIPE).communicate()

    def step(self):
        self.send_cmd("step")

    def step_out(self):
        self.send_cmd("step_out")

    def step_in(self):
        self.send_cmd("step_in")

    def cont_exec(self):
        self.send_cmd("cont")

    def get_state(self):
        retry = 0
        while not os.path.isfile(self.state_file) and retry < 10:
            time.sleep(0.1)
            retry += 1
        if retry >= 10:
            return None, None
        state = subprocess.Popen("sh sync_read.sh {} {}".format(self.lock_file, self.state_file),
                         shell=True, stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen("sh sync_rm.sh {} {}".format(self.lock_file, self.state_file),
                                 shell=True, stdout=subprocess.PIPE).communicate()
        state = state.split(" ")
        if len(state) < 2:
            return None, None
        src = state[0]
        line = state[1]
        return src, int(line)
