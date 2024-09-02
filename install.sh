#!/bin/bash

#Installation script for BRETAGNE
#Install docker
# Add Docker's official GPG key:
echo "Install Docker..."
sudo apt-get update -qq 2>/dev/null >/dev/null;
sudo apt-get install ca-certificates curl -qq 2>/dev/null >/dev/null;
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -qq 2>/dev/null >/dev/null;
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -yqq 2>/dev/null >/dev/null;
# Manage Docker as non root user
if ! getent group docker > /dev/null; then
    echo "Add Docker group..."
    sudo groupadd docker
fi

#Install Kathara
echo "Add Kathara depot..."
sudo apt-get install software-properties-common -yqq 2>/dev/null >/dev/null;
sudo apt update -qq 2>/dev/null >/dev/null;
sudo add-apt-repository ppa:katharaframework/kathara -sy 2>/dev/null >/dev/null;
sudo apt update -yqq 2>/dev/null >/dev/null;
echo "Install Kathara..."
sudo apt install kathara -yqq 2>/dev/null >/dev/null;

echo "Kathara installation check..."
kathara check 2>/dev/null >/dev/null;

# Install Python
echo "Installation of pip and Python dependencies..."
sudo apt install python3-pip -yqq 2>/dev/null >/dev/null;
pip3 install yaspin -q --break-system-packages 2>/dev/null >/dev/null;
python3 -m pip install git+https://github.com/saghul/pyuv@master#egg=pyuv -q --break-system-packages 2>/dev/null >/dev/null;
python3 -m pip install "kathara" -q --break-system-packages 2>/dev/null >/dev/null;
python3 -m pip install boto3 -q --break-system-packages 2>/dev/null >/dev/null;

# Download and install BRETAGNE
echo "Cloning the BRETAGNE depot..."
git clone https://github.com/ThomasL53/BRETAGNE.git -q
# Add env to .bashrc
echo "alias bretagne=\"python3 $(pwd)/BRETAGNE/bretagne.py\"" >> ~/.bashrc
source ~/.bashrc
echo "Installation complete. For more help, use: bretagne -h"