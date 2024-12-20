# BRETAGNE ( Building a Reproducible and Efficient Training AI Gym for Network Environments )
<p align="center">
	<img src="img/logo.png"  width=200%/>  
</p>

[![BRETAGNE 1.0](https://img.shields.io/badge/BRETAGNE-1.0-white.svg)](https://github.com/ThomasL53/BRETAGNE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-31013/)
[![Kathara 3.7.6](https://img.shields.io/badge/Kathara-3.7.6-red.svg)](https://www.kathara.org/download.html)

## Introduction
 BRETAGNE, is a network simulation environment designed to serve as a training ground for autonomous defense agents using hybrid AI models in simulations. The platform integrates docker, a lightweight virtualization technology orchestrated by Kathara with widely used network protocols such as BGP, OSPF, HTTP, SSH and others to simulate production-like environments. We present a multi-agent architecture involving blue, red, green, and white agents, designed to create dynamic, communicative environments for training purposes. Overall, the BRETAGNE framework offers a realistic and scalable solution for the training and deployment of autonomous agents in operational networks.

## Key Features

- **Realism**. Using docker to simulate an environment with real implementations.

- **Scalability**. Create your own network scenario quickly with built-in python functions.

- **Performant**. Using containerization to simulate large networks.

- **Autonomous traffic**. Green and red agent implementations for realistic, autonomous network traffic generation.
  
- **Interaction**. Each machine can be operated during simulation via its own terminal.

- **Automatic monitoring**. Automatic monitoring of attacks using LLM and decision-making using SDM.


## Installation
Bretagne is available for:
[![Ubuntu 24.04](https://img.shields.io/badge/Ubuntu-24.04-orange.svg)](https://ubuntu.com/blog/tag/ubuntu-24-04-lts)
[![Debian 12](https://img.shields.io/badge/Debian-12-red.svg)](https://www.debian.org/releases/bookworm/)
[![Kali Linux](https://img.shields.io/badge/Kali-linux-blue.svg)](https://www.kali.org/)
[![Debian 11](https://img.shields.io/badge/Debian-11-red.svg)](https://www.debian.org/releases/bullseye/)

1. To install bretagne, start by downloading the install.sh script: https://github.com/ThomasL53/BRETAGNE/blob/main/install.sh

2. Move your file to your home directory and give it installation rights:
```shell
sudo chmod +x install.sh
```
3. Run the installation script (This may take some time depending on your internet connection). If an error occurs, refer to /tmp/InstallBretagne.log
```shell
./install.sh
```
4. Reboot your computer or close your terminal to finalize installation

5. Don't forget to install AWS CLI and configure your login with 'AWS configure' to use the blue agent.

6. Please note that the initial start-up of the simulation may take some time, depending on the images already present on your machine. 

## Example of use
Starting a simulation with metasploit on the network Restricted Zone A (RA):
```shell
bretagne --start --metasploit RA
```
Open a terminal on pc_ra1:
```shell
bretagne --control pc_ra1
```
Observe traffic on the Restricted Zone A (RA):
```shell
bretagne --monitor RA
```
Generating user traffic on the network:
```shell
bretagne --generate_traffic 10
```
Deploy a blue agent on the Restricted Zone A (RA):
```shell
bretagne --BlueAgent RA
```
Stop the simulation:
```shell
bretagne --stop
```
For more help:
```shell
bretagne -h
```
## Default topology
The default network is that used in Cage Challenge 4. The network consists of two theater networks, shown as ’A’ and ’B’ and a metropolitan network, shown as ’C’, interconnected
by a traditional carrier network (ON). In addition, a corporate network (CN) is connected to the same operator.The subnetworks used in the simulation are specified on the schematic switch.

<p align="center">
	<img src="img/Topology.png"  width=200%/>  
</p>

- **The routers**. Utilize FRR 9.0.1 and it's name fw_'NETWORK name' (exemple: for the RA network the router is fw_ra)
- **The switches**. Employ Open vSwitch 3.0.1 and it's name ovs_'NETWORK name' (exemple: for the OFN network the switch is ovs_ofn). They are all connected to the SDN controller via a common control plane.
- **The hosts**. Are randomly generated between 3 and 10 on each subnetwork. The are are based on a Linux kernel 6.8.0-39 and it's name pc'x'_'NETWORK name' (exemple: for the DMZ network the host 1 is pc1_dmz)
- **The server**. Are randomly generated between 1 and 6 on each subnetwork. The are are based on a Linux kernel 6.8.0-39 and it's name srv'x'_'NETWORK name' (exemple: for the RB network the server 3 is srv3_dmz)
- **The SDN controler**. Is based on Floodlight 1.2. It is accessible via the URL:http://localhost:8080/ui/pages/index.html. It's name 'controller'

## Using the blue agent with POE (not recommended) 
The blue agent used by BRETAGNE can also be used with POE with a special bot based on the use of GPT-4o-mini.
To use this agent, you need to create an account on POE (free).Then you have to get your private keys.

### Install POE API
```shell
pip3 install poe-api-wrapper
pip3 install ballyregan
```

### Getting your token
Sign in at https://poe.com/

F12 for Devtools (Right-click + Inspect)
- Chromium: Devtools > Application > Cookies > poe.com
- Firefox: Devtools > Storage > Cookies
- Safari: Devtools > Storage > Cookies

Copy the values of `p-b` and `p-lat` cookies and paste on BRETAGNE/BlueAgent.py

