from pathlib import Path

from pyinfra.operations import apt, files, server

template_dir = Path(__file__).parent / "templates"

apt.packages(
    name="Install nginx & modules",
    packages=["nginx", "libnginx-mod-http-lua"],
    present=True,
)
files.link(
    name="Remove default nginx site",
    path="/etc/nginx/sites-enabled/default",
    present=False,
)

upload_default_conf = files.put(
    name="Upload default nginx server conf",
    src=template_dir / "default_server.conf",
    dest="/etc/nginx/conf.d/default_server.conf",
    user="root",
    group="root",
    mode="0644",
)
if upload_default_conf.changed:
    server.service(
        name="Reload nginx service",
        service="nginx.service",
        reloaded=True,
    )
