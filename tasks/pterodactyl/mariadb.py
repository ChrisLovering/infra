from pyinfra.operations import mysql

from tasks.pterodactyl import secrets

mysql.user(
    name=f"Create MariaDB {secrets.db_user["username"]} user",
    user=secrets.db_user["username"],
    password=secrets.db_user["password"],
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
