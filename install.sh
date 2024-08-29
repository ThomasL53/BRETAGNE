#!/bin/bash

# Script d'installation pour BRETAGNE

# Installer Kathara
echo "Ajout du dépôt Kathara..."
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


# Gérer Docker en tant qu'utilisateur non-root
if ! getent group docker > /dev/null; then
    echo "Ajout du groupe Docker..."
    sudo groupadd docker
else
    echo "Le groupe Docker existe déjà."
fi

# Vérification de l'installation de Kathara
echo "Vérification de l'installation de Kathara..."
kathara check

# Installer les dépendances Python
echo "Installation de pip et des dépendances Python..."
sudo apt install -y python3-pip
pip3 install yaspin
python3 -m pip install git+https://github.com/saghul/pyuv@master#egg=pyuv
python3 -m pip install "kathara"
python3 -m pip install boto3

# Télécharger et installer BRETAGNE
echo "Clonage du dépôt BRETAGNE..."
git clone https://github.com/ThomasL53/BRETAGNE.git
cd BRETAGNE || { echo "Échec de l'accès au répertoire BRETAGNE"; exit 1; }

# Source du fichier env.sh
if [ -f env.sh ]; then
    echo "Sourcing env.sh..."
    source env.sh
else
    echo "Le fichier env.sh est introuvable."
fi

# Message final
echo "Installation terminée. Pour plus d'aide, utilisez : bretagne -h"
