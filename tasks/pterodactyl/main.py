from pyinfra import local

local.include("tasks/pterodactyl/dependencies.py")
local.include("tasks/pterodactyl/panel_setup.py")
