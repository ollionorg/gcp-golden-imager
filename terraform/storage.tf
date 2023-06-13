resource "null_resource" "zipping_files" {
  triggers = {
    build_number = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = <<EOT
     apk update
     apk add zip
     rm -f python.zip
     cp -r ../files/* .
     zip python.zip main.py requirements.txt payload.json
     rm -rf main.py requirements.txt payload.json
    EOT
  }
}

resource "google_storage_bucket" "bucket" {
  name                        = "${var.name}-${random_string.suffix.result}"
  location                    = var.region
  project                     = google_project.golden_image.project_id
  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "archive" {
  depends_on = [null_resource.zipping_files]
  name       = "index-${timestamp()}.zip"
  bucket     = google_storage_bucket.bucket.name
  source     = "./python.zip"
}
