
#lua debug file generator

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
