from tkinter import messagebox

from Scripts.Kubectl.Kube_Setup import check_kubectl_installed
from Scripts.Terraform.Terraform_Setup import check_terraform_installed


def check_ready_deplyoment():
    if not check_kubectl_installed():
        messagebox.showerror(
            "Kubectl not found",
            f"It looks like kubectl is not installed on your pc.\n"
            f"Please make sure to properly install kubectl."
        )
        return False
    if not check_terraform_installed():
        messagebox.showerror(
            "Terraform not found",
            f"It looks like Terraform is not installed on your pc.\n"
            f"Please make sure to properly install Terraform."
        )
        return False

    print("Ready to deploy.")
    return True