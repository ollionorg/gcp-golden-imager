# gcp-golden-imager

Packer Pipeline and Golden Image Monitoring Solution  to build regulatory compliant base images for GCE vms and to monitor if VMs are using hardened image or not.

## Directory Structure for repo
```
├── CODEOWNERS
├── LICENSE
├── README.md
├── packer
│   ├── Dockerfile
│   ├── ansible
│   │   ├── files
│   ├── cloudbuild.yaml
│   ├── packer.BKP
│   ├── packer.json
│   └── variables.json
└── terraform
    ├── Files
```

## Prerequisites
1. We have to enable the below APIs in each of the active projects:
   1. Compute API
   2. Cloud Asset API
   3. Cloud Resource Manager API
2. Create a `Custom role` at the organization level with the below permissions
    ```
    compute.addresses.setLabels
    compute.disks.setLabels
    compute.externalVpnGateways.setLabels
    compute.forwardingRules.pscSetLabels
    compute.forwardingRules.setLabels
    compute.globalAddresses.setLabels
    compute.globalForwardingRules.pscSetLabels
    compute.globalForwardingRules.setLabels
    compute.images.deprecate
    compute.images.setLabels
    compute.instances.setLabels
    compute.interconnectAttachments.setLabels
    compute.interconnects.setLabels
    compute.snapshots.setLabels
    compute.targetVpnGateways.setLabels
    compute.vpnGateways.setLabels
    compute.vpnTunnels.setLabels
    notebooks.instances.setLabels
   ```
3. Create a service account in the GCP project where cloud function is deployed.
4. Add a principal at the organisation level with the same name as that of the service account defined above and attach the below roles to the principal
   1. Cloud Asset Viewer
   2. Compute Viewer
   3. Organisation Viewer
   4. `Custom role` (created in step 2)
5. Attach the service account to cloud function at the time of deployment of cloud function.
6. Deploy a scheduler in the same project as that of cloud function, which will trigger the cloud function periodically.
7. Please also make changes in github action workflow cloudbuild-packer.yml , variables.json in packer directory  , ansible variables according to your requirements
8. add github secretes for Service accounts emails, service account keys and project IDs.

## To trigger the Packer pipeline

make changes in `packer` directory variables and raise the PR and merge it to main. this will trigger a worflow which in result will trigger packer cloudbuild pipeline.

## To trigger the deployment of golden image monitoring solution

make changes in `Terraform` directory or `files` directory and raise a PR.
once the PR is raise terraform plan workflow will get trigger.
once the PR is approved and all the checks has been passed, code will be merged into main branch which will trigger terraform apply.
