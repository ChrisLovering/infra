from pathlib import Path

from pyinfra.operations import apt, files, systemd

template_dir = Path(__file__).parent / "templates"

apt.packages(
    name="Install fail2ban",
    packages=["fail2ban"],
    present=True,
)

create_fail2ban_config = files.template(
    name="Create fail2ban config",
    src=template_dir / "jail.local.j2",
    dest="/etc/fail2ban/jail.local",
    user="root",
    group="root",
    mode="0444",
)
if create_fail2ban_config.changed:
    systemd.service("fail2ban", reloaded=True)

systemd.service(
    name="Start fail2ban service",
    service="fail2ban",
    running=True,
    enabled=True,
)
