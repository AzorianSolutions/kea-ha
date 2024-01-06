# Kea-HA

## Configuration Guide

### Getting Started

The application provides a lot of fluidity in how it can be configured. The application is designed to be
flexible and allow for a wide variety of deployment scenarios which include bare metal, virtual machines,
containers, and cloud environments.

There is a plethora of environment configuration settings that can be used to bootstrap the application for
varying environments. All of these settings can be set using environment variables or by creating a
`.env` file in the `build/docker` directory of the application. The file should contain one or more
environment variables to be loaded at application startup. Additionally, this file will be automatically
created with each execution of the `ctrl.sh configure` command or any other command that provides interactive
configuration support such as `ctrl.sh install`.

For more information on these settings, see the
[Application Settings Guide](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/configuration/settings/README.md).

#### Secrets Support

There is currently no support for secrets in the application. This is a planned feature and will be
implemented in the near future.

### [Application Settings](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/configuration/settings/README.md)

To get an in-depth understanding of the many application settings available, see the
[Application Settings Guide](https://github.com/AzorianSolutions/kea-ha/blob/main/docs/wiki/configuration/settings/README.md).
