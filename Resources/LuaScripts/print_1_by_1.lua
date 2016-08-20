

package.path = "../?.lua;../../?.lua;./?.lua"
require("debug_module")
local function test(i)
    print(i)
end

break_point()
print(1)
for i = 1, 10 do
    test(i)
end

