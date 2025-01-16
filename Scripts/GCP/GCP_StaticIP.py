import subprocess
from Scripts.GCP.GCP_Locate import locate_gcloud

def check_static_ip(region):
    gcloud_path = locate_gcloud()
    result = subprocess.run(
        [gcloud_path, 'compute', 'addresses', 'list', '--regions', region, '--filter', f"name=('ip2-{region}')"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        if f"ip2-{region}" in result.stdout:
            return True
    return False

def check_global_static_ip():
    gcloud_path = locate_gcloud()
    result = subprocess.run(
        [gcloud_path, 'compute', 'addresses', 'list', '--global', '--filter', "name=('ip2-global')"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        if "ip2-global" in result.stdout:
            return True
    return False

def create_static_ip(region):
    gcloud_path = locate_gcloud()
    create_ip = subprocess.run(
        [gcloud_path, 'compute', 'addresses', 'create', f'ip2-{region}',
         f'--region={region}'],
        capture_output=True,
        text=True
    )
    print(create_ip.stdout)
    print(create_ip.stderr)

def create_global_static_ip():
    gcloud_path = locate_gcloud()
    create_ip = subprocess.run(
        [gcloud_path, 'compute', 'addresses', 'create', 'ip2-global',
         '--global'],
        capture_output=True,
        text=True
    )
    print(create_ip.stdout)
    print(create_ip.stderr)

def get_static_ip(region):
    gcloud_path = locate_gcloud()
    gcloud_get_ip = subprocess.run(
        [gcloud_path, 'compute', 'addresses', 'list', '--filter', f'name=ip2-{region}', '--format',
         'value(ADDRESS)'],
        capture_output=True,
        text=True,
    )
    return gcloud_get_ip.stdout.strip()

def get_global_static_ip():
    gcloud_path = locate_gcloud()
    gcloud_get_ip = subprocess.run(
        [gcloud_path, 'compute', 'addresses', 'list', '--global', '--filter', 'name=ip2-global', '--format', 'value(ADDRESS)'],
        capture_output=True,
        text=True,
    )
    return gcloud_get_ip.stdout.strip()


if __name__ == "__main__":
    exist = check_global_static_ip()
    if exist:
        print('exists')
    else:
        print('not exists')