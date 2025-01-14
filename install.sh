#!/bin/bash

# Installation script for BRETAGNE
LOG_FILE="/tmp/InstallBRETAGNE.log"
touch "$LOG_FILE"

#sudo acess verification
if ! sudo ls > /dev/null 2>&1; then
    echo "This user doesn't have access to the sudo group. Please add this user to the sudo group"
    exit
fi

#Distribution check
#!/bin/bash
OS=$(lsb_release -si)
VERSION=$(lsb_release -sr)

if [[ "$OS" == "Debian" ]]; then
    if [[ "$VERSION" == "11" || "$VERSION" == "12" ]]; then
        DIST=$VERSION
    else
        echo "This debian version is not supported"
    fi
elif [[ "$OS" == "Ubuntu" ]]; then
    DIST="ubuntu"
elif [[ "$OS" == "Kali" ]]; then
    DIST="kali"
else
    echo "Please use debian 11,12, ubuntu or kali"
fi

#Install docker
echo "Install Docker..." | tee -a "$LOG_FILE"
if [[ "$DIST" == "ubuntu" ]]; then
  for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove -yqq $pkg  >> "$LOG_FILE" 2>&1; done
  sudo apt-get update -yqq >> "$LOG_FILE" 2>&1
  # Add Docker's official GPG key:
  sudo apt-get install ca-certificates curl -yqq >> "$LOG_FILE" 2>&1
  sudo install -m 0755 -d /etc/apt/keyrings >> "$LOG_FILE" 2>&1
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc >> "$LOG_FILE" 2>&1
  sudo chmod a+r /etc/apt/keyrings/docker.asc >> "$LOG_FILE" 2>&1
  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null 
  sudo apt-get update -yqq >> "$LOG_FILE" 2>&1
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -yqq >> "$LOG_FILE" 2>&1

elif [[ "$DIST" == "11" || "$DIST" == "12" ]]; then
  for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove -yqq $pkg  >> "$LOG_FILE" 2>&1; done
  # Add Docker's official GPG key:
  sudo apt-get update -yqq >> "$LOG_FILE" 2>&1
   sudo apt-get install curl -yqq >> "$LOG_FILE" 2>&1
  sudo apt-get install ca-certificates curl -yqq >> "$LOG_FILE" 2>&1
  sudo install -m 0755 -d /etc/apt/keyrings >> "$LOG_FILE" 2>&1
  sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc >> "$LOG_FILE" 2>&1
  sudo chmod a+r /etc/apt/keyrings/docker.asc >> "$LOG_FILE" 2>&1
  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update -yqq >> "$LOG_FILE" 2>&1
  sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -yqq >> "$LOG_FILE" 2>&1

elif [[ "$DIST" == "kali" ]]; then
  for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove -yqq $pkg  >> "$LOG_FILE" 2>&1; done
  # Add Docker's official GPG key:
  sudo apt-get update -yqq >> "$LOG_FILE" 2>&1
  echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian bookworm stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list >> "$LOG_FILE" 2>&1
  curl -fsSL https://download.docker.com/linux/debian/gpg |
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg >> "$LOG_FILE" 2>&1
  sudo apt update -yqq >> "$LOG_FILE" 2>&1
  sudo apt install -yqq docker-ce docker-ce-cli containerd.io >> "$LOG_FILE" 2>&1
fi

# Install Kathara
if [[ "$DIST" == "ubuntu" ]]; then
  echo "Add Kathara depot..." | tee -a "$LOG_FILE"
  sudo apt-get install software-properties-common -yqq >> "$LOG_FILE" 2>&1
  sudo apt update -yqq >> "$LOG_FILE" 2>&1
  sudo add-apt-repository ppa:katharaframework/kathara -sy >> "$LOG_FILE" 2>&1

elif [[ "$DIST" == "11" ]]; then
  wget -qO - "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x21805a48e6cbba6b991abe76646193862b759810" | sudo gpg --dearmor -o /usr/share/keyrings/ppa-kathara-archive-keyring.gpg >> "$LOG_FILE" 2>&1
  echo "deb [ signed-by=/usr/share/keyrings/ppa-kathara-archive-keyring.gpg ] http://ppa.launchpad.net/katharaframework/kathara/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/kathara.list yqq >> "$LOG_FILE" 2>&1
  echo "deb-src [ signed-by=/usr/share/keyrings/ppa-kathara-archive-keyring.gpg ] http://ppa.launchpad.net/katharaframework/kathara/ubuntu focal main" | sudo tee -a /etc/apt/sources.list.d/kathara.list yqq >> "$LOG_FILE" 2>&1

