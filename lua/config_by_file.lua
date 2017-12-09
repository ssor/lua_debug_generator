local util = require("list.api.util")

local default_config_file = "configs.data"


local _M = {}


local function file_exists(file_name)
    local f = io.open(file_name, "rb")
    if f then f:close() end
    return f ~= nil
end

local function load_config_from_file()
    if file_exists(default_config_file) == true then
        local config_file, err = io.open(default_config_file, "r")
        if err == nil then
            local data = config_file:read("*a")
            config_file:close()
            if data == nil then
                return nil, nil
            else
                return util.json_decode(data)
            end
        else
            util.log("config_by_file:load_config_from_file err: ", err)
            return nil, err
        end
    else
        return nil, nil
    end
end


local function save_config_to_file(data)
    local raw = util.encode(data)
    if raw == nil then
        return "no data saved"
    else
        local config_file, err = io.open(default_config_file, "w")
        if err == nil then
            local raw = util.encode(data)
            local _, err = config_file:write(raw)
            config_file:close()
            return err
        else
            return err
        end
    end
end

-- get all config, deserialize, add new config, then serialize and save to file
local function add_config(name, value)
    local data, err = load_config_from_file()
    if err == nil then
        if data == nil then
            data = {}
        end
        data[name] = value
        return save_config_to_file(data)
    else
        return err
    end
end

-- get all config, deserialize, remove new config, then serialize and save to file
local function remove_config(name)
    local data, err = load_config_from_file()
    if err == nil then
        data[name] = nil
        return save_config_to_file(data)
    else
        return nil, err
    end
end

local function get_config(name)
    local data, err = load_config_from_file()
    if err == nil then
        if data == nil then
            return nil
        else
            return data[name]
        end
    else
        util.log("get_config ---> err: ", err)
        return nil
    end
end


_M.add_config = add_config
_M.remove_config = remove_config
_M.get_config = get_config

return _M