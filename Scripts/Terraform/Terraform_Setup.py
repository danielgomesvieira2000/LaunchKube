import subprocess

def check_terraform_installed():
    try:
        result = subprocess.run(
            ["terraform", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Terraform is installed.")
        return True
    except subprocess.CalledProcessError:
        print("Unkown error. Terraform may not be installed.")
        return False
    except FileNotFoundError:
        print("Terraform is not installed on this machine.")
        return False

if __name__ == "__main__":
    print("Please run main.py.")