elif [[ "$DIST" == "12" ]]; then
  wget -qO - "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x21805a48e6cbba6b991abe76646193862b759810" | sudo gpg --dearmor -o /usr/share/keyrings/ppa-kathara-archive-keyring.gpg >> "$LOG_FILE" 2>&1
  echo "deb [ signed-by=/usr/share/keyrings/ppa-kathara-archive-keyring.gpg ] http://ppa.launchpad.net/katharaframework/kathara/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/kathara.list >> "$LOG_FILE" 2>&1
  echo "deb-src [ signed-by=/usr/share/keyrings/ppa-kathara-archive-keyring.gpg ] http://ppa.launchpad.net/katharaframework/kathara/ubuntu jammy main" | sudo tee -a /etc/apt/sources.list.d/kathara.list >> "$LOG_FILE" 2>&1
elif [[ "$DIST" == "kali" ]]; then
  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 21805A48E6CBBA6B991ABE76646193862B759810
  echo "deb http://ppa.launchpad.net/katharaframework/kathara/ubuntu focal main" | sudo tee /etc/apt/sources.list.d/kathara.list >> "$LOG_FILE" 2>&1
  echo "deb-src http://ppa.launchpad.net/katharaframework/kathara/ubuntu focal main" | sudo tee -a /etc/apt/sources.list.d/kathara.list >> "$LOG_FILE" 2>&1
  wget http://ftp.it.debian.org/debian/pool/main/m/mpdecimal/libmpdec2_2.4.2-2_amd64.deb
  wget http://ftp.de.debian.org/debian/pool/main/libf/libffi/libffi6_3.2.1-9_amd64.deb
  wget http://ftp.de.debian.org/debian/pool/main/r/readline/libreadline7_7.0-5_amd64.deb
  sudo apt install ./libmpdec2_2.4.2-2_amd64.deb
  sudo apt install ./libffi6_3.2.1-9_amd64.deb
  sudo apt install ./libreadline7_7.0-5_amd64.deb
fi

sudo apt update -yqq >> "$LOG_FILE" 2>&1
echo "Install Kathara..." | tee -a "$LOG_FILE"
sudo apt install kathara -yqq >> "$LOG_FILE" 2>&1

echo "Kathara installation check..." | tee -a "$LOG_FILE"
kathara check >> "$LOG_FILE" 2>&1

# Install Python dependencies
if [[ "$DIST" == "11" ]]; then
  echo "Installation of pip and Python dependencies..." | tee -a "$LOG_FILE"
  sudo apt install python3-pip -yqq >> "$LOG_FILE" 2>&1
  pip3 install yaspin >> "$LOG_FILE" 2>&1
  python3 -m pip install "kathara" >> "$LOG_FILE" 2>&1
  python3 -m pip install boto3 >> "$LOG_FILE" 2>&1
else
  echo "Installation of pip and Python dependencies..." | tee -a "$LOG_FILE"
  sudo apt install python3-pip -yqq >> "$LOG_FILE" 2>&1
  pip3 install yaspin -q --break-system-packages >> "$LOG_FILE" 2>&1
  python3 -m pip install git+https://github.com/saghul/pyuv@master#egg=pyuv -q --break-system-packages >> "$LOG_FILE" 2>&1
  python3 -m pip install "kathara" -q --break-system-packages >> "$LOG_FILE" 2>&1
  python3 -m pip install boto3 -q --break-system-packages >> "$LOG_FILE" 2>&1
fi

#Download and install tshark
sudo apt install tshark -yqq >> "$LOG_FILE" 2>&1

# Download and install BRETAGNE
echo "Cloning the BRETAGNE depot..." | tee -a "$LOG_FILE"
git clone https://github.com/ThomasL53/BRETAGNE.git -q >> "$LOG_FILE" 2>&1

# Manage Docker as non root user
sudo usermod -aG docker ${USER} 

# Add env to bashrc
echo "alias bretagne=\"python3 $(pwd)/BRETAGNE/bretagne.py\"" >> ~/.bashrc
echo "Installation complete. RESTART YOUR COMPUTRE. For more help, use: bretagne -h" | tee -a "$LOG_FILE"
