from pyinfra import local
from pyinfra.operations import apt, files, server

local.include("tasks/pterodactyl/apt_repos.py")
local.include("tasks/pterodactyl/dependencies.py")

