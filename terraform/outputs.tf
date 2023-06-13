output "bucket_name" {
  description = "Storage bucket name"
  value       = google_storage_bucket.bucket.name
}

output "cloudfunction_name" {
  description = "Cloud Foundation name"
  value       = google_cloudfunctions_function.function.name
}

output "project_id" {
  value = google_project.golden_image.project_id
}
output "custom-role-id" {
  value = google_organization_iam_custom_role.my-custom-role.id
}

output "service-account" {
  value = google_service_account.sa.email
}
