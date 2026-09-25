import subprocess

def update_upgrade():
    # system update and upgrade
    for command in (("sudo", "apt-get", "update"), ("sudo", "apt-get", "upgrade", "-y"), ("sudo", "apt-get", "autoremove", "-y")):
        subprocess.run(command, check=True)

if __name__ == "__main__":
    update_upgrade()
