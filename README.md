# GitLab-CI SafeSCARF

This repository provides an example implementation of [SafeSCARF](https://documentation.portal.pan-net.cloud/safescarf-product/) (based on [DefectDojo](https://www.defectdojo.org)) with [GitLab-CI](https://docs.gitlab.com/ee/ci/).

It supports the following test engines:

* [DevSecOps Container Scanner By DTIT](https://gitlab.devops.telekom.de/devsecops-tools/container-scanner)
* [GitLab Dependency Scanner](https://docs.gitlab.com/ee/user/application_security/dependency_scanning/)
* [GitLab Container Scanner](https://docs.gitlab.com/ee/user/application_security/container_scanning/)
* [GitLab SAST](https://docs.gitlab.com/ee/user/application_security/sast/)
* [GitLab Secret Scanner](https://docs.gitlab.com/ee/user/application_security/secret_detection/)

Please see [Scan Engines](#scan-engines) to understand how to enable them and which are enabled by default.

> Some engines, like the gitlab-container engine are not directly plug and play and need some minor configurations.

For having Anchore Engine working the path of the image is expected in the Variable "IMAGE_NAME".

## Usage

For using this example simple include the main file "gitlab-sast.yml" as a remote and configure at least the mandatory variables in your CI/CD pipeline.

```yaml
include:
  - remote: "https://secureops.pages.devops.telekom.de/safescarf/safescarf-integration/gitlab-safescarf.yml"
```

After, you can enable and configure the desired engines (see [Scan Engines](#scan-engines)).

## Variables

The variables have to be set in your gitlab-ci.yml file or in the GitLab UI.

### General

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| SAFESCARF_URL | Yes | 'https://dt-sec.safescarf.pan-net.cloud/api/v2' | URL your your DefectDojo (SafeSCARF) API-V2 Endpoint |
| SAFESCARF_TOKEN | Yes | null | API token for API-V2 Endpoint (machine or user token)|
| SAFESCARF_PRODUCTID | Yes | null | ID of your Product in SafeSCARF (will be displayed in the url bar of the browser after accessing the product) |
| SAFESCARF_NOT_ON_MASTER | No | false | Disable SafeSCARF implementation when executed on Master branch |

### Engagement

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| SAFESCARF_ENGAGEMENT_PERIOD | No | 7 | Duration in days of the created Engagement |
| SAFESCARF_ENGAGEMENT_STATUS | No | In  Progress | Initial Status of the Engagement when created. Possible Values: Not Started, Blocked, Cancelled, Completed, In Progress, On Hold, Waiting for Resource |
| SAFESCARF_ENGAGEMENT_DEDUPLICATION_ON_ENGAGEMENT | No | false | If enabled deduplication will only mark a finding in this engagement as duplicate of another finding if both findings are in this engagement. If disabled, deduplication is on the product level. |
| SAFESCARF_ENGAGEMENT_BUILD_SERVER | No | null | ID of the Build Server if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_SOURCE_CODE_MANAGEMENT_SERVER | No | null | ID of the SCM Server if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_ORCHESTRATION_ENGINE | No | null | ID of the Orchestration Engine if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_THREAT_MODEL | No | true | |
| SAFESCARF_ENGAGEMENT_API_TEST | No | true | |
| SAFESCARF_ENGAGEMENT_PEN_TEST | No | true | |
| SAFESCARF_ENGAGEMENT_CHECK_LIST | No | true | |

### Scan Engines

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| DSO_CONTAINER_SCANNING | No | false | enables the [DevSecOps Scanner By DTIT](https://gitlab.devops.telekom.de/devsecops-tools/container-scanner) |
| GITLAB_CONTAINER_SCANNING | No | false | enables gitlabs built in [container scanner](https://docs.gitlab.com/ee/user/application_security/container_scanning/) |
| GITLAB_DEPENDENCY_SCANNING | No | false | enables gitlabs built in [dependency scanner](https://docs.gitlab.com/ee/user/application_security/dependency_scanning/) |
| GITLAB_SAST_SCANNING | No | true | enables gitlabs built in [sast scanner](https://docs.gitlab.com/ee/user/application_security/sast/) |
| GITLAB_SECRET_SCANNING | No | true | enables gitlabs built in [secret detection](https://docs.gitlab.com/ee/user/application_security/secret_detection/) |

### Scan

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| SAFESCARF_SCAN_MINIMUM_SEVERITY | No | Info | Available values : Info, Low, Medium, High, Critical | 
| SAFESCARF_SCAN_ACTIVE | No | true | |
| SAFESCARF_SCAN_VERIFIED | No | true | |
| SAFESCARF_SCAN_CLOSE_OLD_FINDINGS | No | true | |
| SAFESCARF_SCAN_PUSH_TO_JIRA | No | false | |
| SAFESCARF_SCAN_ENVIRONMENT | No | Default | |

### Anchore Engine

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| DISABLE_ANCHORE | No | true | Disable Anchore Engine if not required | 
| ANCHORE_FAIL_ON_POLICY | No | false | Let Job Anchore-Engine fail if vulnerability is found |

## Forking

Feel free to fork this repository and include into your own GitLab Instance.
The only thing you have to take care of is to update the includes in "gitlab-safescarf.yml" in the repositories root directory.

## Contributing

Feel free to add another scanner or to improve current implementations.

For new implementations, please follow the naming conventions: `<product>-<scanner-type>.yml`.
