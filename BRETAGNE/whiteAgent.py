from Kathara.manager.docker.DockerMachine import DockerMachine
import docker
import time
import os
import BRETAGNE.Generate_traffic
import BRETAGNE.monitoring
import BRETAGNE.utils.tools
import random
import re
import csv
import BRETAGNE.blueAgent
import BRETAGNE.utils.Sim_tools
import script.CountScore
import signal
from functools import partial

directory = "simu"
ip_srvlist = []

def signal_handler(sig, frame, LLM, data_file):
    print(f"results for {LLM}:")
    script.CountScore.count(data_file)
    exit(0)

#Exec a command on the specified node without Katahra
def exec_command(hostname,command, timeout=0):

    with open("simu/labhash", 'r') as file:
        labhash = file.read()

    container_id = DockerMachine.get_container_name(hostname,labhash)
    client = docker.from_env()
    container = client.containers.get(container_id)
    if timeout == 0:
        container.exec_run(command)
    else:
        container.exec_run(command,detach=True)
        time.sleep(timeout)

#Launch a ports scam from the specified host to the specified host by using Metasploit framework
def portscan(attackerIP,defenderIP,network):
    subnetIP=BRETAGNE.utils.Sim_tools.get_ip_network(network.lower())
    gateway=".".join(subnetIP.rsplit(".", 1)[:-1] + ["254"])
    command= f"./msfconsole -x \"use auxiliary/scanner/portscan/tcp; set RHOST {defenderIP}; set PORTS 1-512; run; exit\""
    exec_command(f"metasploit_{network.lower()}",f"ip addr add {attackerIP}/24 dev eth0")
    exec_command(f"metasploit_{network.lower()}",f"ip route add default via {gateway} dev eth0")
    exec_command(f"metasploit_{network.lower()}",command)
    exec_command(f"metasploit_{network.lower()}",f"ip addr del {attackerIP}/24 dev eth0")
    return "portscan"

#Launch a slowloris attack from the specified host to the specified host by using Metasploit framework
def webddos(attackerIP,defenderIP,network):
    subnetIP=BRETAGNE.utils.Sim_tools.get_ip_network(network.lower())
    gateway=".".join(subnetIP.rsplit(".", 1)[:-1] + ["254"])
    command= f"./msfconsole -x \"use auxiliary/dos/http/slowloris; set RHOST {defenderIP}; set delay 5; set sockets 10; run; exit\""
    exec_command(f"metasploit_{network.lower()}",f"ip addr add {attackerIP}/24 dev eth0")
    exec_command(f"metasploit_{network.lower()}",f"ip route add default via {gateway} dev eth0")
    exec_command(f"metasploit_{network.lower()}",command, 20)
    exec_command(f"metasploit_{network.lower()}",f"pkill -f \"msfconsole -x\" ")
    exec_command(f"metasploit_{network.lower()}",f"ip addr del {attackerIP}/24 dev eth0")
    return "web ddos"

#Launch a brute force  ssh attack from the specified host to the specified host by using Metasploit framework
def bruteforcessh(attackerIP,defenderIP,network):
    subnetIP=BRETAGNE.utils.Sim_tools.get_ip_network(network.lower())
    gateway=".".join(subnetIP.rsplit(".", 1)[:-1] + ["254"])
    command= f"./msfconsole -x \"use auxiliary/scanner/ssh/ssh_login; set RHOST {defenderIP}; set USERNAME root; set PASS_FILE /shared/script/password; set THREADS 4; run; exit\""
    exec_command(f"metasploit_{network.lower()}",f"ip addr add {attackerIP}/24 dev eth0")
    exec_command(f"metasploit_{network.lower()}",f"ip route add default via {gateway} dev eth0")
    exec_command(f"metasploit_{network.lower()}",command)
    exec_command(f"metasploit_{network.lower()}",f"ip addr del {attackerIP}/24 dev eth0")
    return "brute force ssh"

#This function returns a list of all IPs assigned to servers (with at least one service accessible)
def get_srv_ip():
    file="simu/srv_iplist"
    with open(file, 'r') as file:
        for line in file:
            ip = line.strip()
            if ip:
                ip_srvlist.append(ip)
    return ip_srvlist

#This function lanch a random attack from a random host to a random host and return the attacker IP, the victim IP amd the attack type
def random_attack(network):
    actions= [portscan,webddos,bruteforcessh]
    global ip_srvlist
    ip_srvlist = get_srv_ip()
    random_action = random.choice(actions)
    defenderIP=random.choice(ip_srvlist)
    subnetIP=BRETAGNE.utils.Sim_tools.get_ip_network(network.lower())
    attackerIP=".".join(subnetIP.rsplit(".", 1)[:-1] + [str(random.randint(20,220))])
    attackname=random_action(attackerIP,defenderIP,network)
    return attackerIP,defenderIP, attackname

