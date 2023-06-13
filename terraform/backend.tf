terraform {
  backend "gcs" {
    bucket = "bkt-b-tfstate-66e6" // this bucket will be created in the seed project
    prefix = "golden-image"
  }
}