resource "google_cloudfunctions_function" "function" {
  depends_on = [null_resource.zipping_files]
  name                  = var.name
  description           = var.cf_description
  runtime               = var.runtime
  region                = var.region
  project               = google_project.golden_image.project_id
  available_memory_mb   = var.available_memory_mb
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  trigger_http          = var.trigger_http
  entry_point           = var.entry_point
  timeout               = var.timeout
  environment_variables = {
    IMAGE_PROJECT_ID = var.image_project_id
    FUNCTION_REGION  = var.region
    FUNCTION_PROJECT = google_project.golden_image.project_id
    FUNCTION_NAME    = var.name
    WEBHOOK_URL      = var.webhook_name
  }
}