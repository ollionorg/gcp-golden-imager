# Packer Image build pipeline

This document details how we are going to set up a build pipeline using GitHub actions , Cloud build and Packer to create a secure Ubuntu 20.04 image which will meet the compliance requirements. This image will be used as a base image for applications. We can assign access and sharing on that image . plus we can put organization wide constraints on trusted images as well.


## Process walk-through

1. We should have packer.json , and ansible playbooks ready
2. GitHub workflow file.
3. Copy this repository in your local and  update the variables in project-factory/packer directory and ansible playbook accordingly and push the code.
4. Create Git secret.
5. Service account and service key handy with below permissions at least.
	-  Cloud Build Service Account (allow for execution of build on your behalf)
	-  Viewer (cloud build log)
 	-  Compute Instance Admin v1
	-  Service account user
	-  Project Browser
6. Provide Service account mail in GitHub Secrets.
7. Provide service account key content in GitHub Secrets.
8. Provide Project Id in GitHub Secrets.
9. Trigger the github action by merging the code in the main branch.
10. Workflow will be triggered and Final image will be built and pushed to GCE.
 
##
