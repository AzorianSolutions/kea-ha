# Kea-HA

## Project Features

The purpose of this document is to provide some explanation about key tool features that really drive the value of
the product.

### Table of Contents

- [Interactive Configuration Tool](#interactive-configuration-tool)
- [HA Mode Deployment](#ha-mode-deployment)
- [Kea Agent Support](#kea-agent-support)
- [Kea Software Updates](#kea-software-updates)
- [Multiple Backend Support](#multiple-backend-support)
  - [MySQL](#mysql)
  - [Postgres](#postgres)

### Interactive Configuration Tool

The container control script (`ctrl.sh`) contains an interactive configuration tool that can be used to configure
the application. The tool is designed to be easy to use and intuitive. It is also designed to be used in a
non-interactive manner as well.

### HA Mode Deployment

The container can be deployed in HA mode which will automatically configure the application to use operating in a
load-balancing configuration with another node. This tool can be used on each node to easily deploy a clustered pair.

### Kea Agent Support

The container comes with Kea Agent support built-in. This means that the container will run an instance
of the Kea Agent service to provide a REST API for the Kea services.

### Kea Software Updates

The container control script (`ctrl.sh`) contains an update tool that can be used to update the application to
a different version. This will automatically build the new version of the container and deploy it to the system.
Additionally, it will run any available database migrations.

### Multiple Backend Support

The container comes complete with all database backend support compiled in at build time. This means that the
application can be configured to use any of the supported database backends. The following database backends are
supported:

#### MySQL

The MySQL backend is fully supported including automatic database initialization and migration. The application will
automatically initialize the database and run the migrations on startup if the database does not exist or is missing
key tables.

#### Postgres

The Postgres backend is fully supported including automatic database initialization and migration. The application
will automatically initialize the database and run the migrations on startup if the database does not exist or is
missing key tables.
