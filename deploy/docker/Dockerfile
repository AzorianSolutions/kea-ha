FROM ubuntu:22.04
LABEL org.opencontainers.image.authors="Azorian Solutions <help@azorian.solutions>"
ARG KHA_VERSION=0.1.0
ARG KHA_SHARE_PATH=/usr/share/kea-ha
ARG KEA_VERSION=2.5.4
ENV DEBIAN_FRONTEND=noninteractive
ENV KHA_VERSION=${KHA_VERSION}
ENV KHA_SHARE_PATH=${KHA_SHARE_PATH}
ENV KEA_VERSION=${KEA_VERSION}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt update

RUN apt install -y --no-install-recommends \
        gettext-base \
        ca-certificates \
        supervisor \
        lsof \
        iproute2 \
        net-tools \
        iputils-ping \
        iptraf \
        mysql-client \
        postgresql-client \
        liblog4cplus-2.0.5 \
        libmysqlclient21 \
        libpq5 \
        curl \
        wget \
        git \
        autoconf \
        automake \
        make \
        libboost-dev \
        libboost-system-dev \
        libssl-dev \
        liblog4cplus-dev \
        g++ \
        libtool \
        pkg-config \
        libmysqlclient-dev \
        libpq-dev \
        postgresql-server-dev-all

RUN mkdir -p /usr/src/kea && \
    cd /usr/src/kea && \
    wget -c https://gitlab.isc.org/isc-projects/kea/-/archive/Kea-${KEA_VERSION}/kea-Kea-${KEA_VERSION}.tar.gz && \
    tar -xzf kea-Kea-${KEA_VERSION}.tar.gz && \
    cd kea-Kea-${KEA_VERSION}

WORKDIR /usr/src/kea/kea-Kea-${KEA_VERSION}

RUN autoreconf --install && \
    ./configure --prefix="" --enable-shell --enable-perfdhcp --with-mysql --with-pgsql && \
    make -j$(nproc) && \
    make install

WORKDIR ${KHA_SHARE_PATH}

RUN cp -Ra /share/* /usr/share/ && \
    apt-get purge -y --auto-remove \
        git \
        autoconf \
        make \
        libboost-dev \
        libboost-system-dev \
        libssl-dev \
        liblog4cplus-dev \
        g++ \
        libtool \
        pkg-config \
        libmysqlclient-dev \
        libpq-dev \
        postgresql-server-dev-all && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --system --no-create-home --disabled-password --group kea

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
