import subprocess
import os

def locate_gcloud():
    try:
        if os.name == 'nt':  #Windows
            where_result = subprocess.run(
                ["where.exe", "gcloud"],
                capture_output=True,
                text=True,
                check=True
            )
            gcloud_path = where_result.stdout.splitlines()[0]

            if gcloud_path.endswith("gcloud"):
                gcloud_path += ".cmd"
        else:  # Linux and others
            which_result = subprocess.run(
                ["which", "gcloud"],
                capture_output=True,
                text=True,
                check=True
            )
            gcloud_path = which_result.stdout.strip()

        return gcloud_path
    except subprocess.CalledProcessError:
        print("gcloud not found in PATH.")
        return None

if __name__ == "__main__":
    print("Please run main.py.")