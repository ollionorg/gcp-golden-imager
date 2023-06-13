resource "random_string" "suffix" {
  length  = 4
  upper   = false
  special = false
}
resource "google_project" "golden_image" {
  name            = var.name
  project_id      = "${var.name}-${random_string.suffix.result}"
  org_id          = var.org_id
  billing_account = var.billing_account
}

resource "google_project_service" "cloudfunctions" {
  project            = google_project.golden_image.project_id
  service            = "cloudfunctions.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  project            = google_project.golden_image.project_id
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}