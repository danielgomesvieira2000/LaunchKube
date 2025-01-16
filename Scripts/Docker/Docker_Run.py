import os
import subprocess
from tkinter import messagebox
import re

def docker_run_local(deploy_name):
    try:
        current_file_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        compose_file_path = f"local_deployment\\{deploy_name}" if os.name == 'nt' else f"local_deployment/{deploy_name}"
        docker_compose_path = os.path.join(project_root, compose_file_path)
        os.chdir(docker_compose_path)
        print(f"Changed directory to: {docker_compose_path}")

        run_result = subprocess.run(
            ['docker-compose', 'up', '-d'],
            capture_output=True,
            text=True,
            check=True
        )
        print(run_result.stdout)
        return run_result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running docker-compose: {e}")
        print(f"Command output:\n{e.output}")
        print(f"Command error output:\n{e.stderr}")
        if "access forbidden" in e.stderr.lower():
            messagebox.showerror(
                "Docker permission denied",
                "It looks like Docker is not logged in to your Gitlab account.\n"
                "Please make sure you are logged in and have the correct permissions to pull the image you are trying to run."
            )
        if "ports are not available" in e.stderr.lower():
            match = re.search(r"0\.0\.0\.0:(\d+)", e.stderr.lower())
            port = match.group(1)
            messagebox.showerror(
                f"Docker Port {port} not available",
                f"It looks like you are tying to deploy on port {port} that is not available.\n"
                "Please make sure the ports are not in use or try to deploy to another port."
            )
        if "no configuration file provided" in e.stderr.lower():
            messagebox.showerror(
                "Docker compose file not found",
                f"It looks like Docker can't find the docker compose file inside of the {deploy_name} folder.\n"
                "Please make sure there is a valid docker compose file inside."
            )
        if "empty compose file" in e.stderr.lower():
            messagebox.showerror(
                "Docker compose file empty",
                f"It looks like your docker compose file inside of the {deploy_name} folder is empty.\n"
                "Please make sure there is a valid docker compose file inside."
            )
        else :
            messagebox.showerror(
                "Docker compose error",
                f"Error: {e.stderr}\n"
            )
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    print("Please run main.py.")
