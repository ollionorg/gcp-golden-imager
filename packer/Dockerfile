FROM alpine:3.14 AS build

ARG PACKER_VERSION
ARG PACKER_VERSION_SHA256SUM
RUN apk update && apk add --upgrade ansible && echo $PATH && which ansible && which ansible-playbook
COPY packer_${PACKER_VERSION}_linux_amd64.zip .
RUN echo "${PACKER_VERSION_SHA256SUM}  packer_${PACKER_VERSION}_linux_amd64.zip" > checksum && sha256sum -c checksum

RUN /usr/bin/unzip packer_${PACKER_VERSION}_linux_amd64.zip


FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest

RUN apt-get -y update && apt-get -y install ca-certificates && rm -rf /var/lib/apt/lists/*  && apt -y update  

# Install dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       sudo systemd systemd-sysv \
       build-essential wget libffi-dev libssl-dev \
       python3-pip python3-dev python3-setuptools python3-wheel python3-apt \
    && rm -rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && apt-get clean

# Upgrade pip to latest version.
RUN pip3 install --upgrade pip

# Install Ansible via pip.
RUN pip3 install ansible && which ansible && which ansible-playbook && ansible --version 

COPY --from=build packer /usr/bin/packer
ENTRYPOINT ["/usr/bin/packer"]
