#  cloud-sql.tf
#  Provisions Cloud SQL resources for this project.

resource "google_sql_database" "database" {
  project = var.project_id
  name     = var.db_name
  instance = google_sql_database_instance.postgres.name
  depends_on = [google_sql_database_instance.postgres]
}

resource "google_sql_database" "database-keycloak" {
  project = var.project_id
  name     = "keycloak"
  instance = google_sql_database_instance.postgres.name
  depends_on = [google_sql_database_instance.postgres, google_sql_user.postgres-user, google_sql_user.postgres-user-keycloak]
}

resource "google_sql_database_instance" "postgres" {
  project          = var.project_id
  name             = "${var.project_id}-pg-instance"
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    database_flags {
      name  = "max_connections"
      value = "50" # Set your desired max_connections value
    }

    disk_autoresize = true
    disk_type = "PD_SSD"

    availability_type = "ZONAL"
    location_preference {
        zone = var.zone
    }

    ip_configuration {
        ipv4_enabled = true
    }

    backup_configuration {
      enabled = true
      start_time = "04:30"
    }
    
  }
  deletion_protection = false
}

resource "google_sql_user" "postgres-user" {
  project = var.project_id
  name    = var.db_user
  
  password = var.db_password

  instance = google_sql_database_instance.postgres.name

  depends_on = [google_sql_database_instance.postgres]
}

resource "google_sql_user" "postgres-user-keycloak" {
  project = var.project_id
  name    = var.db_user_2
  
  password = var.db_password_2

  instance = google_sql_database_instance.postgres.name

  depends_on = [google_sql_database_instance.postgres]
}
