from pyinfra import local

local.include("tasks/pterodactyl/apt_repos.py")
local.include("tasks/pterodactyl/dependencies.py")
local.include("tasks/pterodactyl/panel.py")
local.include("tasks/pterodactyl/mariadb.py")
