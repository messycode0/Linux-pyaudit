"""Run the bundled Ansible hardening playbook."""

from pathlib import Path
import shutil
import subprocess

PLAYBOOK = Path(__file__).resolve().parent / "ansible_files" / "UbuntuBase.yml"

def check_ansible_installed() -> bool:
    return shutil.which("ansible-playbook") is not None

def install_ansible() -> bool:
    """Install Ansible on Debian/Ubuntu systems after explicit user consent."""
    if shutil.which("apt-get") is None:
        print("Ansible is not installed and apt-get is unavailable.")
        return False
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "ansible"], check=True)
        return True
    except subprocess.CalledProcessError as exc:
        print(f"Could not install Ansible (exit code {exc.returncode}).")
        return False

def run_ansible_playbook() -> bool:
    try:
        subprocess.run(["ansible-playbook", str(PLAYBOOK), "-vv"], check=True)
        print("Ansible playbook executed successfully.")
        return True
    except subprocess.CalledProcessError as exc:
        print(f"Error running Ansible playbook (exit code {exc.returncode}).")
        return False

def main() -> bool:
    if not check_ansible_installed():
        print("Ansible is not installed.")
        if input("Install Ansible with apt now? (y/N): ").strip().lower() != "y":
            return False
        if not install_ansible() or not check_ansible_installed():
            print("Ansible is still unavailable; the playbook was not run.")
            return False
    return run_ansible_playbook()

if __name__ == "__main__":
    main()
