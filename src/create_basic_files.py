from pathlib import Path
import getpass
import os
import pwd

def _operator_home() -> Path:
    username = os.environ.get("SUDO_USER", getpass.getuser())
    try:
        return Path(pwd.getpwnam(username).pw_dir)
    except (KeyError, ImportError):
        return Path.home()

def cbf() -> int:
    """Create both allow-list files if they do not already exist."""
    created = 0
    for filename in ("authorized_users.txt", "authorized_admin_users.txt"):
        path = _operator_home() / filename
        if path.exists():
            print(f"{filename} already exists")
            continue
        path.touch(mode=0o600)
        print(f"{filename} was created at {path}")
        created += 1
    return created

if __name__ == "__main__":
    cbf()
