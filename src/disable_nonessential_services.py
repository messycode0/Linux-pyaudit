import subprocess

def get_running_services():
    """Retrieve a list of running services."""
    try:
        result = subprocess.run(['systemctl', 'list-units', '--type=service', '--state=running', '--no-legend', '--plain'], 
                                capture_output=True, text=True, check=True)
        return [line.split()[0] for line in result.stdout.splitlines() if line.split()]
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error retrieving running services: {e}")
        return []

def is_service_essential(service_name):
    """Determine if a service is essential. Modify this list as needed."""
    # Cups may not be needed... But ill leave it in there. you can disable it manully if you wish.
    essential_services = {'systemd', 'dbus', 'NetworkManager', 'cron', 'udev', 'rsyslog', 'lightdm', 'pulseaudio', 'cups', 'ssh', 'systemd-journald'}
    base_name = service_name.removesuffix('.service')
    return base_name in essential_services

def disable_service(service_name):
    """Disable and stop a service."""
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', service_name], check=True)
        subprocess.run(['sudo', 'systemctl', 'disable', service_name], check=True)
        print(f"Service {service_name} has been stopped and disabled.")
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"Error disabling service {service_name}: {e}\n\n:( very sad")

def main():
    running_services = get_running_services()
    
    for service in running_services:
        if not is_service_essential(service):
            user_input = input(f"SERVICE: {service} is running.\nDisable and stop? (N/y): ").strip().lower()
            if user_input == 'y' or user_input == 'yes':
                disable_service(service)
            else:
                print(f"Continuing with {service} running.")

if __name__ == "__main__":
    main()
