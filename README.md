
#lua debug file generator

## Why do this
As develop in lua and nginx, the info of how code works is great help for debug. 

There is one way usually used: log. As code runs, the record is wirtten to log files if we do this in code. However sometimes log is too large, and we need to spend a lot of time and attention to analysis logs to get right answer.

If there is a way to get all relative debug info without any other mass info, it would be  great help.

Simply thinking, if an API's debug info is returned at a direct way, it would be great. So this tools will do this. It will simulate APIs working process, with recording the process info and important values. All these debug info will help to find out what's wrong with the APIs


## How to do:

### prepare
- functions in code should has no more than two returned values, this would be make the question simpler

### 1. add debuginfo to lua file
- add function baseinfo(function name, paras)
- add debuginfo as third to return values
- get debuginfo from depended functions

### 2. edit require file path
