# Kea-HA

This project provides an interactive CLI tool that makes it easy to automatically build, install, and update
Kea HA deployments using Docker containers.

## Build Status

|  Branch  |                                                                                                            Status                                                                                                            |
|:--------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| `latest` |    [![Kea Docker Image](https://github.com/AzorianSolutions/kea-ha/actions/workflows/build-and-publish.yml/badge.svg?branch=latest)](https://github.com/AzorianSolutions/kea-ha/actions/workflows/build-and-publish.yml)     |
|  `dev`   |      [![Kea Docker Image](https://github.com/AzorianSolutions/kea-ha/actions/workflows/build-and-publish.yml/badge.svg?branch=dev)](https://github.com/AzorianSolutions/kea-ha/actions/workflows/build-and-publish.yml)      |
| `2.5.4`  | [![Kea Docker Image](https://github.com/AzorianSolutions/kea-ha/actions/workflows/build-and-publish.yml/badge.svg?branch=release/2.5.4)](https://github.com/AzorianSolutions/kea-ha/actions/workflows/build-and-publish.yml) |

## [Features](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/project/features.md):

- Can be configured with interactive CLI prompts or a configuration file
- Provides automatic container image building
- Provides automatic database initialization
- Provides automatic database migrations
- Provides automatic HA deployment (two nodes)
- Provides Kea Agent support (REST API)
- Provides easy software updates
- Provides multiple database backend support
    - MySQL
    - Postgres

## TL;DR

To get started quickly with a simple deployment, execute the following commands on a *nix based system
with `bash` and `git` installed:

```
git clone https://github.com/AzorianSolutions/kea-ha.git
cd kea-ha
git checkout latest
./ctrl.sh prepare
./ctrl.sh install
```

## [Project Documentation](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/README.md)

### [Project Information](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/project/README.md)

For information about the project such as feature planning, the roadmap, and milestones, then please see the
[Project Information](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/project/README.md) section of the
wiki.

### [Contributing](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/contributing/README.md)

If you're interested in participating in the project design discussions, or you want to actively submit work to the
project then you should check out the
[Contribution Guide](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/contributing/README.md)!

### [Application Configuration](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/configuration/README.md)

For information about all the ways this application can be configured and what each setting does, please visit the
[Configuration Guide](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/configuration/README.md) section of
the wiki.

### [Application Deployment](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/deployment/README.md)

For information about how to deploy the application in various environments, please visit the
[Deployment Guides](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/deployment/README.md) section of the
wiki.

### [Application Testing](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/testing/README.md)

For information on how to create and execute automated application tests, please visit the
[Testing Guide](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/testing/README.md) section of the wiki.

## [Security Policy](https://github.com/AzorianSolutions/kea-ha/blob/main/.github/SECURITY.md)

Please see our
[Security Policy](https://github.com/AzorianSolutions/kea-ha/blob/main/.github/SECURITY.md).

## [Support Policy](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/support/README.md)

Please see our
[Support Policy](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/support/README.md).

Looking to chat with someone? Join our [Discord Server](https://discord.azorian.solutions).

## [Code of Conduct](https://github.com/AzorianSolutions/kea-ha/blob/main/.github/CODE_OF_CONDUCT.md)

Please see our
[Code of Conduct](https://github.com/AzorianSolutions/kea-ha/blob/main/.github/CODE_OF_CONDUCT.md).

## [License](https://github.com/AzorianSolutions/kea-ha/blob/main/LICENSE)

This project is released under the MIT license. For additional
information, [see the full license](https://github.com/AzorianSolutions/kea-ha/blob/main/LICENSE).

## [Donate](https://www.buymeacoffee.com/AzorianMatt)

Like my work?

<a href="https://www.buymeacoffee.com/AzorianMatt" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

**Want to sponsor me?** Please visit my organization's [sponsorship page](https://github.com/sponsors/AzorianSolutions).
