terraform {
  backend "gcs" {
    bucket = "UPDATE_BUCKET_NAME" // this bucket will be created in the seed project
    prefix = "golden-image"
  }
}