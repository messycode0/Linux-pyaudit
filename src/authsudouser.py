import getpass
import os
from pathlib import Path
import pwd
import subprocess

def _operator_home() -> Path:
    username = os.environ.get("SUDO_USER", getpass.getuser())
    try:
        return Path(pwd.getpwnam(username).pw_dir)
    except (KeyError, ImportError):
        return Path.home()

def _valid_names(names):
    return {name.strip() for name in names if name.strip() and name.strip() != "root"}

def get_current_sudo_users():
    try:
        result = subprocess.run(["getent", "group", "sudo"], capture_output=True, text=True, check=True)
        fields = result.stdout.strip().split(":")
        return sorted(_valid_names(fields[3].split(",") if len(fields) > 3 else []))
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        print(f"Could not read the sudo group: {exc}")
        return []

def get_authorized_admin_users():
    path = _operator_home() / "authorized_admin_users.txt"
    try:
        return sorted(_valid_names(path.read_text(encoding="utf-8").splitlines()))
    except OSError as exc:
        print(f"Error reading {path}: {exc}")
        return []

def manage_sudo_users(current_sudo_users, authorized_admin_users):
    current = _valid_names(current_sudo_users)
    authorized = _valid_names(authorized_admin_users)
    for user in sorted(authorized - current):
        try:
            subprocess.run(["sudo", "usermod", "-aG", "sudo", user], check=True)
            print(f"Added user to sudo: {user}")
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Error adding {user} to sudo: {exc}")
    for user in sorted(current - authorized):
        try:
            subprocess.run(["sudo", "deluser", user, "sudo"], check=True)
            print(f"Removed user from sudo: {user}")
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Error removing {user} from sudo: {exc}")

if __name__ == "__main__":
    manage_sudo_users(get_current_sudo_users(), get_authorized_admin_users())
