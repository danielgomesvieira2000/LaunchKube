import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox
import os
import threading

from Scripts.Dashboard.Dashboard_Loading import show_loading
from Scripts.GCP.GCP_Controller import gcp_check_billing
from Scripts.GCP.GCP_Project import gcp_get_currentproject
from Scripts.GCP.GCP_ServiceAccount import check_credentials, service_account_create
from Scripts.Kubectl.Kube_Controller import kubectl_run
from Scripts.Kubectl.Kube_Destroy import kube_destroy_gcp
from Scripts.Kubectl.Kube_Ingress import get_ingress_hosts
from Scripts.Terraform.Terraform_Controller import terraform_run
from Scripts.Terraform.Terraform_Destory import terraform_destroy_gcp
from Scripts.Deployment.Deployment_Check import check_ready_deplyoment
from Scripts.Docker.Docker_Controller import local_deploy, docker_check
from Scripts.Docker.Docker_Manage import docker_get_list, docker_delete_all
from Scripts.Terraform.Terraform_VariableBuilder import check_if_variables_exist, get_secret_variables, \
    set_secret_variables

def show_deploy_local(app):
    app.clear_main_content()

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    teams_file_path = f"local_deployment\\" if os.name == 'nt' else f"local_deployment/"
    projects_path = os.path.join(project_root, teams_file_path)

    def get_project_names():
        if os.path.exists(projects_path):
            return [folder for folder in os.listdir(projects_path) if os.path.isdir(os.path.join(projects_path, folder))]
        return []

    deploy_frame = tk.Frame(app.main_content, bg="white")
    deploy_frame.pack(fill=tk.X, pady=20, padx=20, anchor="w")

    containers_label = tk.Label(
        deploy_frame,
        text="",
        font=("Arial", 12),
        bg="white",
        fg="#333333",
    )
    containers_label.pack(fill=tk.X, pady=(0, 10))

    button_frame = tk.Frame(deploy_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=(10, 0))

    project_names = get_project_names()
    selected_project = tk.StringVar()

    if project_names:
        selected_project.set(project_names[0])
    else:
        selected_project.set("Select a team")

    dropdown_menu = ttk.Combobox(
        button_frame,
        textvariable=selected_project,
        values=project_names,
        state="readonly",
        font=("Arial", 12),
    )
    dropdown_menu.pack(side=tk.LEFT, padx=(0, 10))

    clear_all_button = tk.Button(
        button_frame,
        text="Clear All",
        font=("Arial", 12),
        bg="#ff2c2c",
        fg="white",
        command=lambda: deploy_local_clear(containers_label),
    )
    clear_all_button.pack(side=tk.LEFT, padx=(0, 10))  # Add space between buttons

    create_button = tk.Button(
        button_frame,
        text="Local run selected team",
        font=("Arial", 12),
        bg="#28a745",
        fg="white",
        command=lambda: deploy_local(app, containers_label, selected_project.get()),
    )
    create_button.pack(side=tk.LEFT, padx=(0, 10))  # Add space between buttons
    fill_containers_label(containers_label)

def show_deploy(app):
    app.clear_main_content()

    deploy_frame = tk.Frame(app.main_content, bg="white")
    deploy_frame.pack(fill=tk.BOTH, pady=20, padx=20, expand=True)

    button_frame = tk.Frame(deploy_frame, bg="white")
    button_frame.pack(expand=True)  # Expand to fill and center the content

    deploy_online_button = tk.Button(
        button_frame,
        text="Deploy Online",
        font=("Arial", 12),
        bg="#007BFF",
        fg="white",
        command=lambda: start_deploy_gcp(app),
    )
    deploy_online_button.pack(side=tk.LEFT, padx=10)

    deploy_local_button = tk.Button(
        button_frame,
        text="Deploy Locally",
        font=("Arial", 12),
        bg="#28a745",
        fg="white",
        command=lambda: start_deploy_local(app),
    )
    deploy_local_button.pack(side=tk.LEFT, padx=10)

