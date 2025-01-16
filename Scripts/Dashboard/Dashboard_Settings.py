from Scripts.GCP.GCP_Authentication import gcp_get_current_user
import tkinter as tk
from tkinter import ttk
from Scripts.GCP.GCP_Project import gcp_get_projects, gcp_get_currentproject, gcp_set_currentproject, gcp_createproject, \
    gcp_check_valid_billing_status


def open_create_project_popup(app):
    popup = tk.Toplevel(app)
    popup.title("Create New Project")
    popup.geometry("300x150")
    popup.configure(bg="white")

    project_name_label = tk.Label(
        popup,
        text="Enter name for new project:",
        font=("Arial", 12),
        bg="white",
        fg="#333333",
    )
    project_name_label.pack(pady=10)

    new_project_name_var = tk.StringVar()
    project_name_entry = tk.Entry(
        popup,
        textvariable=new_project_name_var,
        font=("Arial", 12),
        width=20,
    )
    project_name_entry.pack(pady=5)

    def on_ok_button_click():
        new_project_name = new_project_name_var.get().strip()
        if new_project_name:
            gcp_createproject(new_project_name)
            popup.destroy()
        else:
            error_label.config(text="Project name cannot be empty.", fg="red")

    ok_button = tk.Button(
        popup,
        text="OK",
        font=("Arial", 12),
        bg="#2ECC71",
        fg="white",
        relief=tk.FLAT,
        command=on_ok_button_click,
    )
    ok_button.pack(pady=10)

    error_label = tk.Label(
        popup,
        text="",
        font=("Arial", 10),
        bg="white",
        fg="red",
    )
    error_label.pack()
    app.wait_window(popup)

def show_settings(app):
    app.clear_main_content()

    current_project = gcp_get_currentproject()
    billing_status = gcp_check_valid_billing_status()
    print(f'Billing Status: {billing_status}')
    app.current_project_var.set(current_project)

    settings_frame = tk.Frame(app.main_content, bg="white")
    settings_frame.pack(fill=tk.X, pady=20, padx=20, anchor="w")

    # Project Settings
    project_label = tk.Label(
        settings_frame,
        text="Project:",
        font=("Arial", 12),
        bg="white",
        fg="#333333",
    )
    project_label.pack(side=tk.LEFT, padx=(0, 10))
    project_dropdown = ttk.Combobox(
        settings_frame,
        textvariable=app.current_project_var,
        state="readonly",
        font=("Arial", 12),
        width=30,
    )
    project_dropdown.pack(side=tk.LEFT)
    fill_dropdown_projects(project_dropdown)

    plus_button = tk.Button(
        settings_frame,
        text=" + ",
        font=("Arial", 12),
        bg="#2ECC71",
        fg="white",
        relief=tk.FLAT,
        command=lambda: open_create_project_popup(app),
    )
    plus_button.pack(side=tk.LEFT, padx=10)

    # Billing status
    billing_status_label = tk.Label(
        settings_frame,
        text="",
        font=("Arial", 12),
        bg="white",
        fg="green" if billing_status else "red",
    )
    billing_status_label.pack(side=tk.LEFT, padx=10)
    billing_status_label.config(
        text="Billing account enabled" if billing_status else "Billing account is NOT enabled yet!"
    )

    def on_project_change(event):
        selected_project = app.current_project_var.get()
        gcp_set_currentproject(selected_project)
        updated_billing_status = gcp_check_valid_billing_status()
        billing_status_label.config(
            text="Billing account enabled" if updated_billing_status else "Billing account is NOT enabled yet!",
            fg="green" if updated_billing_status else "red",
        )

    project_dropdown.bind("<<ComboboxSelected>>", on_project_change)

    current_user = gcp_get_current_user()
    if current_user:
        user_label = tk.Label(
            app.main_content,
            text=f"Logged in as {current_user}",
            font=("Arial", 10),
            bg="white",
            fg="#333333",
        )
        user_label.pack(side=tk.BOTTOM, pady=20)

def fill_dropdown_projects(project_dropdown):
    current_project = gcp_get_currentproject()
    project_dropdown["values"] = []
    projects = gcp_get_projects()
    project_dropdown["values"] = projects

    if projects:
        project_dropdown.set(current_project)
    else:
        project_dropdown.set("No projects available")


