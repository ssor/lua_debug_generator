
local util = require("list.api.util")

local _M = {}
_M.stack_cache = {}


function _M.must_not_nil(self, arg)
    return arg or "nil"
end

function _M.clear_cache(self)
    self.stack_cache = {}
end

-- push somme standalone arg
function _M.add(self, log)
    table.insert(self.stack_cache, log)
end

function _M.get_cache(self)
    return self.stack_cache
end

function _M.print_logs(self, f)
    if f ~= nil then
        f(util.encode(self.stack_cache))
    else
        ngx.say(util.encode(self.stack_cache))
    end
end

return _M