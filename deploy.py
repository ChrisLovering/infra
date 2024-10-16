from pyinfra import local

local.include("tasks/common/main.py")
local.include("tasks/users/main.py")
local.include("tasks/fail2ban/main.py")
local.include("tasks/redis/main.py")
local.include("tasks/mariadb/main.py")
local.include("tasks/certbot/main.py")
local.include("tasks/pterodactyl/main.py")
