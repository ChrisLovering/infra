from pyinfra.operations import server

from tasks.users.users import users

for user in users:
    server.user(
        name=f"Create user {user["name"]}",
        present=True,
        user=user["name"],
        groups=user["groups"],
        password=user["passwd_hash"],
        public_keys=user["ssh_keys"],
        shell="/bin/bash",
        create_home=True,
    )
