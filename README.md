# GitLab-CI SafeSCARF 2.0

This repository provides a template for gitlab pipelines to integrate with
[SafeSCARF](https://documentation.portal.pan-net.cloud/safescarf-product/)
(based on [DefectDojo](https://www.defectdojo.org)).

- [GitLab-CI SafeSCARF 2.0](#gitlab-ci-safescarf-20)
    - [Structure](#structure)
        - [gitlab-safescarf.yml](#gitlab-safescarfyml)
        - [plugins](#plugins)
    - [Usage](#usage)
        - [Scan Engines](#scan-engines)
            - [DevSecOps Container Scanner By DTIT](#devsecops-container-scanner-by-dtit)
            - [GitLab Container Scanner](#gitlab-container-scanner)
            - [GitLab Dependency Scanner](#gitlab-dependency-scanner)
            - [GitLab SAST Scanner](#gitlab-sast-scanner)
            - [GitLab Secret Scanner](#gitlab-secret-scanner)
            - [Helm Scanning](#helm-scanning)
    - [Variables](#variables)
        - [General](#general)
        - [Engagement](#engagement)
        - [Scan](#scan)
    - [Forking](#forking)
    - [Contributing](#contributing)

Please see [Scan Engines](#scan-engines) to understand how to enable them and
which are enabled by default.

> Some templates, like the gitlab-container scanner are not directly plug and
> play and need some minor configurations.
>
> **You can still use the original variables to configure your jobs!**

## Structure

### gitlab-safescarf.yml

The `gitlab-safescarf.yml` template provides the neccessary default variables
and bundles the
[Safescarf-Connector](https://github.com/telekom-security/SafeSCARF-Connector)
to interact with the SafeSCARF api.

It also verifies that the mandatory variables have been set to prevent long
pipeline debugging.

### plugins

The scan jobs itself can be thought of a plugin. On the one hand they take care
to actually scan the content and keep the result file and on the other hand,
they extend the main template to interact with SafeSCARF and upload the result
file with the correct metadata.

The plugins are located in
[Implementations](https://github.com/telekom-security/SafeSCARF-GitLab-Integration/tree/master/implementations)

## Usage

To use this integration, simply include the mandatory base template
`gitlab-safescarf.yml` as a remote and include the desired plugins after:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/gitlab-safescarf.yml
```

> Make sure to use the github reference. We are publishing those templates on
> GitHub to allow you to pull those templates without any authentication from
> any cicd system.

### Scan Engines

#### DevSecOps Container Scanner By DTIT

To enable this scanner, add the following template to your `include``:

```yaml
include:
  - project: 'secureops/safescarf/safescarf-integration'
    ref: "master"
    file: 'implementations/devsecops-container.yml'
```

For further usage on how to use the scanner please check the scanner
[docs](https://gitlab.devops.telekom.de/devsecops-tools/container-scanner).

> In case of the DSO Container Scanner you need to include it from gitlab via
> the project include syntax (see above) since it is not publicly available.

#### GitLab Container Scanner

To enable this scanner, add the following template to your `include``:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/gitlab-container.yml
```

For further usage on how to use the scanner please check the scanner
[docs](https://docs.gitlab.com/ee/user/application_security/container_scanning/).

#### GitLab Dependency Scanner

To enable this scanner, add the following template to your `include``:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/gitlab-dependency.yml
```

For further usage on how to use the scanner please check the scanner
[docs](https://docs.gitlab.com/ee/user/application_security/dependency_scanning/).

#### GitLab SAST Scanner

To enable this scanner, add the following template to your `include``:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/gitlab-sast.yml
```

For further usage on how to use the scanner please check the scanner
[docs](https://docs.gitlab.com/ee/user/application_security/dependency_sast/).

#### GitLab Secret Scanner

To enable this scanner, add the following template to your `include``:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/gitlab-secrets.yml
```

For further usage on how to use the scanner please check the scanner
[docs](https://docs.gitlab.com/ee/user/application_security/secret_detection/).

#### Helm Scanning

To enable this template, add the following to your `include``:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/gitlab-secrets.yml
```

This template consists of multiple test stages.

1. [Trivy](https://github.com/aquasecurity/trivy) is doing an config scan of the
   helm charts.
1. The helm chart will be build and all related docker images will be extreacted
1. [Grype](https://github.com/anchore/grype) will scan every detected container

For further usage on how to use / modify the template please check the
[knowledgebase](https://secureops.pages.devops.telekom.de/knowledgebase/safescarf/helm-scanning-guides).

## Variables

The variables have to be set in your gitlab-ci.yml file or in the GitLab CI/CD Settings.

### General

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| SAFESCARF_URL | Yes | '[https://safescarf.domain.tld/](https://safescarf.domain.tld/)' | URL your your SafeSCARF Instance |
| SAFESCARF_TOKEN | Yes | null | API token for API-V2 Endpoint (machine or user token)|
| SAFESCARF_PRODUCTID | Yes | null | ID of your Product in SafeSCARF (will be displayed in the url bar of the browser after accessing the product) |
| SAFESCARF_REIMPORT_DO_NOT_REACTIVATE | No | True | see [docs](https://defectdojo.github.io/django-DefectDojo/integrations/importing/#triage-less-scanners) |

### Engagement

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| SAFESCARF_ENGAGEMENT_PERIOD | No | 7 | Duration in days of the created Engagement |
| SAFESCARF_ENGAGEMENT_STATUS | No | In  Progress | Initial Status of the Engagement when created. Possible Values: Not Started, Blocked, Cancelled, Completed, In Progress, On Hold, Waiting for Resource |
| SAFESCARF_ENGAGEMENT_DEDUPLICATION_ON_ENGAGEMENT | No | true | If enabled deduplication will only mark a finding in this engagement as duplicate of another finding if both findings are in this engagement. If disabled, deduplication is on the product level. |
| SAFESCARF_ENGAGEMENT_BUILD_SERVER | No | null | ID of the Build Server if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_SOURCE_CODE_MANAGEMENT_SERVER | No | null | ID of the SCM Server if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_ORCHESTRATION_ENGINE | No | null | ID of the Orchestration Engine if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_THREAT_MODEL | No | true | |
| SAFESCARF_ENGAGEMENT_API_TEST | No | true | |
| SAFESCARF_ENGAGEMENT_PEN_TEST | No | true | |
| SAFESCARF_ENGAGEMENT_CHECK_LIST | No | true | |

### Scan

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| SAFESCARF_SCAN_MINIMUM_SEVERITY | No | Info | Available values : Info, Low, Medium, High, Critical |
| SAFESCARF_SCAN_ACTIVE | No | true | |
| SAFESCARF_SCAN_VERIFIED | No | true | |
| SAFESCARF_SCAN_CLOSE_OLD_FINDINGS | No | true | |
| SAFESCARF_SCAN_ENVIRONMENT | No | Default | **Recommended to set!**|

## Forking

Feel free to fork this repository and include into your own GitLab Instance. The
only thing you have to take care of is to update the includes in
"gitlab-safescarf.yml" in the repositories root directory.

## Contributing

Feel free to fork this repository and add another scanner or to improve current
implementations.

For new implementations, please follow the naming conventions:
`<product>-<scanner-type>.yml`.
