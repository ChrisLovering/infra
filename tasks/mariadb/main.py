from pyinfra.operations import apt, files, mysql, server

from tasks.mariadb import secrets

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
    packages=["mariadb-server"],
    present=True,
)

mysql.user(
    name=f"Create MariaDB {secrets.pterodactyl_db_user["username"]} user",
    user=secrets.pterodactyl_db_user["username"],
    password=secrets.pterodactyl_db_user["password"],
)

mysql.database(
    name="Create panel database",
    database="panel",
)

mysql.privileges(
    name="Give pterodactyl user all privileges to panel db",
    user="pterodactyl",
    privileges="ALL",
    database="panel",
    with_grant_option=True,
)
