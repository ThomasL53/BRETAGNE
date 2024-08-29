#!/bin/bash

# Script d'installation pour BRETAGNE

# Installer Kathara
echo "Ajout du dépôt Kathara..."
sudo apt-get install software-properties-common -y
sudo apt update
sudo add-apt-repository -y ppa:katharaframework/kathara
sudo apt update
sudo apt install -y kathara

# Gérer Docker en tant qu'utilisateur non-root
if ! getent group docker > /dev/null; then
    echo "Ajout du groupe Docker..."
    sudo groupadd docker
else
    echo "Le groupe Docker existe déjà."
fi

# Debug Docker si nécessaire
if ! command -v docker &> /dev/null; then
    echo "Installation de Docker..."
    sudo apt install -y docker.io
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
