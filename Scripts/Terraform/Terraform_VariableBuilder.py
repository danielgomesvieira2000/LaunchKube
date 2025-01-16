import re
import os

def get_variable_location(teamname, filename="variables.tf"):
    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    terra_file_path = f"gcp_deployment\\{teamname}\\{filename}" if os.name == 'nt' else f"gcp_deployment/{teamname}/{filename}"
    return os.path.join(project_root, terra_file_path)

def get_secret_variables(teamname):
    file_path = get_variable_location(teamname, "TEMPLATE_variables.wtf")
    secret_variables = []
    variable_name = None
    is_sensitive = False

    with open(file_path, "r") as file:
        for line in file:
            stripped_line = line.strip()

            if stripped_line.startswith("variable"):
                match = re.match(r'variable\s+"([^"]+)"', stripped_line)
                if match:
                    variable_name = match.group(1)
                    is_sensitive = False

            if stripped_line.startswith("sensitive") and "true" in stripped_line:
                is_sensitive = True

            if variable_name and is_sensitive and stripped_line == "}":
                secret_variables.append(variable_name)
                variable_name = None

    return secret_variables

def set_secret_variables(teamname, secrets, secret_values, project_id):
    template_file_path = get_variable_location(teamname, "TEMPLATE_variables.wtf")
    output_file_path = get_variable_location(teamname, "variables.tf")

    with open(template_file_path, "r") as file:
        lines = file.readlines()

    updated_lines = []
    secret_index = 0
    inside_variable_block = False
    variable_name = None

    for line in lines:
        stripped_line = line.strip()

        if "{PROJECT_ID}" in line:
            line = line.replace("{PROJECT_ID}", project_id)

        if stripped_line.startswith("variable"):
            match = re.match(r'variable\s+"([^"]+)"', stripped_line)
            if match:
                variable_name = match.group(1)
                inside_variable_block = True

        if inside_variable_block and "sensitive" in stripped_line and variable_name in secrets:
            default_value = secret_values[secret_index]
            updated_lines.append(f'  default = "{default_value}"\n')
            secret_index += 1
            continue

        if inside_variable_block and stripped_line == "}":
            inside_variable_block = False
            variable_name = None

        updated_lines.append(line)

    with open(output_file_path, "w") as output_file:
        output_file.writelines(updated_lines)

    print(f"Updated variables saved to {output_file_path}")

def check_if_variables_exist(teamname):
    file_path = get_variable_location(teamname, "variables.tf")
    return os.path.exists(file_path)

if __name__ == "__main__":
    print('Please run main.py.')
