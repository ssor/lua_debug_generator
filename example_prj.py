import lua_line_sensor

if __name__ == '__main__':
    debug_files = [
        "C:/lua/a1.lua",
        "C:/lua/a2.lua",
        "C:/lua/a3.lua",
    ]
    ops = {"require_debug_files": ["a1",
                                   "a2",
                                   "a3",
                                   ]}
    lua_line_sensor.handle_files(debug_files, ops)
