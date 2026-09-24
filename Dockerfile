# EMANE TDMA Simulation Environment Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    iproute2 \
    iptables \
    net-tools \
    iputils-ping \
    tcpdump \
    curl \
    git \
    build-essential \
    autoconf \
    automake \
    libtool \
    libxml2-dev \
    libprotobuf-dev \
    protobuf-compiler \
    libpcap-dev \
    libpcre3-dev \
    python3-networkx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Run schedule optimizer and bridge
CMD ["python3", "tdma_brain.py"]
