#!/bin/bash

# Nova OS Image Builder Documentation
# This script explains how to create a flashable .img for your Raspberry Pi 4.

cat <<EOF
###############################################################################
#                           NOVA OS IMAGE BUILDER                             #
###############################################################################

Since you are on macOS and building a Raspberry Pi image requires a Linux 
environment with loopback support, I have set up two ways to build your .img:

--- OPTION 1: CLOUD BUILD (Recommended) ---

I have created a GitHub Actions workflow in:
.github/workflows/build_image.yml

To build your image:
1. Push this project to a GitHub repository.
2. Go to the 'Actions' tab.
3. Select 'Build Nova OS Image' and click 'Run workflow'.
4. Once finished, download the 'nova-os-image' artifact.

--- OPTION 2: LOCAL BUILD (Requires Docker) ---

If you install Docker on your Mac, you can build it locally:
1. Run: docker build -t nova-os-builder .
2. Run: docker run --privileged -v $(pwd)/deploy:/build/pi-gen/deploy nova-os-builder

--- OPTION 3: MANUAL INSTALL ---

If you already have a Pi running Raspberry Pi OS:
1. Copy the 'offline_assistant' folder to your Pi.
2. Run: cd offline_assistant/scripts && ./setup.sh && ./kiosk_setup.sh
3. Reboot.

EOF
