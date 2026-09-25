import getpass
import os
from pathlib import Path
import pwd
import subprocess

SYSTEM_UID_CUTOFF = 1000

def _operator_home() -> Path:
    username = os.environ.get("SUDO_USER", getpass.getuser())
    try:
        return Path(pwd.getpwnam(username).pw_dir)
    except (KeyError, ImportError):
        return Path.home()

def get_human_users():
    try:
        return sorted(entry.pw_name for entry in pwd.getpwall() if entry.pw_uid >= SYSTEM_UID_CUTOFF)
    except OSError as exc:
        print(f"Error retrieving users: {exc}")
        return []

def compare_users(current_on_system_users):
    path = _operator_home() / "authorized_users.txt"
    try:
        authorized = {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
    except OSError as exc:
        print(f"Error reading {path}: {exc}")
        return [], []
    current = set(current_on_system_users)
    return sorted(current - authorized), sorted(authorized - current)

def stabilize_users(add_users_waitlist, remove_users_waitlist):
    operator = os.environ.get("SUDO_USER", getpass.getuser())
    for username in remove_users_waitlist:
        if username in {"root", operator}:
            print(f"Skipping protected user: {username}")
            continue
        try:
            subprocess.run(["sudo", "userdel", "--remove", username], check=True)
            print(f"Removed user: {username}")
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Error removing user {username}: {exc}")
    for username in add_users_waitlist:
        try:
            subprocess.run(["sudo", "useradd", "--create-home", username], check=True)
            print(f"Added user: {username}")
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Error adding user {username}: {exc}")

# Backward-compatible spelling for callers using the original API.
stablize_users = stabilize_users

def change_user_passwords():
    """Set one operator-provided password for human users; never log it."""
    password = getpass.getpass("New password for all human users (leave blank to cancel): ")
    if not password:
        print("Password change cancelled.")
        return
    if password != getpass.getpass("Confirm new password: "):
        print("Passwords did not match; no passwords were changed.")
        return
    for username in get_human_users():
        try:
            subprocess.run(["sudo", "chpasswd"], input=f"{username}:{password}\n", text=True, check=True)
            print(f"Password changed for user: {username}")
        except (OSError, subprocess.CalledProcessError) as exc:
            print(f"Error changing password for {username}: {exc}")

if __name__ == "__main__":
    print("Run runner.py to use the full audit workflow.")
