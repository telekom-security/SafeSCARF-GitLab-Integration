# GitLab-CI DefectDojo

This repository provides an example implementation of [DefectDojo](https://www.defectdojo.org) with [GitLab-CI](https://docs.gitlab.com/ee/ci/).

It supports all [GitLab SAST](https://docs.gitlab.com/ee/user/application_security/sast/) tests and [Anchore Engine](https://anchore.com/opensource/).

As soon as you include this implementation the GitLab SAST test will be activated as well as the Anchore Engine based test for container images.

For having Anchore Engine working the path of the image is expected in the Variable "IMAGE_NAME".

## Usage
For using this example simple include the main file "gitlab-sast.yml" as a remote and configure at least the mandatory variables in your CI/CD pipeline.

```
include:
  - remote: "https://safescarf-integration.caas-p03.telekom.de/gitlab-safescarf.yml"
````

## Variables

The variables have to be set in your gitlab-ci.yml file or in the GitLab UI.

### General

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| DEFECTDOJO_URL | Yes | null | URL your your DefektDojo API-V2 Endpoint (https://defectdojo.example.com/api/v2) |
| DEFECTDOJO_TOKEN | Yes | null | API token for API-V2 Endpoint| 
| DEFECTDOJO_PRODUCTID | Yes | null | ID of your Product in DefectDojo |
| DEFECTDOJO_NOT_ON_MASTER | No | false | Disable DefectDojo implementation when executed on Master branch |

### Engagement
| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| DEFECTDOJO_ENGAGEMENT_PERIOD | No | 7 | Duration in days of the created Engagement |
| DEFECTDOJO_ENGAGEMENT_STATUS | No | Not Started | Initial Status of the Engagement when created. Possible Values: Not Started, Blocked, Cancelled, Completed, In Progress, On Hold, Waiting for Resource |
| DEFECTDOJO_ENGAGEMENT_DEDUPLICATION_ON_ENGAGEMENT | No | false | If enabled deduplication will only mark a finding in this engagement as duplicate of another finding if both findings are in this engagement. If disabled, deduplication is on the product level. | 
| DEFECTDOJO_ENGAGEMENT_BUILD_SERVER | No | null | ID of the Build Server if configured in DefecDojo | 
| DEFECTDOJO_ENGAGEMENT_SOURCE_CODE_MANAGEMENT_SERVER | No | null | ID of the SCM Server if configured in DefecDojo |
| DEFECTDOJO_ENGAGEMENT_ORCHESTRATION_ENGINE | No | null | ID of the Orchestration Engine if configured in DefecDojo | 
| DEFECTDOJO_ENGAGEMENT_THREAT_MODEL | No | true | |
| DEFECTDOJO_ENGAGEMENT_API_TEST | No | true | |
| DEFECTDOJO_ENGAGEMENT_PEN_TEST | No | true | |
| DEFECTDOJO_ENGAGEMENT_CHECK_LIST | No | true | |

### Scan
| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| DEFECTDOJO_SCAN_MINIMUM_SEVERITY | No | Info | Available values : Info, Low, Medium, High, Critical | 
| DEFECTDOJO_SCAN_ACTIVE | No | true | |
| DEFECTDOJO_SCAN_VERIFIED | No | true | |
| DEFECTDOJO_SCAN_CLOSE_OLD_FINDINGS | No | true | |
| DEFECTDOJO_SCAN_PUSH_TO_JIRA | No | false | |
| DEFECTDOJO_SCAN_ENVIRONMENT | No | Default | |

### Anchore Engine
| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| DEFECTDOJO_ANCHORE_DISABLE | No | false | Disable Anchore Engine if not required | 
| ANCHORE_FAIL_ON_POLICY | No | false | Let Job Anchore-Engine fail if vulnerability is found |

## Forking

Feel free to fork this repository and include into your own GitLab Instance.
The only thing you have to take care of is to update the includes in "gitlab-defectdojo.yml" in the repositories root directory.