def show_deploy_gcp(app):
    app.clear_main_content()

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    teams_file_path = f"gcp_deployment\\" if os.name == 'nt' else f"gcp_deployment/"
    projects_path = os.path.join(project_root, teams_file_path)

    hosts = get_ingress_hosts()

    def get_project_names_local():
        if os.path.exists(projects_path):
            return [folder for folder in os.listdir(projects_path) if
                    os.path.isdir(os.path.join(projects_path, folder))]
        return []

    deploy_frame = tk.Frame(app.main_content, bg="white")
    deploy_frame.pack(fill=tk.X, pady=20, padx=20, anchor="w")

    containers_label = tk.Label(
        deploy_frame,
        text="No deployment online",
        font=("Arial", 12),
        bg="white",
        fg="#333333",
    )
    containers_label.pack(fill=tk.X, pady=(0, 10))

    button_frame = tk.Frame(deploy_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=(10, 0))

    project_names = get_project_names_local()
    selected_project = tk.StringVar()

    if project_names:
        selected_project.set(project_names[0])
    else:
        selected_project.set("Select a team")

    if hosts:
        containers_label.config(text=f"Deployed: {hosts}")
    else:
        containers_label.config(text="Nothing deployed.")

    dropdown_menu = ttk.Combobox(
        button_frame,
        textvariable=selected_project,
        values=project_names,
        state="readonly",
        font=("Arial", 12),
    )
    dropdown_menu.pack(side=tk.LEFT, padx=(0, 10))

    clear_all_button = tk.Button(
        button_frame,
        text="Take offline",
        font=("Arial", 12),
        bg="#ff2c2c",
        fg="white",
        command=lambda: deploy_gcp_delete(app, selected_project.get()),
    )
    clear_all_button.pack(side=tk.LEFT, padx=(0, 10))  # Add space between buttons

    deploy_button = tk.Button(
        button_frame,
        text="Deploy selected team",
        font=("Arial", 12),
        bg="#28a745",
        fg="white",
        command=lambda: deploy_gcp(app, selected_project.get()),
    )
    deploy_button.pack(side=tk.LEFT, padx=(0, 10))


def show_variable_screen(app, teamname):
    app.clear_main_content()
    secret_variables = get_secret_variables(teamname)

    frame = tk.Frame(app.main_content, bg="white")
    frame.pack(fill=tk.X, pady=20, padx=20, anchor="w")
    secret_values = []

    for idx, variable in enumerate(secret_variables):
        tk.Label(frame, text=variable).grid(row=idx, column=0, padx=10, pady=5, sticky="e")

        entry = tk.Entry(frame, width=40)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        secret_values.append(entry)

    def add_variables():
        values = [entry.get() for entry in secret_values]
        set_secret_variables(teamname, secret_variables, values, gcp_get_currentproject())
        show_deploy_gcp(app)

    add_button = tk.Button(frame, text="Add variables", command=add_variables)
    add_button.grid(row=len(secret_variables), column=0, columnspan=2, pady=10)


def start_deploy_local(app):
    if docker_check():
        show_deploy_local(app)

def start_deploy_gcp(app):

    if not gcp_check_billing():
        app.messagebox.showerror("Please setup billing on project.")
        return

    if not check_ready_deplyoment():
        app.messagebox.showerror("Not ready for deployment. Missing installed components.")
        return

    def load_settings():
        time.sleep(5)
        app.after(0, lambda: show_deploy_gcp(app))

    show_loading(app, "Loading GCP Deployment... THIS MAY TAKE A FEW SECONDS")
    threading.Thread(target=load_settings, daemon=True).start()

def deploy_local(app, containers_label, teamname):
    if docker_check():
        def task():
            app.after(0, lambda: containers_label.config(text="Deploying locally..."))
            local_deploy(teamname)
            fill_containers_label(containers_label)

        threading.Thread(target=task).start()

def deploy_gcp(app, teamname):
    if not check_if_variables_exist(teamname):
        messagebox.showerror(
            "Secret variables not filled in yet.",
            f"Please fill in your secret credentials. {teamname}"
        )
        show_variable_screen(app, teamname)
        return

    if not check_credentials(teamname):
        service_account_create(teamname)

    def task():
        show_loading(app, "Setting up Terraform... (Can take up to 30 minutes...)")
        terraform_run(teamname)

        show_loading(app, "Setting up Kubernetes...")
        kubectl_run(teamname, gcp_get_currentproject())

        show_deploy_gcp(app)

    threading.Thread(target=task).start()

def fill_containers_label(containers_label):
    docker_stout = docker_get_list()
    if len(docker_stout) < 1:
        docker_stout = 'No containers running'
    else:
        container_details = []
        for stack_name in docker_stout:
            container_output = subprocess.run(
                ['docker', 'ps', '--filter', f'label=com.docker.compose.project={stack_name}', '--format',
                 '{{.Ports}}'],
                capture_output=True,
                text=True
            )
            # string formatting
            ports = container_output.stdout.strip().replace('"', '')
            port_list = []
            for line in ports.split('\n'):
                if line:
                    port = line.split('->')[0].split(':')[-1]
                    port_list.append(port)
            ports_string = ', '.join(port_list)
            if not ports_string:
                ports_string = 'No ports exposed'
            container_details.append(f"Running: {stack_name} on ports: {ports_string}")
        docker_stout = '\n'.join(container_details)
    containers_label.config(text=docker_stout)

def deploy_local_clear(containers_label):
    docker_delete_all()
    clear_containers_label(containers_label)

def deploy_gcp_delete(app, teamname):
    def task():
        show_loading(app, "Deleting kubernetes setup...")
        kube_destroy_gcp()

        show_loading(app, "Performing terraform destroy... (Can take up to 15 minutes...)")
        terraform_destroy_gcp(teamname)

        show_loading(app, "Finishing up...")
        show_deploy_gcp(app)

    threading.Thread(target=task).start()

def clear_containers_label(containers_label):
    containers_label.config(text="No containers running")

if __name__ == "__main__":
    print("Please run main.py.")