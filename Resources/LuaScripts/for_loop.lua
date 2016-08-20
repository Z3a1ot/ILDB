

package.path = "../?.lua;../../?.lua;./?.lua"
require("debug_module")
function test()
    print("Require_Module")
    print("Require_Module")
    print("Require_Module")
    print("Require_Module")
    print("Require_Module")
    test2()
end



function test2()

    print("test2")
    print("test2")
    print("test2")


end
for i = 1, 3 do
    break_point()
    test()
end


