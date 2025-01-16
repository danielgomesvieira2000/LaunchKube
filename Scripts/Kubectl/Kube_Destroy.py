import json
import os
import subprocess
from tkinter import messagebox

from Scripts.GCP.GCP_Locate import locate_gcloud


def kube_destroy_gcp():
    try:
        try:
            secrets = get_secrets()
        except Exception as e:
            messagebox.showerror("Error", f"Error in getting kubectl secrets: {e}")
        try:
            deployments = get_deployments()
        except subprocess.SubprocessError as e:
            messagebox.showerror("Error", f"Error in getting kubectl deployments: {e}")
        try:
            services = get_services()
        except subprocess.SubprocessError as e:
            messagebox.showerror("Error", f"Error in getting kubectl services: {e}")

        for secret in secrets:
            try:
                delete_secret = subprocess.run(
                    ['kubectl', 'delete', 'secret', secret],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.SubprocessError as e:
                messagebox.showerror("Error", f"Error in deleting kubectl credentials: {e}")

        for deployment in deployments:
            try:
                delete_deployment = subprocess.run(
                    ['kubectl', 'delete', 'deployment', deployment],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.SubprocessError as e:
                messagebox.showerror("Error", f"Error in deleting kubectl deployment: {e}")

        for service in services:
            try:
                delete_service = subprocess.run(
                    ['kubectl', 'delete', 'service', service],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.SubprocessError as e:
                messagebox.showerror("Error", f"Error in deleting kubectl services: {e}")

        delete_all_instances()

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running kubectl: {e}")
        print(f"Command output:\n{e.output}")
        print(f"Command error output:\n{e.stderr}")
        messagebox.showerror(
            "Kubectl error",
            f"Error: {e.stderr}\n"
        )
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_services():
    result = subprocess.run(
        ['kubectl', 'get', 'services', '-o', 'jsonpath={.items[*].metadata.name}'],
        capture_output=True,
        text=True,
        check=True
    )
    services = result.stdout.strip().split()
    return services

def get_deployments():
    result = subprocess.run(
        ['kubectl', 'get', 'deployments', '-o', 'jsonpath={.items[*].metadata.name}'],
        capture_output=True,
        text=True,
        check=True
    )
    deployments = result.stdout.strip().split()
    return deployments

def get_secrets():
    result = subprocess.run(
        ['kubectl', 'get', 'secrets', '-o', 'jsonpath={.items[*].metadata.name}'],
        capture_output=True,
        text=True,
        check=True
    )
    secrets = result.stdout.strip().split()
    return secrets


def list_instances():
    try:
        gcloud_path = locate_gcloud()
        result = subprocess.run(
            [gcloud_path, "compute", "instances", "list", "--format=json"],
            capture_output=True,
            text=True,
            check=True
        )
        instances = json.loads(result.stdout)
        return instances
    except subprocess.CalledProcessError as e:
        print(f"Error listing instances: {e.stderr}")
        return []


def delete_instance(instance_name, zone):
    try:
        gcloud_path = locate_gcloud()
        subprocess.run(
            [gcloud_path, "compute", "instances", "delete", instance_name, "--zone", zone, "--quiet"],
            check=True
        )
        print(f"Deleted instance: {instance_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting instance {instance_name}: {e.stderr}")


def delete_all_instances():
    instances = list_instances()
    if not instances:
        print("No instances found.")
        return

    print(f"Found {len(instances)} instances. Deleting them...")
    for instance in instances:
        instance_name = instance["name"]
        zone = instance["zone"].split("/")[-1]
        delete_instance(instance_name, zone)


if __name__ == "__main__":
    secrets = get_secrets()
    deployments = get_deployments()
    services = get_services()

    print(secrets)
    print(deployments)
    print(services)
