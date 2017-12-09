local util = require("list.api.util")
local config_by_file = require("list.api.config_by_file")
local topic = require("list.api.skushow.topic")


local _M = {}
_M.cluster_config_key = "ONLINE_SERVICE_GROUP"

local five_minutes = 5 * 60

local function update_to_cache(cluster)
     local success, err = ngx.shared.config:set("online_service_group", new_config, five_minutes)
    if success == true then
        return true
    else
        util.log("cache online_service_group err: ", err)
        return false
    end
end


local function save_online_cluster_config_to_file(new_config)
    local err = config_by_file.add_config("online_service_group", new_config)
    if err == nil then
        return true
    else
        util.log("save_online_cluster_config_to_file err: ", err)
        return false
    end
end

local function two_values_returned(para1, para2)
    return false, true
end

function _M.get_online_cluster_config()
    local cluster_online = ngx.shared.config:get("online_service_group")
    if cluster_online == nil then
        local online_service_group =  config_by_file.get_config("online_service_group")
        if online_service_group == nil then
            return nil
        else
            update_to_cache(online_service_group)
            return online_service_group
        end
    else
        return cluster_online
    end
end


function _M.update_online_cluster_config(new_config)
    local ok = save_online_cluster_config_to_file(new_config)
    if ok == true then
        if update_to_cache(new_config) == true then
            return true
        else
            return false
        end
    else
        return false
    end
end



return _M
