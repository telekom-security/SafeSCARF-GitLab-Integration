# GitLab-CI SafeSCARF 2.0

> **UPDATE:** This integration is now following the [Branch Git
> Wokflow](https://secureops.pages.devops.telekom.de/knowledgebase/safescarf/branch-git-workflows)
> and therefore sets the `SAFESCARF_ENGAGEMENT_DEDUPLICATION_ON_ENGAGEMENT` to
> `false` by default (previously it defaulted to `true`).

This repository provides a template for gitlab pipelines to integrate with
[SafeSCARF](https://portal.pan-net.cloud/docs/SafeSCARF%20product)
(based on [DefectDojo](https://www.defectdojo.org)).

- [GitLab-CI SafeSCARF 2.0](#gitlab-ci-safescarf-20)
    - [Structure](#structure)
        - [gitlab-safescarf.yml](#gitlab-safescarfyml)
        - [plugins](#plugins)
    - [Usage](#usage)
        - [Scan Engines](#scan-engines)
            - [DevSecOps Container Scanner By DTIT](#devsecops-container-scanner-by-dtit)
            - [DTSP Container Scan](#dtsp-container-scan)
                - [Configuration](#configuration)
            - [GitLab Container Scanner](#gitlab-container-scanner)
            - [GitLab Dependency Scanner](#gitlab-dependency-scanner)
            - [GitLab SAST Scanner](#gitlab-sast-scanner)
            - [GitLab Secret Scanner](#gitlab-secret-scanner)
            - [Helm Scanning](#helm-scanning)
            - [Xray Container Scan](#xray-container-scan)
                - [Configuration](#configuration-1)
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

#### DTSP Container Scan

The [Deutsche Telekom Scan Platform (DTSP)](https://dtsp.telekom-dienste.de/) is
the preferred way of T-Sec to scan container images. Internally grype is used.
Besides, SBOMS are generated, mapped to the container digest and continously
scanned to prevent new image scans.

To enable this Feature you have to include the template:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/dtsp-container.yml
```

##### Configuration

**GLOBAL Variables:**

| Variable         | Mandatory | Default                         | Description                                                                                                                       |
| ---------------- | --------- | ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| DTSP_API_KEY     | Yes       |                                 | API Token of DTSP (can be created in the user profile) - see [FAQ](https://dtsp.telekom-dienste.de/help/faq) for MCICD Source IPs |
| DTSP_URL         | Yes       | https://dtsp.telekom-dienste.de | URL of the used DTSP instance                                                                                                     |
| DTSP_RESULT_FILE | Yes       | dtsp-scanresults.json           | default filename for the results file (normally, you should not change this)                                                      |

**JOB specific variables:**

| Variable            | Mandatory | Default | Description                                                               |
| ------------------- | --------- | ------- | ------------------------------------------------------------------------- |
| DTSP_REGISTRY_PW    | No        |         | Needed if the image is behind a registry authentication                   |
| DTSP_REGISTRY_TOKEN | No        |         | Needed if the image is behind a registry authentication                   |
| DTSP_REGISTRY_USER  | No        |         | Needed if the image is behind a registry authentication                   |
| DTSP_IMAGE          | Yes       |         | The Image that should be scanned by DTSP (must include the registry path) |

Further details about DTSP can be found within their [docs](https://dtsp.telekom-dienste.de/help)

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

#### Xray Container Scan

Jfrog Xray scans docker containers for any known vulnerabilites and posts the
findings with metadata including remediation suggestions to SafeSCARF. For this
to function, you need to include the variable `XRAY_CONTAINER_IMAGE` with the ID
of your target Container Image (e.g `nginx:1.0.0`) in your `.gitlab-ci.yml`
file. Additionally, add an `ARTIFACTORY_TOKEN` to your `Settings -> CI/CD ->
Variables`. Generate this token by logging into Artifactory, clicking on
Welcome, your email on the top-right -> Set Me Up -> docker -> Generate Token &
Create Instructions.

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/<version>/implementations/xray-container.yml
```

##### Configuration

| Variable             | Mandatory | Default | Description               |
| -------------------- | --------- | ------- | ------------------------- |
| ARTIFACTORY_TOKEN    | Yes       | null    | API token for Artifactory |
| XRAY_CONTAINER_IMAGE | Yes       | ""      | ID of the Container Image |

## Variables

The variables have to be set in your gitlab-ci.yml file or in the GitLab CI/CD Settings.

### General

| Variable                             | Mandatory |                                                          Default |                                                                                                   Description |
| ------------------------------------ | :-------: | ---------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------: |
| SAFESCARF_URL                        |    Yes    | '[https://safescarf.domain.tld/](https://safescarf.domain.tld/)' |                                                                              URL your your SafeSCARF Instance |
| SAFESCARF_TOKEN                      |    Yes    |                                                             null |                                                         API token for API-V2 Endpoint (machine or user token) |
| SAFESCARF_PRODUCT_ID                 |    Yes    |                                                             null | ID of your Product in SafeSCARF (will be displayed in the url bar of the browser after accessing the product) |
| SAFESCARF_REIMPORT_DO_NOT_REACTIVATE |    No     |                                                             True |       see [docs](https://defectdojo.github.io/django-DefectDojo/integrations/importing/#triage-less-scanners) |

### Engagement

| Variable                                           | Mandatory |      Default |                                                                                                                                                                                       Description |
| -------------------------------------------------- | :-------: | -----------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| SAFESCARF_ENGAGEMENT_PERIOD                        |    No     |            7 |                                                                                                                                                        Duration in days of the created Engagement |
| SAFESCARF_ENGAGEMENT_STATUS                        |    No     | In  Progress |                                            Initial Status of the Engagement when created. Possible Values: Not Started, Blocked, Cancelled, Completed, In Progress, On Hold, Waiting for Resource |
| SAFESCARF_ENGAGEMENT_DEDUPLICATION_ON_ENGAGEMENT   |    No     |         true | If enabled deduplication will only mark a finding in this engagement as duplicate of another finding if both findings are in this engagement. If disabled, deduplication is on the product level. |
| SAFESCARF_ENGAGEMENT_BUILD_SERVER                  |    No     |         null |                                                                                                                                                 ID of the Build Server if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_SOURCE_CODE_MANAGEMENT_SERVER |    No     |         null |                                                                                                                                                   ID of the SCM Server if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_ORCHESTRATION_ENGINE          |    No     |         null |                                                                                                                                         ID of the Orchestration Engine if configured in SafeSCARF |
| SAFESCARF_ENGAGEMENT_THREAT_MODEL                  |    No     |         true |                                                                                                                                                                                                   |
| SAFESCARF_ENGAGEMENT_API_TEST                      |    No     |         true |                                                                                                                                                                                                   |
| SAFESCARF_ENGAGEMENT_PEN_TEST                      |    No     |         true |                                                                                                                                                                                                   |
| SAFESCARF_ENGAGEMENT_CHECK_LIST                    |    No     |         true |                                                                                                                                                                                                   |

### Scan

| Variable                          | Mandatory | Default |                                          Description |
| --------------------------------- | :-------: | ------: | ---------------------------------------------------: |
| SAFESCARF_SCAN_MINIMUM_SEVERITY   |    No     |    Info | Available values : Info, Low, Medium, High, Critical |
| SAFESCARF_SCAN_ACTIVE             |    No     |    true |                                                      |
| SAFESCARF_SCAN_VERIFIED           |    No     |    true |                                                      |
| SAFESCARF_SCAN_CLOSE_OLD_FINDINGS |    No     |    true |                                                      |
| SAFESCARF_SCAN_ENVIRONMENT        |    No     | Default |                              **Recommended to set!** |

## Forking

Feel free to fork this repository and include into your own GitLab Instance. The
only thing you have to take care of is to update the includes in
"gitlab-safescarf.yml" in the repositories root directory.

## Contributing

Feel free to fork this repository and add another scanner or to improve current
implementations.

For new implementations, please follow the naming conventions:
`<product>-<scanner-type>.yml`.

More Details can be found in our
[knowledgebase](https://secureops.pages.devops.telekom.de/knowledgebase/safescarf/gitlab-integrations)
