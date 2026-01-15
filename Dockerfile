FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    git \
    quilt \
    parted \
    libfile-whisperer-perl \
    coreutils \
    qemu-user-static \
    debootstrap \
    zerofree \
    zip \
    dosfstools \
    bsdtar \
    sudo \
    curl

WORKDIR /build

# Clone pi-gen
RUN git clone --depth 1 https://github.com/RPi-Distro/pi-gen.git

WORKDIR /build/pi-gen

# Configuration for Nova OS build
RUN echo "IMG_NAME='NovaOS'" > config
RUN echo "RELEASE='bookworm'" >> config
RUN echo "DEPLOY_COMPRESSION='zip'" >> config

# Copy Nova OS source into the build environment
COPY . /build/nova-os

# Create a custom stage for Nova OS
RUN mkdir -p stage2/01-nova-os
RUN echo "cd /home/pi/nova-os/scripts && ./setup.sh && ./kiosk_setup.sh" > stage2/01-nova-os/01-run.sh
RUN chmod +x stage2/01-nova-os/01-run.sh

CMD ["./build.sh"]
