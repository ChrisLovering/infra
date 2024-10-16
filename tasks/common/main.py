from io import StringIO
from pathlib import Path

from pyinfra import host
from pyinfra.operations import apt, files, server, systemd

template_dir = Path(__file__).parent / "templates"

server.hostname(
    name="Update hostname to match inventory",
    hostname=host.name,
)

ssh_options = files.put(
    name="Configure SSH daemon options",
    dest="/etc/ssh/sshd_config.d/hardening.conf",
    src=StringIO("""
# Logins
PasswordAuthentication no

# Forwarding
AllowAgentForwarding no
X11Forwarding no

# Keep alive
ClientAliveInterval 300
ClientAliveCountMax 3
"""),
    user="root",
    group="root",
    mode="0444",
)
if ssh_options.changed:
    systemd.service("ssh", restarted=True)

timezone_update = files.link(
    name="Set timezone to UTC",
    path="/etc/localtime",
    target="/usr/share/zoneinfo/Etc/UTC",
    user="root",
    group="root",
)
if timezone_update.changed:
    systemd.service("systemd-timesyncd", restarted=True)

files.template(
    name="Create sudoers lecture",
    src=template_dir / "sudo_lecture.j2",
    dest="/etc/sudo_lecture",
    user="root",
    group="root",
    mode="0444",
)

files.template(
    name="Configure sudo",
    src=template_dir / "sudoers.j2",
    dest="/etc/sudoers.d/conf",
    user="root",
    group="root",
    mode="0444",
)

files.template(
    name="Configure MOTD",
    src=template_dir / "motd.j2",
    dest="/etc/motd",
    user="root",
    group="root",
    mode="0444",
)

apt.packages(
    name="Install system admin tools",
    packages=[
        "net-tools",
        "pwgen",
        "sl",
        "tmux",
        "btop",
        "fortune-mod",
        "cowsay",
        "software-properties-common",
        "curl",
        "apt-transport-https",
        "ca-certificates",
        "gnupg",
        "python3-launchpadlib",
        "tar",
        "unzip",
        "git",
        "unattended-upgrades",
    ],
)
