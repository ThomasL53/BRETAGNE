from Kathara.manager.docker.DockerMachine import DockerMachine
import docker
import time
import os
import BRETAGNE.Generate_traffic
import BRETAGNE.monitoring
import random
import re
import csv
import subprocess

directory = "simu"
ip_srvlist = []

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

def pcap_to_csv(pcap_file,csv_file):
    os.system('tshark -r ' + pcap_file + ' >' + csv_file)
def clean_file(pcap_file,csv_file):
    if os.path.isfile(pcap_file):
        os.remove(pcap_file)
    if os.path.isfile(csv_file):
        os.remove(csv_file)

def portscan(attackerIP,defenderIP,network):
    command= f"./msfconsole -x \"use auxiliary/scanner/portscan/tcp; set RHOST {defenderIP}; set RPORTS 1-1024; run; exit\""
    exec_command(f"metasploit_{network.lower()}",f"ip addr add {attackerIP}/24 dev eth0")
    exec_command(f"metasploit_{network.lower()}",command)
    exec_command(f"metasploit_{network.lower()}",f"ip addr del {attackerIP}/24 dev eth0")
    return "portscan"

def webddos(attackerIP,defenderIP,network):
    command= f"./msfconsole -x \"use auxiliary/dos/http/slowloris; set RHOST {defenderIP}; set delay 5; set sockets 10; run; exit\""
    exec_command(f"metasploit_{network.lower()}",f"ip addr add {attackerIP}/24 dev eth0")
    exec_command(f"metasploit_{network.lower()}",command, 20)
    exec_command(f"metasploit_{network.lower()}",f"pkill -f \"msfconsole -x\" ")
    exec_command(f"metasploit_{network.lower()}",f"ip addr del {attackerIP}/24 dev eth0")
    return "web ddos"

def bruteforcessh(attackerIP,defenderIP,network):
    command= f"./msfconsole -x \"use auxiliary/scanner/ssh/ssh_login; set RHOST {defenderIP}; set USERNAME root; set PASS_FILE /shared/script/password; set THREADS 4; run; exit\""
    exec_command(f"metasploit_{network.lower()}",f"ip addr add {attackerIP}/24 dev eth0")
    exec_command(f"metasploit_{network.lower()}",command)
    exec_command(f"metasploit_{network.lower()}",f"ip addr del {attackerIP}/24 dev eth0")
    return "brute force ssh"

def get_ip_network(network):
    with open(f"simu/pc_{network.lower()}1.startup", "r") as file:
        content = file.read()
    ip_match = re.search(r"/sbin/ifconfig eth\d (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d{1,2} up", content)
    if ip_match:
        ip_address = ip_match.group(1)
        return ip_address

def get_srv_ip():
    file="simu/srv_iplist"
    with open(file, 'r') as file:
        for line in file:
            ip = line.strip()
            if ip:
                ip_srvlist.append(ip)
    return ip_srvlist

def random_attack(network):
    actions= [portscan,webddos,bruteforcessh]
    global ip_srvlist
    ip_srvlist = get_srv_ip()
    random_action = random.choice(actions)
    defenderIP=random.choice(ip_srvlist)
    subnetIP=get_ip_network(network.lower())
    attackerIP=".".join(subnetIP.rsplit(".", 1)[:-1] + [str(random.randint(20,220))])
    attackname=random_action(attackerIP,defenderIP,network)
    return attackerIP,defenderIP, attackname

def generate_dataset(network):
    pcap_file = f"simu/shared/capture/ovs_{network.lower()}.pcap"
    csv_file = f"simu/shared/capture/ovs_{network.lower()}.csv"
    dataset_file= "dataset.csv"
    while 1:     
        clean_file(pcap_file,csv_file)
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
        time.sleep(15)
        pcap_to_csv(pcap_file,csv_file)
        time.sleep(1)
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_string = file.read()
        file_exists = os.path.isfile(dataset_file)

        with open(dataset_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Écrire l'en-tête si le fichier vient d'être créé
            if not file_exists:
                writer.writerow(["Traffic", "Attack Flag", "Attacker IP", "Defender IP","Attack type"])
            
            # Ajouter une nouvelle ligne avec les données
            writer.writerow([csv_string, attack, attackerIP, defenderIP, attackname])

generate_dataset("ra")