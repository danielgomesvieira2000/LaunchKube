import os
import subprocess
import sys

from Scripts.GCP.GCP_Locate import locate_gcloud
from Scripts.GCP.GCP_Project import gcp_get_currentproject


def gcloud_set_location(teamname):
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    project_path = f"gcp_deployment\\{teamname}" if os.name == 'nt' else f"gcp_deployment/{teamname}"
    gcloud_path = os.path.join(project_root, project_path)
    os.chdir(gcloud_path)
    print(f"Changed directory to: {gcloud_path}")

def service_account_create(teamname):
    gcloud_path = locate_gcloud()
    project_id = gcp_get_currentproject()
    try:
        gcloud_create_sa = subprocess.run(
            [gcloud_path, 'iam', 'service-accounts', 'create', 'terraform', '--description="Service account for Terraform with owner permissions"', '--display-name="Terraform Service Account"'],
            capture_output=True,
            text=True,
            check=True
        )
        print(gcloud_create_sa.stdout)
    except Exception as e:
        print(f'Error: {e}')

    gcloud_permissions_sa = subprocess.run(
        [
            gcloud_path, 'projects', 'add-iam-policy-binding',
            f'{project_id}',
            f'--member=serviceAccount:terraform@{project_id}.iam.gserviceaccount.com',
            '--role=roles/owner'
        ],
        capture_output=True,
        text=True
    )

    gcloud_set_location(teamname)
    gcloud_get_credentials = subprocess.run(
        [
            gcloud_path, 'iam', 'service-accounts', 'keys', 'create',
            'credentials.json',
            f'--iam-account=terraform@{project_id}.iam.gserviceaccount.com'
        ],
        capture_output=True,
        text=True
    )

    print("STDOUT:", gcloud_get_credentials.stdout)
    print("STDERR:", gcloud_get_credentials.stderr)


def check_credentials(teamname):
    gcloud_set_location(teamname)
    return os.path.isfile('credentials.json')

if __name__ == "__main__":
    gcloud_set_location("team10")
    service_account_create("team10")