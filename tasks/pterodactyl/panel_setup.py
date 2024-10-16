from pathlib import Path

from pyinfra.operations import files, server

from tasks.mariadb.secrets import pterodactyl_db_user
from tasks.pterodactyl.secrets import panel_admin_user

template_dir = Path(__file__).parent / "templates"

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
)
if download_panel_tar.changed:
    server.shell(
        name="Unpack panel tar",
        commands=[
            "cd /var/www/pterodactyl && tar -xzvf panel.tar.gz",
            "cd /var/www/pterodactyl && chmod -R 755 storage/* bootstrap/cache",
        ],
    )
    server.shell(
        name="Setup composer",
        commands=[
            "cd /var/www/pterodactyl && cp .env.example .env",
            "cd /var/www/pterodactyl && COMPOSER_ALLOW_SUPERUSER=1 composer install --no-dev --optimize-autoloader",
            "cd /var/www/pterodactyl && php artisan key:generate --force",
        ],
    )
    files.get(
        name="Download generated .env file",
        src="/var/www/pterodactyl/.env",
        dest=".env.remote",
        force=True,
    )
    server.shell(
        name="Setup environment",
        commands=[
            "cd /var/www/pterodactyl && php artisan p:environment:setup --author chris.lovering.95@gmail.com --url panel.chrisjl.dev --timezone Europe/London --no-interaction",
            f"cd /var/www/pterodactyl && php artisan p:environment:database --password {pterodactyl_db_user["password"]} --no-interaction",
        ],
    )
    server.shell(
        name="Migrate database",
        commands=["cd /var/www/pterodactyl && php artisan migrate --seed --force"],
    )
    server.shell(
        name="Create admin user",
        commands=[
            "cd /var/www/pterodactyl && "
            "php artisan p:user:make "
            f"--email {panel_admin_user["email"]} --username {panel_admin_user["username"]} "
            f"--name-first {panel_admin_user["name_first"]} --name-last {panel_admin_user["name_last"]} "
            f"--password {panel_admin_user["password"]} --admin {panel_admin_user["admin"]} "
            "--no-interaction"
        ],
    )

files.directory(
    name="Set permissions on web files",
    path="/var/www/pterodactyl",
    user="www-data",
    group="www-data",
    recursive=True,
)

server.crontab(
    name="Setup pterodactyl queue processor",
    command="php /var/www/pterodactyl/artisan schedule:run >> /dev/null 2>&1",
    user="root",
    cron_name="pterodactyl_queue _processor",
)

files.put(
    name="Add pterodactyl queue worker service file",
    src=template_dir / "pteroq.service",
    dest="/etc/systemd/system/pteroq.service",
    user="root",
    group="root",
)

server.service(
    name="Enable pterodactyl queue worker server on boot",
    service="pteroq.service",
    enabled=True,
    running=True,
)
