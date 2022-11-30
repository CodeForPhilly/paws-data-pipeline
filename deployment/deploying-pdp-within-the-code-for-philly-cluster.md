# Deploying PDP within the Code for Philly cluster

## PDP hosting

The PAWS Data Pipeline runs on a Kubernetes cluster donated by [Linode](https://github.com/CodeForPhilly/paws-data-pipeline/wiki/www.linode.com) to the Code for Philly (CfP) project and is managed by the CfP [civic-cloud](https://forum.codeforphilly.org/c/public-development/civic-cloud/17) team.

The code and configurations for the various projects running on the cluster are managed using [hologit](https://github.com/JarvusInnovations/hologit) which

> _lets you declaratively define virtual sub-branches (called holobranches) within any Git branch that mix together content from their host branch, content from other repositories/branches, and executable-driven transformations._\[1]

The pieces for the sandbox clusters can be found in the `.holo` directory in the PDP repository and the [sandbox](https://github.com/CodeForPhilly/cfp-sandbox-cluster) or [live](https://github.com/CodeForPhilly/cfp-live-cluster) cluster repos as appropriate.

The branch (within the PDP repo) that holds the `.holo` directory is specified at [paws-data-pipeline.toml](https://github.com/CodeForPhilly/cfp-sandbox-cluster/blob/main/.holo/sources/paws-data-pipeline.toml).

RBAC roles and rights are defined at [admins](https://github.com/CodeForPhilly/cfp-sandbox-cluster/blob/main/admins/paws-data-pipeline.yaml).

### Updating deployed code

To deploy new code,

* Bump the image tag versions in **paws-data-pipeline/src/helm-chart/values.yaml** to the value you'll use for this deployment (e.g. v.2.3.4)
* Commit to master, tag with the above value, push to GitHub with --follow-tags
* Open a PR against [cfp-sandbox-cluster/.holo/sources/paws-data-pipeline.toml](https://github.com/CodeForPhilly/cfp-sandbox-cluster/blob/main/.holo/sources/paws-data-pipeline.toml) setting ref = "refs/tags/v2.3.4"
* The sysadmin folks hang out at [https://forum.codeforphilly.org/c/project-support-center/sysadmin/20](https://forum.codeforphilly.org/c/project-support-center/sysadmin/20) and you can ask for help there

### Ingress controller

CfP uses the [ingress-nginx](https://kubernetes.github.io/ingress-nginx) ingress controller (_not to be confused with an entirely different project called **nginx-ingress**_)

The list of settings can be found here: [Settings](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/)\
To update settings, edit [release-values.yaml](https://github.com/CodeForPhilly/cfp-sandbox-cluster/blob/main/paws-data-pipeline/release-values.yaml) and create a pull request.

SSL cert configuration can also be found in [release-values.yaml](https://github.com/CodeForPhilly/cfp-sandbox-cluster/blob/main/paws-data-pipeline/release-values.yaml)



1. _“Any sufficiently advanced technology is indistinguishable from magic.”_ Arthur C. Clarke
