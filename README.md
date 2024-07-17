# BRETAGNE ( Best Resilient Emulator for Training AI and Generate Network Environement ) 
Scenario simulation used for cage challenge 4 with Kathara


![Topology created with Kathara](topology.png)

# Install kathara
`sudo add-apt-repository ppa:katharaframework/kathara`

`sudo apt update`

`sudo apt install kathara`

## Manage Docker as a non-root user
`sudo add-apt-repository ppa:katharaframework/kathara`

`sudo groupadd docker`

`sudo usermod -aG docker $USER`

`newgrp docker`

### Debug Docker
If docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory')) occurs.

`apt install docker.io`

In ~/.docker/config.json change credsStore to credStore.

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

# Example of use
Starting a simulation with wireshark on the Operator Network (ON) and DMZ:

`bretagne --start --wireshark ON DMZ`

Starting a simulation with wireshark and metasploit on the Operator Network (ON):

`bretagne --start --wireshark ON --metasploit ON`

Open a terminal on pc_ra1:

`bretagne --control pc_ra1`

Generating user traffic on the network:

`bretagne --generate_traffic 10`

Stop the simulation:
`bretagne --stop`





