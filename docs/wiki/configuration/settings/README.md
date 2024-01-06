# Kea-HA

## Configuration Guide

### Application Settings Guide

The configuration settings listed in this section are used for bootstrapping the application before
initialization. Configuration settings are only placed here if the setting is required to bootstrap
the application and only changes for the deployment environment.

All configuration settings are prefixed with `KEA_` and are set using environment variables. The
environment variables can be set in a `.env` file in the `build/docker` directory of the application.
This file is generated as the result of executing the `ctrl.sh configure` command or any other command
that provides interactive configuration such as `ctrl.sh install`.

#### KEA_IMAGE_REPO_URL

`Options:` docker.io, cloudsmith.io, etc \
`Default:` docker.io

Specifies the URL of the container image repository to use when pushing and pulling images for the application.

#### KEA_IMAGE_REPO_USERNAME

`Default:` azoriansolutions

Specifies the username of the account to use when pushing and pulling images for the application.

#### KEA_IMAGE_REPO_PASSWORD

`Default:` 

Specifies the password of the account to use when pushing and pulling images for the application.

#### KEA_IMAGE_NAME

`Default:` kea-ha

Specifies the image name to use when pushing and pulling images for the application.

#### KEA_VERSION

`Default:` 2.5.4

Specifies the version of the Kea source to use when building images for the application.

#### KEA_LOG_SEVERITY

`Options:` DEBUG, INFO, WARN, ERROR, CRITICAL \
`Default:` INFO

Specifies the minimum severity of log messages to output to the console and log files.

#### KEA_ADMIN_USER

`Default:` kea

Specifies the username of the admin user for Kea services.

#### KEA_ADMIN_PASSWORD

`Default:` kea

Specifies the password of the admin user for Kea services.

#### KEA_CONTAINER_INTERFACE

`Default:` eth2

Specifies the name of the **container** network interface to use for Kea DHCP services.

Unless you are modifying the container networking design, this should be left as the default value.

#### KEA_DB_TYPE

`Options:` mysql, postgresql \

Specifies the type of database to use for Kea services.

#### KEA_DB_VERSION

`Default:` 8.2

Specifies the version of the database to use for Kea services.

This setting is automatically set based on the value of `KEA_DB_TYPE`.

#### KEA_DB_VERSION_MYSQL

`Default:` 8.2

Specifies the version of the MySQL database to use for Kea services.

#### KEA_DB_VERSION_PGSQL

`Default:` 16.1

Specifies the version of the PostgreSQL database to use for Kea services.

#### KEA_DB_HOST

`Default:` db

Specifies the hostname of the database server to use for Kea services.

Unless you are modifying the Docker Compose configuration, this should be left as the default value.

#### KEA_DB_PORT

`Default:` 3306

Specifies the port of the database server to use for Kea services.

This setting is automatically set based on the value of `KEA_DB_TYPE`.

#### KEA_DB_PORT_MYSQL

`Default:` 3306

Specifies the port of the MySQL database server to use for Kea services.

#### KEA_DB_PORT_PGSQL

`Default:` 5432

Specifies the port of the PostgreSQL database server to use for Kea services.

#### KEA_DB_USER

`Default:` kea

Specifies the username of the database user to use for Kea services.

#### KEA_DB_PASSWORD

`Default:` kea

Specifies the password of the database user to use for Kea services.

#### KEA_DB_ROOT_PASSWORD

`Default:` kea

Specifies the password of the database root user to use for Kea services.

#### KEA_DB_NAME

`Default:` kea

Specifies the name of the database to use for Kea services.

#### KEA_DB_SCHEMA

`Default:` public

Specifies the name of the database schema to use for Kea services when using Postgres as a backend.

#### KEA_DHCP_INTERFACE

`Default:` eth2

Specifies the name of the **host** network interface to use for Kea DHCP services.

#### KEA_DHCP4_IP

`Default:` 192.168.1.1

Specifies the IPv4 address of the Kea services.

#### KEA_DHCP4_SUBNET

`Default:` 192.168.1.0/29

Specifies the IPv4 subnet of the Kea services.

#### KEA_DHCP4_GW_IP

`Default:` 192.168.1.6

Specifies the IPv4 gateway address of the Kea services.

#### KEA_MGMT_INTERFACE

`Default:` eth1

Specifies the name of the **host** network interface to use for Kea management services.

#### KEA_MGMT4_IP

`Default:` 192.168.2.10

Specifies the IPv4 address of the Kea management services.

#### KEA_MGMT4_SUBNET

`Default:` 192.168.2.0/24

Specifies the IPv4 subnet of the Kea management services.

#### KEA_MGMT4_GW_IP

`Default:` 192.168.2.1

Specifies the IPv4 gateway address of the Kea management services.

#### KEA_HA_ENABLED

`Options:` yes, no \
`Default:` no

Specifies whether to enable Kea HA services.

#### KEA_HA_HOST_NAME

`Options:` node1, node2 \
`Default:` node1

Specifies the node name of this node as it relates to an HA cluster.

This setting is automatically set based on the value of `KEA_HA_ROLE`.

#### KEA_HA_HOST_IP

`Default:` 192.168.2.10

Specifies the IPv4 management address of this node as it relates to an HA cluster.

This setting is automatically set based on the value of `KEA_HA_ROLE`.

#### KEA_HA_ROLE

`Options:` primary, secondary \
`Default:` primary

Specifies the role of this node as it relates to an HA cluster.

#### KEA_HA_HOST1_IP

`Default:` 192.168.2.10

Specifies the IPv4 management address of the primary node as it relates to an HA cluster.

#### KEA_HA_HOST2_IP

`Default:` 192.168.2.11

Specifies the IPv4 management address of the secondary node as it relates to an HA cluster.
