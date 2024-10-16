from pathlib import Path

from pyinfra.operations import apt, files, server

from tasks.certbot import vars

template_dir = Path(__file__).parent / "templates"

apt.packages(
    name="Install certbot & certbot cloudflare extension",
    packages=["python3-certbot", "python3-certbot-dns-cloudflare"],
    present=True,
)

files.put(
    name="Generate Cloudflare credentials file",
    src=template_dir / "certbot.ini",
    dest="/etc/letsencrypt/cloudflare.ini",
    user="root",
    group="root",
    mode="0400",
)

server.group(
    name="Create cert-users group",
    group="cert-users",
    present=True,
)
for path in ("/etc/letsencrypt/live", "/etc/letsencrypt/archive"):
    files.directory(
        name="Create certificate directories on hosts",
        path=path,
        user="root",
        group="cert-users",
        mode="u=rwX,g=rX",
        recursive=True,
    )

server.shell(
    name="Request certificates for configured domains",
    commands=[
        f"certbot certonly --agree-tos --non-interactive --email {vars.certbot_email} --dns-cloudflare-propagation-seconds 30 "
        f"--dns-cloudflare --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini -d {vars.certbot_domains}"
    ],
)

files.put(
    name="Add post-renewal nginx reload hook",
    src=template_dir / "reload-nginx",
    dest="/etc/letsencrypt/renewal-hooks/deploy/reload-nginx",
    user="root",
    group="root",
    mode="0600",
)
