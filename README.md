
# lua debug file generator

## Why do this
As develop in lua and nginx, the info of how code works is great help for debug. 

There is one way usually used: log. As code runs, the record is wirtten to log files if we do this in code. However sometimes log works not very well:
- log is too large, and we need to spend a lot of time and attention to analysis logs to get right answer
- If code is running online, we have no chance to print logs we need which we don't think need to print out

If there is a way to get all relative debug info without any other mass info, and if we don't need no more log is print out as sometime-use, it would be  great help.

Simply thinking, if an API's debug info is returned at a direct way as we request, it would be great. So this tools will do this. It will simulate APIs working process, with recording the process info and important values. All these debug info will help to find out what's wrong with the APIs


## How to do:


### 1. add debuginfo to lua file
we need add log-print code to functions at:
> 1. function entry
> 2. before invoke a function in 
> 3. after function returns

### 2. edit require file path
As in fact we generate similar code files, we also need to edit the require parts


## Use this project

In folder lua, there is a log_stack.lua file which is used to cache logs in one nginx request handle, and can be seen as a reference for you.

On above of "How to do", two things need to do, and we should let the project know which files should be handled, so there should be some configs.

The configs is very simple, like example_pry.py, we need first list files to insert log code:


```
    debug_files = [
        "C:/lua/a1.lua",
        "C:/lua/a2.lua",
        "C:/lua/a3.lua",
    ]
```


Then list the require of lua which module should use debug version(we generate new files, and do Not change any src code)


```
    ops = {"require_debug_files": ["a1",
                                   "a2",
                                   "a3",
                                   ]}
```

At last do this job

```
	lua_line_sensor.handle_files(debug_files, ops)
```

