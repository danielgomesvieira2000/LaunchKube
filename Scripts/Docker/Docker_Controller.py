import os
from tkinter import messagebox

from Scripts.Docker.Docker_Run import docker_run_local
from Scripts.Docker.Docker_Setup import check_docker_installed, check_docker_running, check_docker_sudo


def local_deploy(deploy_name):
    return docker_run_local(deploy_name)

def docker_check():
    if not check_docker_installed():
        messagebox.showerror(
            "Docker not found",
            f"It looks like docker is not running or not installed on your pc.\n"
            f"Please make sure to properly installed and start docker."
        )
        return False
    if os.name == 'nt':  # Windows
        if not check_docker_running():
            messagebox.showerror(
                "Docker is not running",
                f"It looks like docker is not running on your pc.\n"
                f"Please make sure to properly start docker."
            )
            return False
    if os.name != 'nt':  # Everything but windows
        if not check_docker_sudo():
            messagebox.showerror(
                "Docker is not running without sudo",
                f"It looks like docker requires sudo to run.\n"
                f"Please make sure to give docker permissions to run without sudo."
            )
            return False
    return True

if __name__ == "__main__":
    print("Running Controller.")