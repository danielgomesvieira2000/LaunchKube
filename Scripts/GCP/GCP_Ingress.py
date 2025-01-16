import subprocess


def get_ingress_ip():
    try:
        command = [
            "kubectl",
            "get",
            "ingress",
            "-o",
            'jsonpath="{.items[0].status.loadBalancer.ingress[0].ip}"'
        ]

        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        # Check for errors
        if result.returncode != 0:
            print("Error executing command:", result.stderr)
            return None

        ip_address = result.stdout.strip().replace('"', '')
        return ip_address

    except Exception as e:
        print("An error occurred:", e)
        return None
