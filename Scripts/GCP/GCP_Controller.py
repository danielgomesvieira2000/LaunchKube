import sys
from tkinter import messagebox
from Scripts.GCP.GCP_Authentication import gcp_login
from Scripts.GCP.GCP_Project import gcp_check_valid_billing_status
from Scripts.GCP.GCP_Setup import check_gcloud_installed, gcloud_check_beta_installed, gcloud_install_beta, \
    check_gcloud_connection


def gcp_check_connection():
    if not check_gcloud_connection():
        messagebox.showerror(
            "Could not connect to Google Cloud Platform",
            f"You must have internet connection in order to deploy.\n"
            f"If you have an internet connection, please check the Google Cloud Platform status."
        )
        sys.exit("Exiting program: Login failed.")

def gcp_check_auth():
    if not gcp_login():
        messagebox.showerror(
            "Login was not successful",
            f"You need to be logged in on a Google Cloud Platform account.\n"
            f"Please log in when the website pops up."
        )
        sys.exit("Exiting program: Login failed.")

def gcp_check_installed():
    if not check_gcloud_installed():
        messagebox.showerror(
            "Google Cloud Was Not Correctly Installed",
            f"The gcloud commands were not found on your system.\n"
            f"Please ensure gcloud is installed correctly."
        )
        sys.exit("Exiting program: gcloud commands not found.")

def gcp_setup():
    gcp_check_connection()
    gcp_check_installed()
    gcp_check_auth()

def gcp_check_billing():
    if not gcp_check_valid_billing_status():
        messagebox.showerror(
            "No valid billing",
            f"The gcloud project you are using has no linked billing account.\n"
            f"You need to have an active billing account to be able to deploy."
        )
        return False
    return True

if __name__ == "__main__":
    print("Running Controller.")