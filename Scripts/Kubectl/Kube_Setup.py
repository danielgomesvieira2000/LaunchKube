import subprocess

def check_kubectl_installed():
    try:
        result = subprocess.run(
            ["kubectl", "version", "--client"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("kubectl is installed.")
        return True
    except subprocess.CalledProcessError:
        print("Unkown error. Kubectl may not be installed.")
        return False
    except FileNotFoundError:
        print("Kubectl is not installed on this machine.")
        return False

if __name__ == "__main__":
    print("Please run main.py.")