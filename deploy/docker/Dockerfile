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
        postgresql-server-dev-all \
        liblog4cplus-2.0.5 \
        libmysqlclient21 \
        libpq5

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
        postgresql-server-dev-all \
        liblog4cplus-2.0.5 \
        libmysqlclient21 \
        libpq5 && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /usr/src/kea


FROM base AS runner
ARG KHA_SHARE_PATH=/usr/share/kea-ha
ARG KEA_VERSION=2.5.4
ENV DEBIAN_FRONTEND=noninteractive
ENV KHA_SHARE_PATH=${KHA_SHARE_PATH}
ENV KEA_VERSION=${KEA_VERSION}
LABEL org.opencontainers.image.title="ISC Kea HA (${KEA_VERSION})"
LABEL org.opencontainers.image.description="Built from Kea source ${KEA_VERSION} with database back-end support",
LABEL org.opencontainers.image.url="https://github.com/AzorianSolutions/kea-ha",
LABEL org.opencontainers.image.source="https://github.com/AzorianSolutions/kea-ha",
LABEL org.opencontainers.image.version="${KEA_VERSION}",
LABEL org.opencontainers.image.authors="Azorian Solutions <help@azorian.solutions>"
LABEL org.opencontainers.image.created="2024-01-06T20:42:00.000Z",
LABEL org.opencontainers.image.licenses="MIT"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt install -y --no-install-recommends \
        gettext-base \
        supervisor \
        mysql-client \
        postgresql-client

RUN adduser --system --no-create-home --disabled-password --group kea

WORKDIR ${KHA_SHARE_PATH}

# Copy the Kea binaries, documentation, and source code into the container
COPY --from=builder /sbin/ /sbin/
COPY --from=builder /usr/lib/*kea* /usr/lib/
COPY --from=builder /share/doc/kea /share/doc/kea
COPY --from=builder /share/kea /share/kea

# Copy the default environment settings into the container
COPY defaults.env ${KHA_SHARE_PATH}/defaults.env

# Copy the configuration templates into the container
COPY deploy/tpl/* ${KHA_SHARE_PATH}/tpl/

# Create the entrypoint script in the container
COPY deploy/inc/entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable
RUN chmod +rwx /entrypoint.sh

VOLUME ["/etc/kea", "${KHA_SHARE_PATH}", "/var/lib/kea", "/var/log/kea", "/var/log/supervisor"]

EXPOSE 8000-8001/tcp 67/tcp 67/udp

ENTRYPOINT ["/entrypoint.sh"]

HEALTHCHECK CMD [ "supervisorctl", "status" ]


FROM runner AS runner-dev
RUN apt install -y --no-install-recommends \
        lsof \
        iproute2 \
        net-tools \
        iputils-ping \
        iptraf
