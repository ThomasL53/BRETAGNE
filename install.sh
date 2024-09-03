#!/bin/bash

# Installation script for BRETAGNE
LOG_FILE="/temp/InstallBRETAGNE.log"

# Créer le fichier log
touch "$LOG_FILE"

# Installation de Docker
echo "Install Docker..." | tee -a "$LOG_FILE"
sudo apt-get update -qq >> "$LOG_FILE" 2>&1
sudo apt-get install ca-certificates curl -qq >> "$LOG_FILE" 2>&1
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc >> "$LOG_FILE" 2>&1
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Ajouter le dépôt à Apt sources
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list >> "$LOG_FILE" 2>&1
sudo apt-get update -qq >> "$LOG_FILE" 2>&1
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -yqq >> "$LOG_FILE" 2>&1

# Gérer Docker en tant qu'utilisateur non root
if ! getent group docker > /dev/null; then
    echo "Add Docker group..." | tee -a "$LOG_FILE"
    sudo groupadd docker
fi

# Installation de Kathara
echo "Add Kathara depot..." | tee -a "$LOG_FILE"
sudo apt-get install software-properties-common -yqq >> "$LOG_FILE" 2>&1
sudo apt update -qq >> "$LOG_FILE" 2>&1
sudo add-apt-repository ppa:katharaframework/kathara -sy >> "$LOG_FILE" 2>&1
sudo apt update -yqq >> "$LOG_FILE" 2>&1
echo "Install Kathara..." | tee -a "$LOG_FILE"
sudo apt install kathara -yqq >> "$LOG_FILE" 2>&1

echo "Kathara installation check..." | tee -a "$LOG_FILE"
kathara check >> "$LOG_FILE" 2>&1

# Installation de Python
echo "Installation of pip and Python dependencies..." | tee -a "$LOG_FILE"
sudo apt install python3-pip -yqq >> "$LOG_FILE" 2>&1
pip3 install yaspin -q --break-system-packages >> "$LOG_FILE" 2>&1
python3 -m pip install git+https://github.com/saghul/pyuv@master#egg=pyuv -q --break-system-packages >> "$LOG_FILE" 2>&1
python3 -m pip install "kathara" -q --break-system-packages >> "$LOG_FILE" 2>&1
python3 -m pip install boto3 -q --break-system-packages >> "$LOG_FILE" 2>&1

# Télécharger et installer BRETAGNE
echo "Cloning the BRETAGNE depot..." | tee -a "$LOG_FILE"
git clone https://github.com/ThomasL53/BRETAGNE.git -q >> "$LOG_FILE" 2>&1

# Ajouter env à .bashrc
echo "alias bretagne=\"python3 $(pwd)/BRETAGNE/bretagne.py\"" >> ~/.bashrc
source ~/.bashrc
echo "Installation complete. For more help, use: bretagne -h" | tee -a "$LOG_FILE"