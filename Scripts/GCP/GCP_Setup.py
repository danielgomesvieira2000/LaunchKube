import os
import subprocess
from Scripts.GCP.GCP_Locate import locate_gcloud

def check_gcloud_installed():
    gcloud_path = locate_gcloud()

    if not gcloud_path:
        return False

    try:
        version_result = subprocess.run(
            [gcloud_path, "--version"],
            capture_output=True,
            text=True
        )

        return version_result.returncode == 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def gcloud_check_beta_installed():
    gcloud_path = locate_gcloud()
    try:
        result = subprocess.run(
            [gcloud_path, 'components', 'list', '--format=value(id,state)'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            components = result.stdout.strip().split('\n')
            for component in components:
                if component.startswith('beta') and 'Installed' in component:
                    return True
            print("The 'beta' component is not installed.")
            return False
        else:
            print(f"Error checking gcloud components: {result.stderr}")
            return False
    except Exception as e:
        print(f"An error occurred while checking gcloud components: {e}")
        return False

## NEEDED FOR BILLING STATUS, MUST BE RAN AS ADMINISTRATOR
def gcloud_install_beta():
    gcloud_path = locate_gcloud()
    try:
        print("Attempting to install the 'beta' component...")
        result = subprocess.run(
            [gcloud_path, 'components', 'install', 'beta', '--quiet'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("The 'beta' component was installed successfully.")
            return True
        else:
            print(f"Error installing 'beta' component: {result.stderr}")
            return False
    except Exception as e:
        print(f"An error occurred while installing 'beta' component: {e}")
        return False

def check_gcloud_connection():
    # ping console.cloud.google.com

    option = '-n' if os.name == 'nt' else '-c'

    result = subprocess.run(
        ['ping', 'console.cloud.google.com', option, '1'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    print("Please run main.py.")