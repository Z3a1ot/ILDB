
local cmd_file = "/tmp/.ildb_cmd"
local lock_file = "/tmp/.ildb_lock"
local state_file = "/tmp/.ildb_state"

local line_num
local src_file

local function ret_hook(event)
    debug.sethook(line_hook,"l")
end

local function call_hook(event)
end

local function handle_input()
    local fh
    local tmp_file
    local done = false
    local done = false
    while not fh do
        tmp_file = "/tmp/.ildb_tmp"
        os.execute("sh sync_read.sh " .. lock_file .. " " .. cmd_file .. " > " .. tmp_file)
        fh = io.open(tmp_file,"r")
    end
    local line = fh:read()
    if line == "cont" then
        debug.sethook()
        done = true
    elseif line == "step" then
        done = true
    elseif line == "step_in" then
        done = true
    elseif line == "step_out" then
        debug.sethook()
        debug.sethook(ret_hook,"r")
        done = true
    elseif line and string.sub(line,1,1) ~= "@" then
        pcall(function() dofile(cmd_file) end)
        os.execute("sh sync_rm.sh " .. lock_file .. " " .. cmd_file)
        os.execute("sh sync_write.sh " .. lock_file .. " " .. state_file .. " '" ..
        src_file .. " " .. line_num .. "'")
        done = false
    else
    end
    fh:close()
    os.execute("sh sync_rm.sh " .. lock_file .. " " .. tmp_file)
    return done
end

function line_hook(event,line)
    local info = debug.getinfo(2)
    if string.find(info.source, 'debug_module') then
        return
    end
    src_file = info.source
    line_num = line
    if info ~= nil then
        os.execute("sh sync_write.sh " .. lock_file .. " " .. state_file .. " '" ..
        info.source .. " " .. line .. "'")
    end
    while not handle_input() do  end
    os.execute("sh sync_rm.sh " .. lock_file .. " " .. cmd_file)
end

function break_point()
    debug.sethook(line_hook,"l")
end
