from pyinfra import host
from pyinfra.api.operation import OperationMeta
from pyinfra.facts.server import LsbRelease
from pyinfra.operations import apt, files, server

host_release_codename = host.get_fact(LsbRelease)["codename"]


def add_repo(name: str, repo_url: str, key_url: str, key_name: str) -> OperationMeta:
    """Add an apt repo, including signing keys."""
    download_key = files.download(
        name=f"Download the {name} apt signing key",
        src=key_url,
        dest=f"/usr/share/keyrings/{key_name}.asc",
        cache_time=60 * 60 * 24 * 14,  # 2 weeks
    )
    if download_key.changed:
        server.shell(
            name=f"Dearmour {name} pgp key",
            commands=[
                f"gpg --no-tty --batch --yes --dearmor -o /usr/share/keyrings/{key_name}.gpg /usr/share/keyrings/{key_name}.asc"
            ],
        )
    return apt.repo(
        name=f"Add the {key_name} apt repo",
        src=f"deb [signed-by=/usr/share/keyrings/{key_name}.gpg] {repo_url} {host_release_codename} main",
    )


add_redis_repo = add_repo(
    name="Redis",
    repo_url="https://packages.redis.io/deb",
    key_url="https://packages.redis.io/gpg",
    key_name="redis-archive-keyring",
)

add_php_repo = add_repo(
    name="PHP",
    repo_url="https://packages.sury.org/php/",
    key_url="https://packages.sury.org/php/apt.gpg",
    key_name="sury-php-archive-keyring",
)

if add_php_repo.changed or add_redis_repo.changed:
    apt.update()
