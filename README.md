![image](./media/launchkube_banner.png)

## Introduction

Welcome to Launchkube, an innovative deployment solution designed to simplify and streamline the process of deploying web applications. Launchkube leverages the power of Terraform and Kubernetes to set up robust infrastructure and deploy applications with minimal effort.

With a user-friendly GUI, Launchkube automates the deployment process while offering full control over configuration and management. It handles the complexities of filling secret variables and setting up credentials, so you can focus on building and improving your applications instead of wrestling with deployment headaches.

Launchkube provides:

* Seamless deployment to Google Cloud Platform using Terraform and Kubernetes.
* Automatic secret variable handling and credential management.
* Local deployment support using Docker Compose.
* A python-based, intuitive dashboard for monitoring and controlling deployments.
* Whether you're deploying your application for the first time or managing ongoing updates, Launchkube empowers you to get your projects online efficiently and with confidence.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Install Gcloud CLI](#install-gcloud-cli)
    - [Debian/Ubuntu](#debianubuntu)
    - [Windows](#windows)
4. [Setup Google Cloud Platform Account](#setup-google-cloud-platform-account)
    - [Create Account](#create-account)
    - [Create Project](#create-project)
    - [Add Billing Account](#add-billing-account)
    - [Enable APIs](#enable-apis)
5. [Install Python](#install-python)
6. [Install kubectl](#install-kubectl)
    - [Windows](#windows-1)
    - [Linux](#linux)
7. [Install Terraform](#install-terraform)
    - [Windows](#windows-2)
    - [Linux](#linux-1)
8. [Run the Program](#run-the-program)
9. [Compile the Program for Windows using PyInstaller](#compile-the-program-for-windows-using-pyinstaller)
10. [Change the Settings](#change-the-settings)
    - [Current Project Google Cloud](#current-project-google-cloud)
11. [Deployment Instructions](#deployment-instructions)
    - [Google Cloud Deployment](#google-cloud-deployment)
        - [Select Your Application](#select-your-application)
        - [Adding Your Credentials](#adding-your-credentials)
        - [Deploying Your Application](#deploying-your-application)
        - [Take Offline](#take-offline)
    - [Local Deployment](#local-deployment)
        - [Add Your Docker-Compose File](#add-your-docker-compose-file)
        - [Run Your Local Deployment](#run-your-local-deployment)
12. [Monitor Your Deployment](#monitor-your-deployment)
13. [Common Errors](#common-errors)
    - [Deploy Errors](#deploy-errors)
    - [Destroy Errors](#destroy-errors)
        - [Terraform Destroy 'xxx is already being used by xxx...'](#terraform-destroy-xxx-is-already-being-used-by-xxx)

---


## Requirements

What programs are required to run this app.
* Python (+ pillow package)
* Docker
* Google Cloud CLI ( + beta components)
* Kubectl
* Terraform

## Install Gcloud CLI
Source: https://cloud.google.com/sdk/docs/install

Introduction to gcloud.
### Debian/Ubuntu
```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates gnupg curl
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
sudo apt-get update && sudo apt-get install google-cloud-cli
gcloud components install beta --quiet
gcloud components install gke-gcloud-auth-plugin
```

### Windows
Download the installer here: https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe

OR

Download using command:
```
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```
When the installer is launched, just follow the prompts on the installer. Make sure gcloud commands are added to your PATH. You can double check this using the command gcloud --version.
If gcloud commands are not properly installed, the dashboard cannot be run.

### Be sure the beta components are installed
Besides installing the basic version of the gcloud commands, we need an extra component. 
This is needed to access billing account of the selected project. 

*Make sure this is installed.*
```
gcloud components install beta --quiet
gcloud components install gke-gcloud-auth-plugin
```

## Setup Google Cloud Platform account

### Create Account
1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. Click on the **Create Account** button.
3. After logging in, you will be redirected to the Google Cloud Console

![Google Cloud Console](./media/screenshots/gcloud-dashboard.png)  
*Google Cloud Console - The home screen where you can create and manage Google Cloud projects.*


### Create Project

On the google cloud dashboard, you can create a new project. At the top left you can see your current project, click on there.
![gcloud create project](./media/screenshots/gcloud_create_project.png)

Here you can create your new project
![gcloud new project](./media/screenshots/gcloud_new_project.png)

### Add billing account

Make sure you have a billing account with Google Cloud credits. You should have gotten 50 bucks of credits from KdG. Add these credits to a billing account, then connect the billing account to a Google Cloud project.

### Enable API's

After creating a new account, make sure to enable the following services:

Set project
```
gcloud config set project [PROJECT_ID]
```
Enable Services
```
gcloud services enable cloudbilling.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable config.googleapis.com
gcloud services enable sqladmin.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable certificatemanager.googleapis.com
```

## Install python

This dashboard is built using python with tkinter.

https://www.python.org/downloads/

You will need an extra library installed called 'pillow'.
```
pip install pillow
pip install cloudflare
pip install customtkinter
```

Or use the requirements.txt to install them.

```
pip install -r requirements.txt
```

## Install kubectl
The deployment will use Kubernetes. Kubectl will make Kubernetes management possible.
### Windows
```
winget install -e --id kubernetes.kubectl
```

### Linux
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl 
/usr/local/bin/kubectl
```

## Install Terraform
Terrafrom is used as an orchestra tool. It will setup the database and Kubernetes.
### Windows
The easiest way is to use choco installer: https://chocolatey.org/
```
choco install terraform
```
### Linux
```
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

wget -O- https://apt.releases.hashicorp.com/gpg | \
gpg --dearmor | \
sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null

gpg --no-default-keyring \
--keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
--fingerprint

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
sudo tee /etc/apt/sources.list.d/hashicorp.list

sudo apt update

sudo apt-get install terraform
```

## Run the program

Run main.py using python3.

```
python3 main.py
```

## Compile the program for Windows using pyinstaller

Run this command:
```
pyinstaller --onefile --windowed --icon=media/icon/launchkube_icon.ico --add-data "media/icon/launchkube_icon.ico;media/icon" main.py
```

If everything is correct, you will see the Launchkube!
![The launchkube home screen](./media/screenshots/dashboard-home.png)

## Change the settings

At the bottom left you will see a 'Settings' button. Here you can set the Google Cloud project you are working on and see if it has a billing account connected to it. At the bottom you will see the account that you are logged in as.

![Launchkube settings](./media/screenshots/billing-account-correct.png)

### Current project Google Cloud

You will see a project dropdown menu, select your project here if it is not selected yet.
Next to the dropdown menu is a '+' button that allows you to add a project to your google cloud account.
At the far left is a text saying if the selected project has a active and working billing account setup.

If that is not the case, it will tell you so. It is important to have a correctly set up billing account, otherwise you won't be able to deploy.

![image](./media/screenshots/billing-account-correct.png)

## Deployment Instructions

If you are ready to deploy your project, proceed to the 'deploy' menu.

![image](./media/screenshots/dashboard-screen-deploy.png)

### Google Cloud Deployment

Proceed to click the 'Deploy Online' to get your application up and running on Google Cloud!

#### Select your application

![image](./media/screenshots/dashboard-deploy-controls.png)

Select your project / team name. If it's the first time deploying, you will 
need to enter your credentials. 

#### Adding your credentials

![image](./media/screenshots/dashboard-setup-credentials.png)

Press ok, and you will find text field to fill in your teams information.

IF THIS DOES NOT SHOW UP AND YOU DID NOT EVER PUT IN YOUR CREDENTAILS, PLEASE DELETE THE variables.tf file in gcp_deployment/{team name}.

![image](./media/screenshots/dashboard-add-credentials.png)

Registry server is where your images are located. This will be either docker or gitlab. For gitlab, enter 'registry.gitlab.com'.

The username and password are your account credentials for where the image is hosted.

In the case of gitlab:
The username is your KdG email.
The password will be a Personal Access Token of your account. That will look like something like this: 'glpat-xxxxxxxxxxxxxxxxxxxx'.

After entering everything, proceed to 'Add variables'.

IN THE CASE OF ENTERING WRONG CREDENTIALS THE DEPLOYMENT WON'T WORK. TO RE-ENTER THESE CREDENTIALS, DELETE THE 'variables.tf' FILE INSIDE OF 'gcp_deployment/{teamname}'.

#### Deploying your application

You will be sent back to the deployment screen. Choose your team and click on 'Deploy selected team'.

![image](./media/screenshots/dashboard-settingup-terraform.png)

First the terraform will setup an infrastructure. This can take anywhere from 15 to 25 minutes.

![image](./media/screenshots/dashboard-settingup-kubernetes.png)

Next the Kubernetes credentials and accounts will be setup on your Google Cloud project.

![image](./media/screenshots/dashboard-deployment-succesful.png)

After that your deployment will be successful!

It may take some minutes until the actual website is up and running.

TEMPORARY

If there is no static ip connected to a domain name, you can get the ip to which it will be deployed using the following command:

![image](./media/screenshots/get-ingress-ip.png)

It can take up to three minutes to get a randomly assigned external ip address.

##### HTTPS Connection

Because a Google Managed Certificate is being used, it may take a while until https is available. Please wait up to 30 minutes for this.

#### Take offline

After deployment, you will want to take down the application. Start doing this by pressing 'Take offline'.

![image](./media/screenshots/dashboard-destroy-kubernetes.png)

First it will start by deleting the Kubernetes deployments, credentials en service accounts.

![image](./media/screenshots/dashboard-destroy-terraform.png)

After that, the terraform infrastructure will be destroyed and taken offline.

### Local Deployment
Local deployment is made possible by using docker compose files.

#### Add your docker-compose file
In order to add docker compose files, you will need to create a new folder in 'local_deployment'. 
Inside that folder, you put in your docker-compose.yml file. The folder name will now be an option in the dropdown menu
on the local deployment screen on the dashboard.

#### Run your local deployment

![image](./media/screenshots/dashboard-local-screen.png)

Just select the project you would like to locally deploy and click on the 'Local run selected team' button.

![image](./media/screenshots/dashboard-local-loading.png)

It will start pulling and running the containers.

![image](./media/screenshots/dashboard-local-done.png)

The project name and it's open ports will now be visible. If you are deploying a website, you can simply surf to localhost:{port}.
If you would like to take the containers down, press the 'Clear all' button.

## Monitor Your Deployment

How to monitor deployment, what can you see.
COMING SOON

## Common Errors
Here you can find error's that I have encountered and not fixed yet in a clean, user-friendly way :)
You can find the dirty, tedious fixes to those problems here.

### Deploy errors

#### Variables that are not correct

In case your variables are not correct because you changed your project or have another person's variables, delete the variables.ft file inside of gcp_deployment/{team name}. 

### Destroy errors

#### Terraform Destroy 'xxx is already being used by xxx...'

The terraform destroy command can sometimes be tedius. After deploying and destroying multiple times, it can create random errors.

![image](./media/screenshots/dashboard-error-destroy-terraform.png)

This error means that there was an issue in the order of which terraform deleted certain components. To fix this, go to: console.cloud.google.com
and check if the following services are deleted:

##### Endpoints

Check for 'Endpoints' and go to 'Network endpoint groups'.

![image](./media/screenshots/dashboard-error-goto-endpoints.png)

Now select the endpoint if there is one, and delete it.
![image](./media/screenshots/dashboard-error-delete-endpoints.png)

##### VPC Network

Check for 'vpc' and go to 'VPC networks'

![image](./media/screenshots/dashboard-error-goto-vpc.png)

If you see an extra vpc besides your 'default' network, it must be deleted. Click on it.

![image](./media/screenshots/dashboard-error-enter-vpc.png)

Once inside, click on the 'DELETE VPC NETWORK' button to delete it.

![image](./media/screenshots/dashboard-error-inside-vpc.png)

Fill in the textfield and proceed to delete the vpc Network.
![image](./media/screenshots/dashboard-error-delete-vpc.png)

If anything goes wrong here, it is always safe to follow these steps.


## Credits
Team 5 3ISB