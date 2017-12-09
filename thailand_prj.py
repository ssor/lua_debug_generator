import lua_line_sensor

if __name__ == '__main__':
    debug_files = [
        "D:/lua/plist-gate/list/api/skushow/backend_service.lua",
        "D:/lua/plist-gate/list/api/skushow/sku_conf.lua",
        "D:/lua/plist-gate/list/api/skushow/sku.lua",
        "D:/lua/plist-gate/list/api/skushow/sku_attr.lua",
        "D:/lua/plist-gate/list/api/skushow/brand.lua",
        "D:/lua/plist-gate/list/api/skushow/topic.lua",
        "D:/lua/plist-gate/list/api/skushow/cache_front.lua",
        "D:/lua/plist-gate/list/api/skushow/redis_front.lua",
    ]
    ops = {"require_debug_files": ["sku_conf",
                                   "backend_service",
                                   "sku",
                                   "sku_attr",
                                   "brand",
                                   "topic",
                                   "cache_front",
                                   "redis_front",
                                   ]}
    new_lines = lua_line_sensor.handle_files(debug_files, ops)
