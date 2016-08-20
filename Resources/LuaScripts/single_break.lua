

package.path = "../?.lua;../../?.lua;./?.lua"
require("debug_module")

local function test()
    print("Require_Module")
end



break_point()
test()

