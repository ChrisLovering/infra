from pyinfra import host
from pyinfra.api.operation import OperationMeta
from pyinfra.facts.server import LsbRelease
from pyinfra.operations import apt, files, server


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

    host_release_codename = host.get_fact(LsbRelease)["codename"]
    return apt.repo(
        name=f"Add the {key_name} apt repo",
        src=f"deb [signed-by=/usr/share/keyrings/{key_name}.gpg] {repo_url} {host_release_codename} main",
    )
