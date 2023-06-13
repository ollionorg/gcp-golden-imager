variable "org_id" {
  description = "GCP Organization ID"
}

variable "billing_account" {
  description = "The ID of the billing account to associate projects with."
}

variable "name" {
  description = "Name of the project, bucket and cloud function"
}

variable "runtime" {
  description = "Specifies the version of framwork which cloud function is going to use"
}

variable "region" {
  description = "accepts the region"
}

variable "available_memory_mb" {
  description = "It acceptst the memory use to run the Cloud function"
}

variable "trigger_http" {
  description = "It accepts the value in boolean format"
}

variable "entry_point" {
  description = "It accepcts the entrypoint from which the needs to be run"
}

variable "cr_description" {
  description = "It contains the description for Custom Role"
}

variable "cf_description" {
  description = "It contains the description for CloudFunction"
}

variable "timeout" {
  description = "A specified period of time till the CloudFunction runs"
}

variable "image_project_id" {
  description = "It contains the project id where all the custom images created and stored"
}

variable "webhook_name" {
  description = "Webhook Url for notification"
  default = ""
}