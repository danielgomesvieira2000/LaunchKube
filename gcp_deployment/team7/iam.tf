resource "google_project_service" "service" {
  count   = length(var.project_services)
  project = var.project_id
  service = element(var.project_services, count.index)

  disable_on_destroy = false
}

resource "google_service_account" "gke-sa" {
  project      = var.project_id
  account_id   = "gke-cluster-minimal-sa"
  display_name = "Minimal service account for GKE cluster"
}

resource "google_project_iam_member" "service-account" {
  count   = length(var.service_account_iam_roles)
  project = var.project_id
  role    = element(var.service_account_iam_roles, count.index)
  member  = "serviceAccount:${google_service_account.gke-sa.email}"
}