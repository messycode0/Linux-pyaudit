import useraudit
import create_basic_files
import etc
import update_upgrade
import authsudouser
import disable_nonessential_services 
import delete_media_files
import ansible_runner

import time
from pathlib import Path

version = "0"

try:
    version = (Path(__file__).resolve().parent / "version").read_text(encoding="utf-8").strip()
except OSError:
    print("Error: failed to get version number...")

if __name__ == "__main__":
    print("WARNING: This applies a broad Linux hardening baseline. Review the playbook and keep console access available.\n")

    print(
        f"""
  /$$$$$$            /$$       /$$$$$$$           /$$                 /$$$$$$$                                                      
 /$$__  $$          | $$      | $$__  $$         | $$                | $$__  $$                                                     
| $$  \__/  /$$$$$$ | $$      | $$  \ $$ /$$$$$$ | $$ /$$   /$$      | $$  \ $$ /$$$$$$  /$$$$$$/$$$$   /$$$$$$  /$$$$$$$   /$$$$$$ 
| $$       |____  $$| $$      | $$$$$$$//$$__  $$| $$| $$  | $$      | $$$$$$$//$$__  $$| $$_  $$_  $$ /$$__  $$| $$__  $$ |____  $$
| $$        /$$$$$$$| $$      | $$____/| $$  \ $$| $$| $$  | $$      | $$____/| $$  \ $$| $$ \ $$ \ $$| $$  \ $$| $$  \ $$  /$$$$$$$
| $$    $$ /$$__  $$| $$      | $$     | $$  | $$| $$| $$  | $$      | $$     | $$  | $$| $$ | $$ | $$| $$  | $$| $$  | $$ /$$__  $$
|  $$$$$$/|  $$$$$$$| $$      | $$     |  $$$$$$/| $$|  $$$$$$$      | $$     |  $$$$$$/| $$ | $$ | $$|  $$$$$$/| $$  | $$|  $$$$$$$
 \______/  \_______/|__/      |__/      \______/ |__/ \____  $$      |__/      \______/ |__/ |__/ |__/ \______/ |__/  |__/ \_______/
                                                      /$$  | $$                                                                     
                                                     |  $$$$$$/                                                                     
                                                      \______/                                                                      
  /$$$$$$  /$$      /$$ /$$$$$$ /$$$$$$$$ /$$$$$$$$                                                                                 
 /$$__  $$| $$  /$ | $$|_  $$_/| $$_____/|__  $$__/                                                                                 
| $$  \__/| $$ /$$$| $$  | $$  | $$         | $$                                                                                    
|  $$$$$$ | $$/$$ $$ $$  | $$  | $$$$$      | $$                                                                                    
 \____  $$| $$$$_  $$$$  | $$  | $$__/      | $$                                                                                    
 /$$  \ $$| $$$/ \  $$$  | $$  | $$         | $$                                                                                    
|  $$$$$$/| $$/   \  $$ /$$$$$$| $$         | $$                                                                                    
 \______/ |__/     \__/|______/|__/         |__/                                                                                    
                                                                                                                                    
                                                                                                                                                                                                                                                                             
Originally For CyberPatiot, apt (Debain/Ubuntu) Linux images, Now includes RedHat/CentOS/Fedora, and Arch Linux. 
Updated for collegiate for CCDC and DoE CyberForce!
version: {version}                                                                                                                             
Made by DogBytes 2024 Revised by CalPoly: LeBroncoBytes 2026                                                                                                                                     
"""
    )


    print("\nREAD THE README BEFORE RUNNING THE SCRIPT!!")
    if input("I have read the readme and done the Forensics(y/n)").lower() == "y":
        print("continuing...")
    else:
        print("failed to pass readme/forensics check-- exiting...")
        exit()

    print("\n\n\n\n\n\n")
    if create_basic_files.cbf() != 0:
        print("New allow-list files were created. Edit them, then rerun the audit.")
        raise SystemExit(0)

    etc.print_banner("User Audit")
    
    human_users = useraudit.get_human_users()
    etc.print_small_title("Human Users On System")
    for user in human_users:
        print(f"{user}")
        
    # unused because of stabilzed users
    # unwanted_users = useraudit.get_unwanted_users()
    # if unwanted_users is not None:
    #     for user in unwanted_users:
    #         print(f"{user}")

    remove_users_waitlist, add_users_waitlist = useraudit.compare_users(human_users)

    etc.print_barrier()
    etc.print_small_title("Users to be edited")
    print(f"remove_users_waitlist: {remove_users_waitlist}")
    print(f"\nadd_users_waitlist: {add_users_waitlist}")
    etc.print_barrier()

    if input("Stabilize users? (y/N): ").lower() == "y":
        useraudit.stabilize_users(add_users_waitlist, remove_users_waitlist)
    else:
        print("Continuing...")


    if input("Set a new password for all human users? (y/N): ").lower() == "y":
        useraudit.change_user_passwords()
    else:
        print("Continuing...")

    etc.print_barrier()
    
    # Run the authsudouser script after user stabilization
    etc.print_banner("Managing Authorized SUDO Users")
    current_sudo_users = authsudouser.get_current_sudo_users()
    authorized_admin_users = authsudouser.get_authorized_admin_users()
    
    authsudouser.manage_sudo_users(current_sudo_users, authorized_admin_users)

    etc.print_barrier()
    
    # Run the disable_nonessential_services script
    etc.print_banner("Disabling Non-Essential Services")
    print("\nBefore you start. make sure you are sure you want to disable this service")
    print("you may not want to disable it, and could break the system. LOOK AT GOOGLE\nloading...")
    time.sleep(3) # here so people read, and not break everything lol
    disable_nonessential_services.main() 
    etc.print_barrier()

    etc.print_banner("Deleting Media Files in /home")
    print("make sure to do forensics before this, it does not crawl into / only /home.")
    print("cannot be undone.\nloading...")
    time.sleep(2) #again... to make sure it is read -_-
    delete_media_files.main()


    etc.print_banner("System Update and Upgrade")
    
    if input("Update and upgrade? (y/N): ").lower() == "y":
        update_upgrade.update_upgrade()
    else:
        print("Continuing...")

    etc.print_barrier()
    etc.print_banner("Running Ansible Playbook!")

    if input("Run the bundled Ansible hardening playbook? (N/y)").lower() == "y":
        ansible_runner.main()
    else:
        print("continuing...")

    print("Script is over... good luck fellow traveler")
