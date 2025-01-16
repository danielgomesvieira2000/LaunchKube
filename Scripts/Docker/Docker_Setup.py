import subprocess

def check_docker_installed():
    try:
        result = subprocess.run(
            ["docker", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("Docker is installed.")
        return True
    except subprocess.CalledProcessError:
        print("Unkown error. Docker may not be installed.")
        return False
    except FileNotFoundError:
        print("Docker is not installed on this machine.")
        return False

def check_docker_running():
    try:
        result = subprocess.run(
            ["docker", "info"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Docker is running.")
        return True
    except subprocess.CalledProcessError:
        print("Docker is not running.")
        return False
    except FileNotFoundError:
        print("Docker is not installed.")
        return False

def check_docker_sudo():
    try:
        result = subprocess.run(
            ["docker", "ps"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Docker is setup correctly.")
        return True
    except subprocess.CalledProcessError:
        print("Docker is not running without sudo.")
        return False
    except FileNotFoundError:
        print("Docker is not installed.")
        return False

if __name__ == "__main__":
    print("Please run main.py.")