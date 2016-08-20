

class InteractiveDebugger:

    def __init__(self, executer, output):
        self.executer = executer
        self.output = output

    def start(self):
        self.executer.execute()
        while self.executer.is_running():
            src, line = self.executer.get_state()
            if src is None or line is None:
                continue
            print(self.output.format_state(src, line))
            cmd = raw_input(self.output.prompt())
            if cmd == 'n':
                self.executer.step_in()
            elif cmd == 'c':
                self.executer.cont_exec()
            elif cmd =='\n':
                continue
            else:
                self.executer.send_cmd(cmd)

    def cleanup(self):
        self.executer.cleanup()
