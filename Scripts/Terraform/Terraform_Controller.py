from Scripts.Terraform.Terraform_Run import set_command_dir, terraform_run_gcp

def terraform_run(teamname):
    set_command_dir(teamname)
    terraform_run_gcp()