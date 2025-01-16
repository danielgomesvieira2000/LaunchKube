provider "google" {
   project = "${var.project_id}"
   credentials = "${file("credentials.json")}"
   region = "europe-central2" 
   zone = "europe-central2-b"
}

provider "kubernetes" {
  config_path = "~/.kube/config"
}
