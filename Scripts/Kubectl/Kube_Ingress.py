import subprocess

def get_ingress_hosts():
    try:
        result = subprocess.run(
            ['kubectl', 'get', 'ingress', '-o', 'jsonpath={.items[*].spec.rules[*].host}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )

        if result.stderr:
            print(f"Error: {result.stderr}")
            return None

        hosts = result.stdout.split()

        if not hosts:
            return None

        return hosts

    except subprocess.TimeoutExpired:
        print("Error: Command timed out after 10 seconds")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None



if __name__ == "__main__":
    hosts = get_ingress_hosts()
    if hosts:
        print("Ingress hosts:", hosts)
    else:
        print("No hosts found.")
