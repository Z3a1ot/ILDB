from abc import ABCMeta, abstractmethod
import os

import subprocess


class LuaExecuter():
    __metaclass__ = ABCMeta

    def __init__(self, executer_path, script_path, protocol):

        """

        :param executer_path: string
        :param script_path: string
        :param protocol: DebuggerProtocol
        :param output: Output
        """
        self.protocol = protocol
        self.executer_path = executer_path
        script_path = os.path.abspath(script_path)
        self.script_path = script_path
        if not os.path.exists(script_path):
            raise Exception("Invalid path {}".format(script_path))

        self.executer_proc = None
        self.cmd = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def execute(self):
        self.executer_proc = subprocess.Popen(self.cmd, shell=True)

    def read_output(self):
        return self.executer_proc.communicate()

    def step(self):
        return self.protocol.step()

    def step_in(self):
        return self.protocol.step_in()

    def cont_exec(self):
        return self.protocol.cont_exec()

    def step_out(self):
        return self.protocol.step_out()

    def send_cmd(self, cmd):
        return self.protocol.send_cmd(cmd)

    def terminate(self):
        return self.executer_proc.terminate()

    def get_state(self):
        src, line = self.protocol.get_state()
        return src, line

    def is_running(self):
        return self.executer_proc.poll() is None

    def cleanup(self):
        if self.executer_proc.poll is None:
            self.executer_proc.terminate()




