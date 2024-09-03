# BRETAGNE
 
BRETAGNE ( Building a Reproducible and Efficient Training AI Gym for Network Environments ), is a network simulation environment designed to serve as a training ground for autonomous defense agents using hybrid AI models in simulations. The platform integrates docker, a lightweight virtualization technology orchestrated by Kathara with widely used network protocols such as BGP, OSPF, HTTP, SSH and others to simulate production-like environments. We present a multi-agent architecture involving blue, red, green, and white agents, designed to create dynamic, communicative environments for training purposes. Overall, the BRETAGNE framework offers a realistic and scalable solution for the training and deployment of autonomous agents in operational networks.

![Preview](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTswnKnRyT66EAWPeL_jRgceNbkJOuxkppM5QNCwwZGkNLgzmwArWHOjEgbbvw1-5dj954&usqp=CAU)


[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-31013/)

## Key Features

- **Realism**. Using docker to simulate an environment with real implementations.

- **Scalability**. Create your own network scenario quickly with built-in python functions.

- **Performant**. Using containerization to simulate large networks.

- **Autonomous traffic**. Green and red agent implementations for realistic, autonomous network traffic generation.
  
- **Interaction**. Each machine can be operated during simulation via its own terminal.

- **Automatic monitoring**. Automatic monitoring of attacks using LLM and decision-making using SDM.


## Installation
1.To install bretagne, start by downloading the install.sh script: https://github.com/ThomasL53/BRETAGNE/blob/main/install.sh

2.Move your file to your home directory and give it installation rights:
```shell
sudo chmod +x install.sh
```
3.Run the installation script (This may take some time depending on your internet connection)
```shell
./install.sh
```
4.Reboot your computer or close your terminal to finalize installation

5.Don't forget to install AWS CLI and configure your login with 'AWS configure' to use the blue agent.

## Example of use
Starting a simulation with metasploit on the Operator Network (ON) and on the network Restricted Zone A (RA):

`bretagne --start --metasploit ON RA`

Open a terminal on pc_ra1:

`bretagne --control pc_ra1`

Observe traffic on the Operator Network (ON):

`bretagne --monitor ON`

Generating user traffic on the network:

`bretagne --generate_traffic 10`

Deploy a blue agent on the Operator Network (ON):

`bretagne --BlueAgent ON`

Stop the simulation:

`bretagne --stop`

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

