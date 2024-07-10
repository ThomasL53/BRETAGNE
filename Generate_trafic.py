from Kathara.model.Lab import Lab
from Kathara.manager.Kathara import Kathara
import os
import random
import re 
import time

directory = "simu"

def get_machine_names(directory):
    machine_names = []
    for filename in os.listdir(directory):
        if filename.endswith(".startup"):
            machine_name = filename.split(".")[0]
            machine_names.append(machine_name)
    return machine_names


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


def generate_ping(nbping):
    for i in range(nbping):
        Kathara.get_instance().exec(machine_name=random.choice(machine_list),command=f'ping -c 4 {random.choice(ip_addresses)}',wait=True, lab_name="simu")

machine_list = get_machine_names(directory)
ip_addresses = get_ip_addresses(directory)
generate_ping(200)