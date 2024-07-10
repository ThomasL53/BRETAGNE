# Cage_scenario_w_Kathara
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

# Start Scenario
`python3 simu.py`

# Watch traffic
`http://localhost:3000/`

# Stop Scenario
`python3 stopsimu.py`
