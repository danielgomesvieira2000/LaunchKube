import os
import subprocess
from tkinter import messagebox

def terraform_run_gcp():
    try:
        init_result = subprocess.run(
            ['terraform', 'init'],
            capture_output=True,
            text=True,
            check=True
        )

        print(init_result.stdout)

        plan_result = subprocess.run(
            ['terraform', 'plan'],
            capture_output=True,
            text=True,
            check=True
        )

        print(plan_result.stdout)

        apply_result = subprocess.run(
            ['terraform', 'apply', '-auto-approve'],
            capture_output=True,
            text=True,
        )
        print(apply_result.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running Terraform: {e}")
        print(f"Command output:\n{e.output}")
        print(f"Command error output:\n{e.stderr}")
        messagebox.showerror(
            "Terraform error",
            f"Error: {e.stderr}\n"
        )
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def set_command_dir(teamname):
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    project_path = f"gcp_deployment\\{teamname}" if os.name == 'nt' else f"gcp_deployment/{teamname}"
    terraform_path = os.path.join(project_root, project_path)
    os.chdir(terraform_path)
    print(f"Changed directory to: {terraform_path}")

if __name__ == "__main__":
    print("Please run main.py.")
