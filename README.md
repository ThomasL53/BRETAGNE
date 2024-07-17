# BRETAGNE ( Best Resilient Emulator for Training AI and Generate Network Environement ) 
Scenario simulation used for cage challenge 4 with Kathara


![Topology created with Kathara](topology.png)

# Install kathara
`sudo add-apt-repository ppa:katharaframework/kathara`

`sudo apt update`
## Manage Docker as a non-root user
`sudo add-apt-repository ppa:katharaframework/kathara`

`sudo groupadd docker`

`sudo usermod -aG docker $USER`

`newgrp docker`

## check install:
`kathara check`

# Install Python API
`python3 -m pip install git+https://github.com/saghul/pyuv@master#egg=pyuv`

`python3 -m pip install "kathara"`

# Download and install BRETAGNE
`git clone https://github.com/ThomasL53/BRETAGNE.git`

go to BRETAGNE directory
`cd BRETAGNE`

Source or add to bashrc the env.sh file
`source env.sh`

For more help
`bretagne -h`


