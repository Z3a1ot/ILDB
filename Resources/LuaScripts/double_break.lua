
package.path = "../?.lua;../../?.lua;./?.lua"
require("debug_module")
function test()
    print("Require_Module")
end

function test1()
    test()
end



break_point()
test()
break_point()
test1()

