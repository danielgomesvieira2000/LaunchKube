# VPC
resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-vpc"
  auto_create_subnetworks = "false"
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_id}-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.10.0.0/24"
}

resource "google_compute_firewall" "allow_postgresql_from_kubernetes" {
  name         = "allow-postgresql-from-kubernetes"
  network     = google_compute_network.vpc.name
  direction    = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["5432"]
  }
  source_ranges = ["10.0.0.0/24"] 

}

resource "google_compute_firewall" "allow_https" {
  name         = "allow-https"
  network      = google_compute_network.vpc.name
  direction    = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
  source_ranges = ["0.0.0.0/0"]
}

resource "google_compute_firewall" "allow_keycloak" {
  name         = "allow-keycloak"
  network      = google_compute_network.vpc.name
  direction    = "INGRESS"
  allow {
    protocol = "tcp"
    ports    = ["8180"]
  }
  source_ranges = ["0.0.0.0/0"]
}
