from pyinfra.operations import apt, files, server

from shared.apt_repos import add_repo

add_php_repo = add_repo(
    name="PHP",
    repo_url="https://packages.sury.org/php/",
    key_url="https://packages.sury.org/php/apt.gpg",
    key_name="sury-php-archive-keyring",
)

if add_php_repo.changed:
    apt.update()

files.directory(
    name="Ensure script dir exists",
    path="/opt/install_scripts",
    user="root",
    group="root",
)

download_mariadb_setup_script = files.download(
    name="Download the MariaDB repo setup script",
    src="https://downloads.mariadb.com/MariaDB/mariadb_repo_setup",
    dest="/opt/install_scripts/mariadb_repo_setup",
    cache_time=60 * 60 * 24 * 14,  # 2 weeks
)
if download_mariadb_setup_script.changed:
    server.shell(
        name="Run MariaDB setup script",
        commands=["bash /opt/install_scripts/mariadb_repo_setup"],
    )

if download_mariadb_setup_script.changed:
    apt.update()

apt.packages(
    name="Install pterodactyl dependencies",
    packages=[
        "php8.3",
        "php8.3-common",
        "php8.3-cli",
        "php8.3-gd",
        "php8.3-mysql",
        "php8.3-mbstring",
        "php8.3-bcmath",
        "php8.3-xml",
        "php8.3-fpm",
        "php8.3-curl",
        "php8.3-zip",
    ],
    present=True,
)

download_composer_setup_script = files.download(
    name="Download the composer setup script",
    src="https://getcomposer.org/installer",
    dest="/opt/install_scripts/composer_install",
    cache_time=60 * 60 * 24 * 14,  # 2 weeks
)
if download_composer_setup_script.changed:
    server.shell(
        name="Run composer setup script",
        commands=["php /opt/install_scripts/composer_install --install-dir=/usr/local/bin --filename=composer"],
    )
