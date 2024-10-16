from pathlib import Path

from pyinfra.operations import files, server

template_dir = Path(__file__).parent / "templates"

files.put(
    name="Upload pterodactyl server conf",
    src=template_dir / "pterodactyl.conf",
    dest="/etc/nginx/sites-available/pterodactyl.conf",
    user="root",
    group="root",
)
enable_pterodactyl = files.link(
    name="Enable pterodactyl conf",
    path="/etc/nginx/sites-enabled/pterodactyl.conf",
    target="/etc/nginx/sites-available/pterodactyl.conf",
)
if enable_pterodactyl.changed:
    server.service(
        name="Restart nginx",
        service="nginx.service",
        reloaded=True,
    )
