from pyinfra.operations import apt, server

from shared.apt_repos import add_repo

add_docker_repo = add_repo(
    name="docker",
    repo_url="https://download.docker.com/linux/debian",
    key_url="https://download.docker.com/linux/debian/gpg",
    key_name="docker",
    repo_name="stable",
)
if add_docker_repo.changed:
    apt.update()

apt.packages(
    name="Install docker packages",
    packages=["docker-ce", "docker-ce-cli", "containerd.io", "docker-buildx-plugin", "docker-compose-plugin"],
)

server.group(
    name="Add docker group",
    group="docker",
    present=True,
)
server.service(name="Enable docker on boot", service="docker.service", enabled=True)
server.service(name="Enable containerd on boot", service="containerd.service", enabled=True)
