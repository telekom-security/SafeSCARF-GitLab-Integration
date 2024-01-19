# GitLab-CI SafeSCARF 2.0

> Release 2.0 introduces some major changes!
>
> **1. Moving away from a "one integration fits all" approach.**
>
> We discovered, that thise approach is pretty error prone, especially when
> relying on third party templates like a dso scanner.
>
> **2. Adapt a more dynamic (plugin style) approach**
>
> For the new approach, the `gitlab-integration.yml` will only contain the
> safescarf interaction parts. Scanning templates for uploading can be included
> on demand.
> By doing this, projects have the ability to easier adapt and implement their
> own adapters. (They are still welcome to share their adapters with us to
> provide it to other projects).
>
> **3. Use shell script for safescarf interactions**
>
> While using and maintaining v1.0 we discovered, that some projects need to
> customize their interaction with safescarf during the pipeline which lead to
> problems with the static pipeline definition. Instead we are going to create
> an bash script that can be executed with custom arguments to interact with
> safescarf.
> Also debugging the pipeline and multi-line comments becomes much easier with
> this approach.
>
> **4. Rely on Tags / Releases for integration versioning**
>
> Primary Idea of v1.0 was to have a single include that auto updates, if
> neccessary changes have been detected.
> Problem with this approach was that pipelines failed since the integration has
> updated and the projects did not get any information about this.
> With v2.0 Projects should test and pin a specific version of the integration
> and decide on their own when to upgrade. (We wil provide detailed release
> notes). We will also offer a `latest` tag for those who want to be on the
> latest edge on their own risk.

This repository provides a template for gitlab pipelines to integrate with
[SafeSCARF](https://documentation.portal.pan-net.cloud/safescarf-product/)
(based on [DefectDojo](https://www.defectdojo.org)).

It supports the following templates:

- [DevSecOps Container Scanner By DTIT](https://gitlab.devops.telekom.de/devsecops-tools/container-scanner)
- [GitLab Dependency Scanner](https://docs.gitlab.com/ee/user/application_security/dependency_scanning/)
- [GitLab Container Scanner](https://docs.gitlab.com/ee/user/application_security/container_scanning/)
- [GitLab SAST](https://docs.gitlab.com/ee/user/application_security/sast/)
- [GitLab Secret Scanner](https://docs.gitlab.com/ee/user/application_security/secret_detection/)
- Helm Scanning (Config by [Trivy](https://github.com/aquasecurity/trivy) and docker images by [Grype](https://github.com/anchore/grype))

Please see [Scan Engines](#scan-engines) to understand how to enable them and
which are enabled by default.

> Some templates, like the gitlab-container scanner are not directly plug and
> play and need some minor configurations.
>
> **You can still use the original variables to configure your jobs!**

## Structure

### gitlab-safescarf.yml

There is only one mandatory `include`:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/2.0-rc8/gitlab-safescarf.yml
```

The `gitlab-safescarf.yml` template provides the neccessary default variables
and bundles the
[Safescarf-Connector](https://gitlab.devops.telekom.de/secureops/safescarf/safescarf-connector)
to interact with the SafeSCARF api.

### plugins

The scan jobs itself can be thought of a plugin. On the one hand they take care
to actually scan the content and keep the result file and on the other hand,
they extend the main template to interact with SafeSCARF and upload the result
file with the correct metadata.

The plugins are located in
[Implementations](https://gitlab.devops.telekom.de/secureops/safescarf/safescarf-integration/-/tree/master/implementations?ref_type=heads)

## Usage

To use this integration, simply include the main file `gitlab-safescarf.yml` as a
remote and include the desired plugins after:

```yaml
include:
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/2.0-rc8/gitlab-safescarf.yml
  - project: 'secureops/safescarf/safescarf-integration'
    ref: "master"
    file: 'implementations/devsecops-container.yml'
  - https://raw.githubusercontent.com/telekom-security/SafeSCARF-GitLab-Integration/2.0-rc8/implementations/gitlab-secrets.yml
```

> In case of the DSO Container Scanner you need to include it from gitlab via
> the project include syntax (see above) since it is not publicly available.

After, you can configure the desired templates (see [Templates](#templates)).

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

### Xray Container

Jfrog Xray scans docker containers for any known vulnerabilites and posts the findings with metadata including remediation suggestions to SafeSCARF. For this to function, you need to include the variable XRAY_CONTAINER_IMAGE with the ID of your target Container Image (e.g `Nginx:1.0.0`) in your `.gitlab-ci.yml` file. Additionally, add an `ARTIFACTORY_TOKEN` to your Settings -> CI/CD -> Variables.
Generate this token by logging into Artifactory, clicking on Welcome, your.email on the top-right -> Set Me Up -> docker -> Generate Token & Create Instructions.

| Variable        | Mandatory | Default | Description |
| -------------   |:-------------:| -----:| -----: |
| ARTIFACTORY_TOKEN | Yes | null | API token for Artifactory |
| XRAY_CONTAINER_IMAGE | Yes | "" | ID of the Container Image |

## Forking

Feel free to fork this repository and include into your own GitLab Instance.
The only thing you have to take care of is to update the includes in "gitlab-safescarf.yml" in the repositories root directory.

## Contributing

Feel free to add another scanner or to improve current implementations.

For new implementations, please follow the naming conventions: `<product>-<scanner-type>.yml`.
