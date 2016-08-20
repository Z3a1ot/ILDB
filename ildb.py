import argparse
import os

from libs.InteractiveDebugger import InteractiveDebugger
from libs.LuaInterpreterExecuter import LuaInterpreterExecuter
from libs.FileBasedDebuggerProtocol import FileBasedDebuggerProtocol
from libs.OutputHandler import OutputHandler


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--script', type=str, required=True, help='The script to debug', dest='script')
    parser.add_argument('-l', '--lua', type=str, required=True, help='Path to lua interpreter', dest='lua')
    parser.add_argument('-i', '--lines', type=int, required=False, default=1, help='Lines to show aroung debugger line', dest='lines')

    return parser.parse_args()


def main():

    args = parse_args()

    if not os.path.isfile(args.script):
        print("Invalid script path")
        exit(-1)

    protocol = FileBasedDebuggerProtocol()
    output = OutputHandler(args.lines)
    with LuaInterpreterExecuter(args.script, protocol) as executer:
        idebugger = InteractiveDebugger(executer,output)
        try:
            idebugger.start()
        except Exception as e:
            print(e)
        finally:
            protocol.cleanup()
            idebugger.cleanup()

if __name__ == "__main__":
    main()
