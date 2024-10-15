from pyinfra.operations import mysql

from tasks.pterodactyl import secrets

for user in secrets.db_users:
    mysql.user(
        name=f"Create MariaDB {user["user"]} user",
        user=user["user"],
        password=user["password"],
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
