from Scripts.Terraform.Terraform_Run import set_command_dir
import os


def check_realmfile_exists(teamname):
    set_command_dir(teamname)

    if os.path.isfile('realm-export.json'):
        print('realm-export file found.')
        return True
    else:
        print('realm-export file not found.')
        return False

if __name__ == "__main__":
    if check_realmfile_exists('team7'):
        print('yeppe')
    else:
        print('nope')