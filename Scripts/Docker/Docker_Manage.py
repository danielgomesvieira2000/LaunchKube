import subprocess

def docker_get_list():
    run_result = subprocess.run(
        ['docker', 'compose', 'ls'],
        capture_output=True,
        text=True,
        check=True
    )
    lines = run_result.stdout.strip().split('\n')
    stack_names = [line.split()[0] for line in lines[1:] if line.strip()]
    return stack_names

def docker_delete_all():
    run_result = subprocess.run(
        ['docker', 'ps', '-aq'],
        capture_output=True,
        text=True,
        check=True
    )

    container_ids = run_result.stdout.strip().splitlines()

    if container_ids:
        subprocess.run(
            ['docker', 'rm', '-f'] + container_ids,
            check=True
        )
        print("All containers have been deleted.")
    else:
        print("No containers to delete.")

if __name__ == "__main__":
    print("Please run main.py.")
