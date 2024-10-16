from pathlib import Path

from pyinfra.operations import files, server

template_dir = Path(__file__).parent / "templates"


files.directory(
    name="Create pterodactyl folder",
    path="/etc/pterodactyl",
    user="root",
    group="root",
    present=True,
)

files.download(
    name="Download wings executable",
    src="https://github.com/pterodactyl/wings/releases/latest/download/wings_linux_amd64",
    dest="/usr/local/bin/wings",
)
files.file(
    name="Mark wings as executable",
    path="/usr/local/bin/wings",
    mode="u+x",
)
files.put(
    name="Add pterodactyl queue worker service file",
    src=template_dir / "wings.service",
    dest="/etc/systemd/system/wings.service",
    user="root",
    group="root",
)

server.service(
    name="Enable the wings service on boot",
    service="wings.service",
    enabled=True,
)
