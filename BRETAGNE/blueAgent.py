from poe_api_wrapper import PoeApi
from scapy.all import rdpcap
import BRETAGNE.monitoring
import BRETAGNE.utils
import time
import os
import re

tokens = {
    'p-b': "yixeeLWYGdQjXtHqOKGWYw%3D%3D",
    'p-lat': "TaTWh%2BB0ffzWoKmRe0gsub3b0UJJ0VeRtp6gRZ5pxQ%3D%3D",
}

def pcap_to_csv(pcap_file,csv_file):
    os.system('tshark -r ' + pcap_file + ' >' + csv_file)
def clean_file(pcap_file,csv_file):
    if os.path.isfile(pcap_file):
        os.remove(pcap_file)
    if os.path.isfile(csv_file):
        os.remove(csv_file)

def send_to_poe(csv_file):
    response = ""
    client = PoeApi(tokens=tokens)
    message = "Has there been a cyber attack ?"
    file_path = [csv_file]
    for chunk in client.send_message(bot="BRETAGNE-BOT", message=message, file_path=file_path):
        print(chunk["response"], end='', flush=True)
        response = response + chunk["response"]
    print("")
    return response

def check_response(rep):
    regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    if 'yes' in rep.lower():
        ip = re.search(regex,rep)
        if ip:
            ip = ip.group() + "/32"
            BRETAGNE.utils.BlockTraffic(ip,"0.0.0.0/0")
            
def run(network):
    pcap_file = f"simu/shared/capture/ovs_{network.lower()}.pcap"
    csv_file = f"simu/shared/capture/ovs_{network.lower()}.csv"
    while 1:     
        clean_file(pcap_file,csv_file)
        BRETAGNE.monitoring.monitor(network.lower())
        time.sleep(30)
        pcap_to_csv(pcap_file,csv_file)
        time.sleep(1)
        respon = send_to_poe(csv_file)
        check_response(respon)