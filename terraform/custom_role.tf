locals {
  sa_org_iam_roles = [
    "roles/cloudasset.viewer",
    "roles/compute.viewer",
    "roles/resourcemanager.organizationViewer",
  ]
}


resource "google_organization_iam_custom_role" "my-custom-role" {
  role_id     = "goldenimagemonitoringcustomrole${random_string.suffix.result}"
  org_id      = var.org_id
  title       = "${var.name}-custom-role-${random_string.suffix.result}"
  description = var.cr_description
  permissions = [
    "compute.addresses.setLabels",
    "compute.disks.setLabels",
    "compute.externalVpnGateways.setLabels",
    "compute.forwardingRules.pscSetLabels",
    "compute.forwardingRules.setLabels",
    "compute.globalAddresses.setLabels",
    "compute.globalForwardingRules.pscSetLabels",
    "compute.globalForwardingRules.setLabels",
    "compute.images.deprecate",
    "compute.images.setLabels",
    "compute.instances.setLabels",
    "compute.interconnectAttachments.setLabels",
    "compute.interconnects.setLabels",
    "compute.snapshots.setLabels",
    "compute.targetVpnGateways.setLabels",
    "compute.vpnGateways.setLabels",
    "compute.vpnTunnels.setLabels",
    "notebooks.instances.setLabels",
    "cloudfunctions.functions.invoke",
    "cloudfunctions.functions.update"
  ]
}

resource "google_service_account" "sa" {
  account_id   = "${var.name}-sa"
  display_name = "${var.name}-service-account for accessing the cloud function"
  project      = google_project.golden_image.project_id
}

resource "google_organization_iam_member" "organization" {
  depends_on = [google_organization_iam_custom_role.my-custom-role]
  for_each   = toset(local.sa_org_iam_roles)
  org_id     = var.org_id
  role       = each.value
  member     = "serviceAccount:${google_service_account.sa.email}"
}

resource "google_organization_iam_member" "cr-organisation" {
  org_id = var.org_id
  role   = google_organization_iam_custom_role.my-custom-role.id
  member = "serviceAccount:${google_service_account.sa.email}"
}