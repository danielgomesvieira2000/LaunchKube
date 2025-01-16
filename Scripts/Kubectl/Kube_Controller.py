import subprocess
import tkinter.messagebox as messagebox
from Scripts.Cloudflare.Cloudflare_Request import update_dns_record
from Scripts.GCP.GCP_Project import gcp_get_currentregion
from Scripts.GCP.GCP_StaticIP import check_static_ip, create_static_ip, get_static_ip
from Scripts.Kubectl.Kube_Keycloak import check_realmfile_exists
from Scripts.Kubectl.Kube_Run import kube_set_location, kube_get_credentials, kube_secret_docker, kube_secret_db, \
    kube_cluster_update, kube_apply
from Scripts.Terraform.Terraform_Run import set_command_dir
from Scripts.Terraform.Terraform_VariableBuilder import get_variable_location


def kubectl_run(teamname, project_id):
    yaml_fill_keycloack(teamname, project_id)
    region = gcp_get_currentregion(teamname)

    if not check_static_ip(region):
        create_static_ip(region)

    try:
        terraform_file = get_variable_location(teamname, 'variables.tf')
    except Exception as e:
        messagebox.showerror("Error", f"Error getting the variables.tf file: {e}")
        return

    try:
        kube_set_location(teamname)
    except Exception as e:
        messagebox.showerror("Error", f"Error in finding the gcp_deployment project: {e}")
        return

    try:
        kube_get_credentials(project_id)
    except Exception as e:
        messagebox.showerror("Error", f"Error in getting kubectl credentials: {e}")

    try:
        if terraform_file:
            kube_secret_docker(terraform_file)
    except Exception as e:
        messagebox.showerror("Error", f"Error in adding docker secrets: {e}")

    try:
        if terraform_file:
            kube_secret_db(terraform_file)
    except Exception as e:
        messagebox.showerror("Error", f"Error in adding database secrets: {e}")

    if teamname == 'team15' or teamname == 'team10':
        kubectl_secret_keycloak = subprocess.run(
            ['kubectl', 'create', 'secret', 'generic', 'db-credentials-keycloak', '--from-literal=username=keycloak',
             '--from-literal=password=password',
             '--from-literal=database=keycloak'],
            capture_output=True,
            text=True,
        )
        print(kubectl_secret_keycloak.stdout)

    if teamname == 'team15':
        kubectl_secret_machikoro = subprocess.run(
            ['kubectl', 'create', 'secret', 'generic', 'mail-credentials',
             '--from-literal=password=CMm1CKdPRLria2h7',
             '--from-literal=email=machikoro@hotmail.com',
             '--from-literal=username=Machikoro Game'],
            capture_output=True,
            text=True,
        )
        print(kubectl_secret_machikoro.stdout)

    try:
        kube_cluster_update(project_id)
    except Exception as e:
        messagebox.showerror("Error", f"Error in updating kube cluster: {e}")

    kubectl_apply_nginx = subprocess.run(
        ['kubectl', 'apply', '-f',
         'https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml'],
        capture_output=True,
        text=True,
    )
    print(kubectl_apply_nginx.stdout)

    setup_nginx_https()

    try:
        kube_apply()
    except Exception as e:
        print('Probably just a warning.')

    if check_realmfile_exists(teamname):
        set_command_dir(teamname)
        kubectl_configmap_keycloak = subprocess.run(
            ['kubectl', 'create', 'configmap', 'keycloak-realm', '--from-file=realm-export.json'],
            capture_output=True,
            text=True,
        )
        print(kubectl_configmap_keycloak.stdout)

    ip = get_static_ip(region)
    update_dns_record(ip, teamname)

    kubectl_patch_ingress = subprocess.run(
        ['kubectl', 'patch', 'svc', 'ingress-nginx-controller', '-n', 'ingress-nginx', '-p',
         f'{{"spec": {{"loadBalancerIP": "{ip}"}}}}'],
        capture_output=True,
        text=True,
    )

def yaml_fill_keycloack(teamname, project_id):
    kube_set_location(teamname)
    update_cloud_sql_proxy_line('backend.yaml', project_id)
    update_cloud_sql_proxy_line('keycloak.yaml', project_id)

def update_cloud_sql_proxy_line(filename, project_id):
    target_container_name = "- name: cloud-sql-proxy"
    update_value = f'- "{project_id}:europe-central2:{project_id}-pg-instance"'

    with open(filename, 'r') as file:
        lines = file.readlines()

    updated = False
    for i, line in enumerate(lines):
        if target_container_name in line:
            base_indent = len(line) - len(line.lstrip())
            target_index = i + 5

            if target_index < len(lines):
                target_indent = len(lines[target_index]) - len(lines[target_index].lstrip())
                if target_indent == 0:
                    target_indent = base_indent + 2

                lines[target_index] = ' ' * target_indent + update_value + '\n'
                updated = True
                print(f"Updated line {target_index + 1}: {lines[target_index].strip()}")
                break

    if updated:
        with open(filename, 'w') as file:
            file.writelines(lines)
        print(f"Updated YAML file saved: {filename}")
    else:
        print("Target container block not found or file format is unexpected.")

def setup_nginx_https():
    kubectl_apply_nginx = subprocess.run(
        ['kubectl', 'apply', '--validate=false', '-f',
         'https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.crds.yaml'],
        capture_output=True,
        text=True,
    )
    print(kubectl_apply_nginx.stdout)

    kubectl_apply_nginx = subprocess.run(
        ['kubectl', 'apply', '-f',
         'https://github.com/jetstack/cert-manager/releases/latest/download/cert-manager.yaml'],
        capture_output=True,
        text=True,
    )
    print(kubectl_apply_nginx.stdout)

if __name__ == "__main__":
    print('Please run main.py')