#This function generate a CSV file with: the network traffic, the attacker IP, the victim IP amd the attack type
def generate_dataset(network):
    pcap_file = f"simu/shared/capture/ovs_{network.lower()}.pcap"
    csv_file = f"simu/shared/capture/ovs_{network.lower()}.csv"
    dataset_file= f"dataset_{network.lower()}.csv"
    print(f"Generation of a dataset {dataset_file}. \n ctrl + c to stop the generation")
    while 1:     
        BRETAGNE.utils.tools.clean_file(pcap_file,csv_file)
        BRETAGNE.monitoring.monitor(network)
        attack = random.randint(0,1)
        userTraffic = random.randint(0,1)
        if attack == 1:
            attackerIP,defenderIP,attackname=random_attack(network)
            print(attackerIP + " attack: " + defenderIP + " :" + attackname)
        else:
            attackerIP=0
            defenderIP=0
            attackname="no attack"
            print("no attack")
        if userTraffic == 1:
            BRETAGNE.Generate_traffic.start(3)
        time.sleep(5)
        BRETAGNE.utils.tools.pcap_to_csv(pcap_file,csv_file)
        time.sleep(1)
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_string = file.read()
        file_exists = os.path.isfile(dataset_file)

        with open(dataset_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Traffic", "Attack Flag", "Attacker IP", "Defender IP","Attack type"])
            writer.writerow([csv_string, attack, attackerIP, defenderIP, attackname])

#This function compute a score for evaluate different LLM
def evaluateLLM(LLM,network):
    if LLM not in ["mistral","llama","sonnet"]:
        print("LLM not supported! Please use mistral, llama or sonnet ")
        return 0
    else:
        data_file= f"{LLM}_evaluation_{network.lower()}.csv"
        handler = partial(signal_handler, LLM=LLM, data_file=data_file)
        signal.signal(signal.SIGINT, handler)
        print(f"generation of the evaluation matrix \'{data_file}\' \nctrl + c to stop the evaluation")
    i = 0
    score = 100
    regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    while 1:
        pcap_file = f"simu/shared/capture/ovs_{network.lower()}.pcap"
        csv_file = f"simu/shared/capture/ovs_{network.lower()}.csv"
        BRETAGNE.utils.tools.clean_file(pcap_file,csv_file)
        BRETAGNE.monitoring.monitor(network.lower())
        attack = random.randint(0,1)
        if attack == 1:
            attackerIP,defenderIP,attackname=random_attack(network)
            print(attackerIP + " attack: " + defenderIP + " :" + attackname)
        else:
            attackerIP="NA"
            defenderIP="NA"
            attackname="no attack"
            print("no attack")
            BRETAGNE.Generate_traffic.start(1)
            time.sleep(5)
        BRETAGNE.utils.tools.pcap_to_csv(pcap_file,csv_file)
        with open(csv_file, 'r') as file:
            content = file.read()
        if not content:
            with open(csv_file, 'w') as file:
                file.write("no traffic")
        time.sleep(1)
        #respon = str(BRETAGNE.blueAgent.send_to_poe(csv_file)).lower()
        respon = str(BRETAGNE.blueAgent.send_to_bedrock(csv_file,LLM)).lower()
        if attack == 0 and "no" in respon:
            score=score+5
            analyse="OK +5"
        elif attack == 1 and "no" in respon:
            score=score-1
            analyse="LLM missed an attack -1"
        elif attack == 0 and re.search(regex,respon):
            score=score-5
            analyse="False positive -5"
        elif attack == 1 and re.search(regex,respon) and not attackerIP in respon:
            score=score-3
            analyse="Bad IP attack -3"
        elif attack == 1 and attackerIP in respon:
            score=score+5
            analyse="OK +5"
        elif attack == 1 and "yes" and not re.search(regex,respon):
            score=score+1
            analyse="attack detected but no IP"
        elif attack == 1 and not "yes" and not re.search(regex,respon):
            score=score+1
            analyse="attack detected but no IP"
        elif attack == 0 and "yes" in respon:
            score=score-5
            analyse="False positive -5"
        i=i+1
        print(f"score: {score} in {i} iteractions")

        if not os.path.isfile(data_file):
            with open(data_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Attack Flag", "Attacker IP", "Attack type", "LLM response", "score", "analyse"])

        with open(data_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([attack, attackerIP, attackname, respon, score, analyse])