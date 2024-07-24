import requests
import json
from Kathara.manager.docker.DockerMachine import DockerMachine
import docker


def BlockTraffic(src_ip, dst_ip):
    url = f"http://localhost:8080/wm/acl/rules/json"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url)
        response.raise_for_status()
        acls = response.json()
        for acl in acls:
            if acl["nw_src"] == src_ip and acl["nw_dst"] == dst_ip and acl["action"] == "ALLOW":
                # Supprimer l'ACL
                acl_id = acl["id"]
                data = {"ruleid": acl_id}
                delete_response = requests.delete(url, data=json.dumps(data), headers=headers)
                delete_response.raise_for_status()
        data = {
            "src-ip": src_ip,
            "dst-ip": dst_ip,
            "action": "deny"
        }
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Une erreur s'est produite lors de l'envoi de la requête :", e)
        
    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la récupération des ACLs :", e)

def AllowTraffic(src_ip, dst_ip):
    url = f"http://localhost:8080/wm/acl/rules/json"
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.get(url)
        response.raise_for_status()
        acls = response.json()
        for acl in acls:
            if acl["nw_src"] == src_ip and acl["nw_dst"] == dst_ip and acl["action"] == "DENY":
                # Supprimer l'ACL
                acl_id = acl["id"]
                data = {"ruleid": acl_id}
                delete_response = requests.delete(url, data=json.dumps(data), headers=headers)
                delete_response.raise_for_status()
                return
        data = {
            "src-ip": src_ip,
            "dst-ip": dst_ip,
            "action": "allow"
        }
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Une erreur s'est produite lors de l'envoi de la requête :", e)
        
    except requests.exceptions.RequestException as e:
        print("Une erreur s'est produite lors de la récupération des ACLs :", e)

def Restore(hostname):

    with open("simu/labhash", 'r') as file:
        labhash = file.read()

    container_id = DockerMachine.get_container_name(hostname,labhash)
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.restart()

    with open(f"simu/{hostname}.startup", 'r') as file:
        commands = file.readlines()
        commands = [cmd.strip() for cmd in commands if cmd.strip()]
        for command in commands:
            container.exec_run(command)

src_ip = "1.1.1.0/24"
dst_ip = "100.100.0.0/24"

BlockTraffic(src_ip, dst_ip)
AllowTraffic(src_ip, dst_ip)
Restore("pc_ra1")