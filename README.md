# BRETAGNE ( Building a Reproducible and Efficient Training AI Gym for Network Environments )
<p align="center">
	<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTswnKnRyT66EAWPeL_jRgceNbkJOuxkppM5QNCwwZGkNLgzmwArWHOjEgbbvw1-5dj954&usqp=CAU"/>  
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
Starting a simulation with metasploit on the Operator Network (ON) and on the network Restricted Zone A (RA):
```shell
bretagne --start --metasploit ON RA
```
Open a terminal on pc_ra1:
```shell
bretagne --control pc_ra1
```
Observe traffic on the Operator Network (ON):
```shell
bretagne --monitor ON
```
Generating user traffic on the network:
```shell
bretagne --generate_traffic 10
```
Deploy a blue agent on the Operator Network (ON):
```shell
bretagne --BlueAgent ON
```
Stop the simulation:
```shell
bretagne --stop
```

## Using the blue agent with POE (not recommended) 
The blue agent used by BRETAGNE can also be used with POE with a special bot based on the use of GPT-4o-mini.
To use this agent, you need to create an account on POE (free).Then you have to get your private keys.

### Install POE API

`pip3 install poe-api-wrapper`

`pip3 install ballyregan`

### Getting your token
Sign in at https://poe.com/

F12 for Devtools (Right-click + Inspect)
- Chromium: Devtools > Application > Cookies > poe.com
- Firefox: Devtools > Storage > Cookies
- Safari: Devtools > Storage > Cookies

Copy the values of `p-b` and `p-lat` cookies and paste on BRETAGNE/BlueAgent.py

