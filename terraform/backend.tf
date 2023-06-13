terraform {
  backend "gcs" {
    bucket = "bkt-b-tfstate-c35d" // this bucket will be created in the seed project
    prefix = "terraform-tfstate"
  }
}