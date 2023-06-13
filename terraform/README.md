# Terraform Folder Structure for image monitoring solution
```
.── terraform
    ├── README.md
    ├── backend.tf
    ├── cloudfunction.tf
    ├── custom_role.tf
    ├── outputs.tf
    ├── project.tf
    ├── providers.tf
    ├── python.zip
    ├── storage.tf
    ├── terraform.tfvars
    └── variables.tf
```

## Event Function

This terraform code create and configures the project with Cloud Functions function.

The `project.tf` creates the project and enables the `cloudfunctions.googleapis.com` and `cloudfunctions.googleapis.com` apis 

The `storage.tf` creates the storage bucket on GCP to store the compressed code.

The `cloudfunctions.tf` configures a function sourced from a directory on
localhost to respond to a given event trigger. The source directory is
compressed and uploaded as a Cloud Storage bucket object which will be
leveraged by the function.

The `custome_role.tf` will create the custom role on ORG level then create 
the SA in project created earlier and add thea SA as principal to the organisation 
with `"roles/cloudasset.viewer","roles/compute.viewer","roles/resourcemanager.organizationViewer","custome_role created earlier"`


## Compatibility
This terraform code is compatible with Terraform `>= 1.0.9` and Google `>= 3.89.0`

## Usage

This terraform code creates a project and under that project it will create the
storage bucket and under that bucket the compressed code will be pushed then 
Cloud Function will be deployed with that code.
It will create the Custom Role on ORG level and create SA in project which will 
inherit the permission from ORG .

## IAM Permisssions

```
"compute.addresses.setLabels"
"compute.disks.setLabels"
"compute.externalVpnGateways.setLabels"
"compute.forwardingRules.pscSetLabels"
"compute.forwardingRules.setLabels"
"compute.globalAddresses.setLabels"
"compute.globalForwardingRules.pscSetLabels"
"compute.globalForwardingRules.setLabels"
"compute.images.deprecate"
"compute.images.setLabels"
"compute.instances.setLabels"
"compute.interconnectAttachments.setLabels"
"compute.interconnects.setLabels"
"compute.snapshots.setLabels"
"compute.targetVpnGateways.setLabels"
"compute.vpnGateways.setLabels"
"compute.vpnTunnels.setLabels"
"notebooks.instances.setLabels"
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| org\_id | GCP Organization ID. | `string` | `n/a` | `yes` |
| billing\_account | The ID of the billing account to associate projects with. | `string` | `n/a` | `yes` |
| name | Name provided to create project and bucket. | `string` | `n/a` | `yes` |
| runtime | It specifies the platform with version on which the code runs. | `string` | `python38` | `yes` |
| region | It specifies the region in which the cloud function needs to deploy and run. | `string` | `n/a` | `yes` |
| available\_memory\_mb | The amount of memory in megabytes allotted for the function to use. | `number` | `256` | `yes` |
| entry\_point | The name of a method in the function source which will be invoked when the function is executed. | `string` | n/a | `yes` |
| cr\_description | It contains the description of Custom Role. | `string` | `n/a` | `yes` |
| cf\_description | It contains the description of Cloud Functions. | `string` | `n/a` | yes |

