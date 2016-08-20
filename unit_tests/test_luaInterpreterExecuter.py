
from unittest import TestCase

import time

from libs.FileBasedDebuggerProtocol import FileBasedDebuggerProtocol
from libs.LuaInterpreterExecuter import LuaInterpreterExecuter
import logging

from libs.OutputHandler import OutputHandler


class TestLuaInterpreterExecuter(TestCase):

    def setUp(self):
        logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG)
        self.protocol = FileBasedDebuggerProtocol()
        self.output = OutputHandler(1)

    def tearDown(self):
        if self.executer:
            self.executer.cleanup()

    def test_cont_exec(self):
        self.executer = LuaInterpreterExecuter("./Resources/LuaScripts/single_break.lua", self.protocol, True)
        self.executer.execute()
        src,line = self.executer.get_state()
        state = self.output.format_state(src,line)
        logging.info(state)
        assert("->test()" in state)
        self.executer.cont_exec()
        sout, serr = self.executer.read_output()
        assert (not serr)
        logging.info(sout)
        assert (sout)
        assert (sout.strip() == "Require_Module")

    def test_cont_exec_neg(self):
        self.executer = LuaInterpreterExecuter("./Resources/LuaScripts/single_break.lua", self.protocol, True)
        self.executer.execute()
        time.sleep(1)
        if not self.executer.is_running():
            self.fail("Process finished")

    def test_execute(self):
        self.executer = LuaInterpreterExecuter("./Resources/LuaScripts/print_test.lua", self.protocol, True)
        self.executer.execute()
        sout, serr = self.executer.read_output()
        logging.info(sout)
        assert(not serr)
        assert(sout.strip() == "Lua Print Test")

    def test_require_debug(self):
        self.executer = LuaInterpreterExecuter("./Resources/LuaScripts/require_module.lua", self.protocol, True)
        self.executer.execute()
        sout, serr = self.executer.read_output()
        logging.info(sout)
        assert (not serr)
        assert (sout.strip() == "Require_Module")

    def test_double_break(self):
        self.executer = LuaInterpreterExecuter("./Resources/LuaScripts/double_break.lua", self.protocol, True)
        self.executer.execute()
        src,line = self.executer.get_state()
        state = self.output.format_state(src,line)
        logging.info(state)
        assert ("->test()" in state)
        self.executer.cont_exec()
        time.sleep(1)
        src,line = self.executer.get_state()
        state = self.output.format_state(src,line)
        logging.info(state)
        assert("->test1()" in state)
        self.executer.cont_exec()
        sout, serr = self.executer.read_output()
        logging.info(sout)
        assert(not serr)
        assert(sout.strip() == "Require_Module\nRequire_Module")

    def test_double_break_neg(self):
        self.executer = LuaInterpreterExecuter("./Resources/LuaScripts/double_break.lua", self.protocol, True)
        self.executer.execute()
        src,line = self.executer.get_state()
        state = self.output.format_state(src,line)
        assert ("->test()" in state)
        self.executer.cont_exec()
        if not self.executer.is_running():
            self.fail("Process finished")