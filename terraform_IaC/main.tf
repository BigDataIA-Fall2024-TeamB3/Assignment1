provider "google" {
  project = var.project_id
  region  = var.region
}

# Minimal Cloud SQL instance configuration with PostgreSQL
resource "google_sql_database_instance" "postgres_instance" {
  name             = var.instance_name
  database_version = "POSTGRES_16"  # Specify the desired PostgreSQL version
  region           = var.region

  settings {
    tier = "db-f1-micro"  # Smallest instance type for testing

    ip_configuration {
      ipv4_enabled = true  # Enable public IP

      # Authorize all IP addresses to access this instance
      authorized_networks {
        name  = "All IPs"
        value = "0.0.0.0/0"
      }
    }
  }

  deletion_protection = false  # Set to true to prevent accidental deletion
}

# Create the initial database in the instance
resource "google_sql_database" "default" {
  name     = var.database_name
  instance = google_sql_database_instance.postgres_instance.name
}

# Create the database user
resource "google_sql_user" "default" {
  name     = var.db_user
  password = var.db_password
  instance = google_sql_database_instance.postgres_instance.name
}

resource "google_storage_bucket" "gaia_files" {
  name          = var.bucket_name
  location      = var.region
  storage_class = "STANDARD"
  uniform_bucket_level_access = true
}