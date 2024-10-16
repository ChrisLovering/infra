from pyinfra.operations import apt

from shared.apt_repos import add_repo

add_redis_repo = add_repo(
    name="Redis",
    repo_url="https://packages.redis.io/deb",
    key_url="https://packages.redis.io/gpg",
    key_name="redis-archive-keyring",
)

if add_redis_repo.changed:
    apt.update()

apt.packages(
    name="Install redis server",
    packages=["redis-server"],
)
