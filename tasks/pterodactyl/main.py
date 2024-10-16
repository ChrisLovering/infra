from pyinfra import local

local.include("tasks/pterodactyl/dependencies.py")
local.include("tasks/pterodactyl/panel_setup.py")
local.include("tasks/pterodactyl/panel_webserver.py")
local.include("tasks/pterodactyl/wings.py")
