from Kathara.manager.Kathara import Kathara
import os
import random
import re 
import time

directory = "simu"
ip_srvlist = []

#This function returning a list with the names of all the machines in the simulation
def get_machine_names(directory):
    machine_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".startup"):
            machine_name = filename.split(".")[0]
            machine_names.append(machine_name)
    return machine_names

#This function returns a list of all allocated IP addresses for this simulation
def get_ip_addresses(directory):
    ip_addresses = []
    for filename in os.listdir(directory):
        if filename.endswith(".startup"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                content = file.read()
                ip_match = re.search(r"/sbin/ifconfig eth\d (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d{1,2} up", content)
                if ip_match:
                    ip_address = ip_match.group(1)
                    ip_addresses.append(ip_address)
    return ip_addresses

#This function returns a list of all IPs assigned to servers (with at least one service accessible)
def get_srv_ip():
    file="simu/srv_iplist"
    with open(file, 'r') as file:
        for line in file:
            ip = line.strip()
            if ip:
                ip_srvlist.append(ip)
    return ip_srvlist

def generate_ping(nbping):
    for i in range(nbping):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'ping -c 4 {random.choice(ip_addresses)}',wait=True, lab_name="simu")
        time.sleep(0.05)

def generate_www(nbconnexion):
    for i in range(nbconnexion):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'wget {random.choice(ip_srvlist)}',wait=True, lab_name="simu")
        time.sleep(0.05)

def generate_ftp(nbconnexion):
    for i in range(nbconnexion):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'ftp {random.choice(ip_srvlist)}',wait=True, lab_name="simu")
        time.sleep(0.05)

def generate_ssh(nbconnexion):
    for i in range(nbconnexion):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'ssh {random.choice(ip_srvlist)}',wait=True, lab_name="simu")
        time.sleep(0.05)

def generate_dns(nbconnexion):
    for i in range(nbconnexion):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'dig @{random.choice(ip_srvlist)} yannandthomas4ever.com',wait=True, lab_name="simu")
        time.sleep(0.05)

def generate_dhcp(nbconnexion):
    for i in range(nbconnexion):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'dhcp-lease-querry -s {random.choice(ip_srvlist)} ',wait=True, lab_name="simu")
        time.sleep(0.05)


def start(nb_iterations=20):
    actions= [generate_dhcp,generate_dns,generate_ping,generate_ssh,generate_www]
    global machine_list
    global ip_addresses
    global ip_srvlist

    machine_list = get_machine_names(directory)
    ip_addresses = get_ip_addresses(directory)
    ip_srvlist = get_srv_ip()
    for _ in range(nb_iterations):
        random_action = random.choice(actions)
        random_nb_connexion = random.randint(1, 20)

        random_action(random_nb_connexion)

        #random sleep 1s to 5s
        temps_attente = random.uniform(1, 5)
        time.sleep(temps_attente)