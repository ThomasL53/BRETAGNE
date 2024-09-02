#!/bin/bash

#Installation script for BRETAGNE

#install Kathara
echo "Add Kathara depot..."
sudo apt-get install software-properties-common -y
sudo apt update
sudo add-apt-repository -y ppa:katharaframework/kathara
sudo apt update
sudo apt install -y kathara

#install docker
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y


# Manage Docker as non root user
if ! getent group docker > /dev/null; then
    echo "Add Docker group..."
    sudo groupadd docker
fi

echo "Kathara installation check..."
kathara check

# Install Python
echo "Installation of pip and Python dependencies..."
sudo apt install -y python3-pip
pip3 install yaspin
python3 -m pip install git+https://github.com/saghul/pyuv@master#egg=pyuv
python3 -m pip install "kathara"
python3 -m pip install boto3

# Download and install BRETAGNE
echo "Cloning the BRETAGNE depot..."
git clone https://github.com/ThomasL53/BRETAGNE.git
cd BRETAGNE || { echo "Access to BRETAGNE directory failed"; exit 1; }

# Add env.sh source to .bashrc
if [ -f env.sh ]; then
    echo "source $(pwd)/env.sh" >> ~/.bashrc
else
    echo "The env.sh file cannot be found."
fi

echo "Installation complete. For more help, use: bretagne -h"