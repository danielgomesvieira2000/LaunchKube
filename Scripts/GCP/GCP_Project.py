import subprocess
from Scripts.GCP.GCP_Locate import locate_gcloud
import re
from Scripts.Kubectl.Kube_Run import get_variable_value
from Scripts.Terraform.Terraform_VariableBuilder import get_variable_location


def gcp_get_projects():
    try:
        gcloud_path = locate_gcloud()
        result = subprocess.run(
            [gcloud_path, 'projects', 'list', '--format=value(projectId)'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            projects = result.stdout.strip().split('\n')
            return projects
        else:
            print("Error fetching projects:", result.stderr)
            return []
    except Exception as e:
        print(f"An error occurred while fetching projects: {e}")
        return []

def gcp_get_currentproject():
    gcloud_path = locate_gcloud()
    try:
        result = subprocess.run(
            [gcloud_path, 'config', 'get-value', 'project'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print("Error fetching current project:", result.stderr)
            return None
    except Exception as e:
        print(f"An error occurred while fetching current project: {e}")
        return None

def gcp_set_currentproject(project):
    gcloud_path = locate_gcloud()
    try:
        result = subprocess.run(
            [gcloud_path, 'config', 'set', 'project', project],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"Project set to: {project}")
            return True
        else:
            print("Error setting current project:", result.stderr)
            return False
    except Exception as e:
        print(f"An error occurred while setting current project: {e}")
        return False

def gcp_createproject(project_name):
    gcloud_path = locate_gcloud()
    project_id = project_name.lower().replace(" ", "-")  # Replace spaces with dashes and lowercase

    if not validate_project_id(project_id):
        print(f"Error: '{project_id}' is not a valid project ID.")
        return False

    try:
        result = subprocess.run(
            [gcloud_path, "projects", "create", project_id, "--name", project_name],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"Project '{project_name}' created successfully with project ID '{project_id}'.")
            return True
        else:
            print(f"Failed to create project. Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"An error occurred while creating the project: {e}")
        return False

def validate_project_id(project_id):
    # Must start with a lowercase letter
    # Can contain lowercase letters, digits, and hyphens
    # Must be between 6 and 30 characters long
    pattern = r'^[a-z][a-z0-9-]{5,29}$'
    if re.match(pattern, project_id):
        return True
    else:
        return False

def gcp_check_valid_billing_status():
    gcloud_path = locate_gcloud()
    try:
        current_project = gcp_get_currentproject()
        if not current_project:
            print("No current project set.")
            return False

        result = subprocess.run(
            [gcloud_path, 'beta', 'billing', 'projects', 'describe', current_project, '--format=value(billingEnabled)'],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            billing_enabled = result.stdout.strip()
            if billing_enabled.lower() == "true":
                return True
            else:
                print(f"Billing is not enabled for project: {current_project}")
                return False
        else:
            print(f"Error checking billing status: {result.stderr}")
            return False
    except Exception as e:
        print(f"An error occurred while checking billing status: {e}")
        return False

def gcp_get_currentregion(teamname):
    terraform_file = get_variable_location(teamname, 'variables.tf')
    return get_variable_value('region', terraform_file)

def gcp_get_currentzone(teamname):
    terraform_file = get_variable_location(teamname, 'variables.tf')
    return get_variable_value('zone', terraform_file)

if __name__ == "__main__":
    region = gcp_get_currentregion('team15')
    print(region)
