

class OutputHandler:

    def __init__(self, offset):
        self.offset = offset
        self.filler = "~~~~~~~~~\n"

    def format_state(self, src, line):
        line = line - 1
        lua_src = open(src.strip()[1:], "r")
        lua_code = lua_src.readlines()
        lua_src.close()
        lua_size = len(lua_code)
        result = [str(line + 1) + "  ->" + lua_code[line]]
        for i in range(1,self.offset):
            index = line-i
            if index < 0:
                if result[0] != self.filler:
                    result.insert(0,self.filler)
            else:
                result.insert(0,str(index+1)+"    "+lua_code[index])
            index = line+i
            if index > lua_size-1:
                if result[len(result)-1] != self.filler:
                    result.append(self.filler)
            else:
                result.append(str(index+1)+"    "+lua_code[index])

        return "".join(result)


    def prompt(self):
        return "n - next, c - continue\nildb>"
