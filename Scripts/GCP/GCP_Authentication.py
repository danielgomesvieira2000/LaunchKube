import subprocess
from Scripts.GCP.GCP_Locate import locate_gcloud

def is_logged_in():
    gcloud_path = locate_gcloud()
    try:
        result = subprocess.run(
            [gcloud_path, "auth", "list", "--format=value(account)"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0 and result.stdout.strip():
            print("Already logged in as:", result.stdout.strip())
            return True
        else:
            print("No active account found. Not logged in.")
            return False

    except Exception as e:
        print(f"An error occurred while checking login status: {e}")
        return False

def gcp_login():
    if is_logged_in():
        print("Skipping login; already authenticated.")
        return True

    gcloud_path = locate_gcloud()
    try:
        result = subprocess.run(
            [gcloud_path, "auth", "login"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("Logged in successfully.")
            return True
        else:
            print("Failed to log in.")
            print("Error:", result.stderr)
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def gcp_get_current_user():
    if is_logged_in():
        gcloud_path = locate_gcloud()
        result = subprocess.run(
            [gcloud_path, "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            current_user = result.stdout.strip()
            return current_user
        else:
            print("Error fetching current user:", result.stderr)
            return None
    else:
        print("User is not logged in.")
        return None

if __name__ == "__main__":
    print("Please run main.py.")