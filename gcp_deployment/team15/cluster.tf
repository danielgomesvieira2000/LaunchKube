resource "google_container_cluster" "primary" {
  project = var.project_id
  name    = "${var.project_id}-gke"
  
  location = var.zone
  deletion_protection = false

  network    = google_compute_network.vpc.name
  subnetwork = google_compute_subnetwork.subnet.name

  logging_service    = "logging.googleapis.com/kubernetes"
  monitoring_service = "monitoring.googleapis.com/kubernetes"

  remove_default_node_pool = true
  initial_node_count       = var.gke_num_nodes
  
  # Enable Shielded Nodes features on all nodes in this cluster. Defaults to false
  enable_shielded_nodes = true

  # Enable workload identity for Cloud SQL authentication.
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
  
  # Allow time for each operation to finish.
  timeouts {
    create = "40m" # Default is 40 minutes.
    read   = "40m" # Default is 40 minutes.
    update = "60m" # Default is 60 minutes.
    delete = "40m" # Default is 40 minutes.
  }

  depends_on = [
    google_project_service.service,
    google_project_iam_member.service-account,
    google_compute_subnetwork.subnet,
  ]
}

resource "google_container_node_pool" "primary_nodes" {
  project = var.project_id
  name       = "${google_container_cluster.primary.name}-node-pool"
  # Creating a zonal node pool since this is only an example and for a quick provisioning
  location   = var.zone
  cluster    = google_container_cluster.primary.name
  node_count = var.gke_num_nodes

  # Configuration required by cluster autoscaler to adjust the size of the node pool to the current cluster usage.
  autoscaling {
      min_node_count = 1
      max_node_count = 3
  }
  
  # Auto repair any issues.
  management {
    auto_repair  = true
    auto_upgrade = true
  }
  
  # Parameters used in creating the cluster's nodes.
  node_config {
    machine_type = var.machine_type
    disk_type    = "pd-standard"

    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    service_account = google_service_account.gke-sa.email
    oauth_scopes    = [
      "https://www.googleapis.com/auth/cloud-platform",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/trace.append",
      "https://www.googleapis.com/auth/sqlservice.admin",
    ]

    labels = {
      env     = var.project_id
      cluster = "${var.project_id}-gke"
    }

    workload_metadata_config {
      mode = "GCE_METADATA"
    }

    # preemptible  = true

    tags         = ["gke-node", "${var.project_id}-gke"]

    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
  
  # Allow time for each operation to finish.
  timeouts {
    create = "30m" # Default is 30 minutes.
    update = "30m" # Default is 30 minutes.
    delete = "30m" # Default is 30 minutes.
  }

  depends_on = [google_container_cluster.primary]
}