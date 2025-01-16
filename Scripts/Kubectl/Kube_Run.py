import os
import subprocess
import re
from time import sleep

from Scripts.GCP.GCP_Locate import locate_gcloud
from Scripts.Terraform.Terraform_VariableBuilder import get_variable_location

def kube_set_location(teamname):
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    project_path = f"gcp_deployment\\{teamname}\\yaml_files" if os.name == 'nt' else f"gcp_deployment/{teamname}/yaml_files"
    terraform_path = os.path.join(project_root, project_path)
    os.chdir(terraform_path)
    print(f"Changed directory to: {terraform_path}")

def kube_get_credentials(project_id):
    gcloud_path = locate_gcloud()
    kubectl_get_cred = subprocess.run(
        [gcloud_path, 'container', 'clusters', 'get-credentials', f'{project_id}-gke', '--region', 'europe-central2-a',
         '--project', project_id],
        capture_output=True,
        text=True,
        check=True
    )

def get_variable_value(variable_name, tf_file_path):
    with open(tf_file_path, 'r') as file:
        content = file.read()

    pattern = rf'variable\s+"{variable_name}"\s+\{{[^}}]*?default\s+=\s+"([^"]+)"'
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()
    else:
        raise ValueError(f"Variable '{variable_name}' not found in {tf_file_path}")

def kube_secret_docker(tf_file_path):
    docker_registry_username = get_variable_value('docker_registry_username', tf_file_path)
    docker_registry_password = get_variable_value('docker_registry_password', tf_file_path)
    registry_server = get_variable_value('registry_server', tf_file_path)

    kubectl_secrets_image = subprocess.run(
        ['kubectl', 'create', 'secret', 'docker-registry', 'gitlab-registry-secret',
         f'--docker-server={registry_server}',
         f'--docker-username={docker_registry_username}',
         f'--docker-password={docker_registry_password}'
         ],
        capture_output=True,
        text=True,
        check=True
    )
    print(kubectl_secrets_image.stdout)

def kube_secret_db(tf_file_path):
    db_username = get_variable_value('db_user', tf_file_path)
    db_password = get_variable_value('db_password', tf_file_path)
    db_name = get_variable_value('db_name', tf_file_path)

    kubectl_secrets_db = subprocess.run(
        ['kubectl', 'create', 'secret', 'generic', 'db-credentials',
         f'--from-literal=username={db_username}',
         f'--from-literal=password={db_password}',
         f'--from-literal=database={db_name}'],
        capture_output=True,
        text=True,
        check=True
    )
    print(kubectl_secrets_db.stdout)

def kube_serviceacc(project_id):
    kubectl_service = subprocess.run(
        ['kubectl', 'annotate', 'serviceaccount', 'default',
         f'iam.gke.io/gcp-service-account=gke-cluster-minimal-sa@{project_id}.iam.gserviceaccount.com'],
        capture_output=True,
        text=True,
        check=True
    )
    print(kubectl_service.stdout)

def kube_cluster_update(project_id):
    gcloud_path = locate_gcloud()
    kube_update = subprocess.run(
        [gcloud_path, 'container', 'clusters', 'update', f'{project_id}-gke', '--location=europe-central2-a',
         f'--workload-pool={project_id}.svc.id.goog'],
        capture_output=True,
        text=True,
        check=True
    )
    print(kube_update.stdout)

def kube_apply():
    apply_result = subprocess.run(
        ['kubectl', 'apply', '-f', '.'],
        capture_output=True,
        text=True,
    )
    print(apply_result.stdout)

    sleep(360)

    apply_result = subprocess.run(
        ['kubectl', 'apply', '-f', '.'],
        capture_output=True,
        text=True
    )
    print(apply_result.stdout)
    print(apply_result.stderr)

if __name__ == "__main__":
    terraform_file = get_variable_location('team15', 'variables.tf')
    docker_registry_username = get_variable_value('docker_registry_username', terraform_file)
    print(docker_registry_username)

