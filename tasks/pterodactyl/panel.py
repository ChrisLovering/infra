from pyinfra.operations import files, server

files.directory(
    name="Create pterodactyl web folder",
    path="/var/www/pterodactyl",
    user="root",
    group="root",
)

download_panel_tar = files.download(
    name="Download panel tar file",
    src="https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz",
    dest="/var/www/pterodactyl/panel.tar.gz",
    user="root",
    group="root",
    cache_time=60 * 60 * 24 * 14,  # 2 weeks
)
if download_panel_tar.changed:
    server.shell(
        name="Unpack panel tar",
        commands=[
            "tar -xzvf /var/www/pterodactyl/panel.tar.gz -C /var/www/pterodactyl",
            "chmod -R 755 /var/www/pterodactyl/storage/* /var/www/pterodactyl/bootstrap/cache",
        ],
    )
