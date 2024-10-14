from pyinfra import local

local.include("tasks/common/main.py")
local.include("tasks/users/main.py")
