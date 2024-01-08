FROM ubuntu:22.04 AS base
RUN apt update
RUN apt install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
        git


FROM base AS builder
ARG KEA_VERSION=2.5.4
ENV DEBIAN_FRONTEND=noninteractive
ENV KEA_VERSION=${KEA_VERSION}
RUN apt install -y --no-install-recommends \
        autoconf \
        automake \
        make \
        pkg-config \
        g++ \
        libtool \
        libssl-dev \
        libboost-dev \
        libboost-system-dev \
        liblog4cplus-dev \
        libmysqlclient-dev \
        libpq-dev \
        postgresql-server-dev-all

RUN mkdir -p /usr/src/kea && \
    cd /usr/src/kea && \
    wget -c https://gitlab.isc.org/isc-projects/kea/-/archive/Kea-${KEA_VERSION}/kea-Kea-${KEA_VERSION}.tar.gz && \
    tar -xzf kea-Kea-${KEA_VERSION}.tar.gz && \
    mv kea-Kea-${KEA_VERSION} ${KEA_VERSION} && \
    cd ${KEA_VERSION}

WORKDIR /usr/src/kea/${KEA_VERSION}

RUN autoreconf --install && \
    ./configure --prefix="" --enable-shell --enable-perfdhcp --with-mysql --with-pgsql && \
    make -j$(nproc) && \
    make install

RUN apt-get purge -y --auto-remove \
        autoconf \
        automake \
        make \
        pkg-config \
        g++ \
        libtool \
        libssl-dev \
        libboost-dev \
        libboost-system-dev \
        liblog4cplus-dev \
        libmysqlclient-dev \
        libpq-dev \
        postgresql-server-dev-all && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/src/kea


FROM base AS runner
ARG KHA_UID=0
ARG KHA_USER=root
ARG KHA_GID=0
ARG KHA_GROUP=root
ARG KHA_ROOT=/opt/kha
ARG KEA_VERSION=2.5.4
ENV DEBIAN_FRONTEND=noninteractive
ENV KHA_UID=${KHA_UID}
ENV KHA_USER=${KHA_USER}
ENV KHA_GID=${KHA_GID}
ENV KHA_GROUP=${KHA_GROUP}
ENV KHA_ROOT=${KHA_ROOT}
ENV KEA_VERSION=${KEA_VERSION}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt install -y --no-install-recommends \
        gettext-base \
        supervisor \
        mysql-client \
        postgresql-client \
        liblog4cplus-2.0.5 \
        libmysqlclient21 \
        libpq5

WORKDIR ${KHA_ROOT}

# Copy the Kea binaries, documentation, and source code into the container
COPY --from=builder /sbin/ /sbin/
COPY --from=builder /usr/lib/*kea* /usr/lib/
COPY --from=builder /share/doc/kea /share/doc/kea
COPY --from=builder /share/kea /share/kea

# Copy the entrypoint script into the container
COPY ./entrypoint.sh /entrypoint.sh

# Create service directories and update permissions
RUN mkdir -p /etc/kea && \
    mkdir -p /var/lib/kea && \
    mkdir -p /var/log/kea && \
    mkdir -p /var/run/kea && \
    mkdir -p /var/log/supervisor/ && \
    # Update service permissions \
    chmod +x /entrypoint.sh && \
    chown -R ${KHA_UID}:${KHA_GID} /entrypoint.sh && \
    chown -R ${KHA_UID}:${KHA_GID} /etc/kea && \
    chown -R ${KHA_UID}:${KHA_GID} /var/lib/kea && \
    chown -R ${KHA_UID}:${KHA_GID} /var/log/kea && \
    chown -R ${KHA_UID}:${KHA_GID} /var/run/kea && \
    chown -R ${KHA_UID}:${KHA_GID} /var/log/supervisor


FROM runner AS runner-dev
ARG KHA_UID=0
ARG KHA_GID=0
ENV DEBIAN_FRONTEND=noninteractive
ENV KHA_UID=${KHA_UID}
ENV KHA_GID=${KHA_GID}

RUN apt install -y --no-install-recommends \
        lsof \
        iproute2 \
        net-tools \
        iputils-ping \
        iptraf

USER ${KHA_UID}:${KHA_GID}

EXPOSE 8000-8001/tcp 67/tcp 67/udp

ENTRYPOINT ["/entrypoint.sh"]

HEALTHCHECK CMD [ "supervisorctl", "status" ]
