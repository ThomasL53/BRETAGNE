from poe_api_wrapper import PoeApi
import BRETAGNE.monitoring
import BRETAGNE.utils.SDN_action
import time
import os
import re
import boto3
import json
from botocore.exceptions import ClientError
tokens = {
    'p-b': "",
    'p-lat': "",
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

def send_to_bedrock(csv_file):
    brt = boto3.client("bedrock-runtime")
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_string = file.read()

    prompt = f"I have a CSV file containing network data captured on our network. Could you analyze this network traffic and say whether or not an attack has taken place.  The answer should be as short as possible: yes or no with the attacker ip. : {csv_string}"
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    try:
        # Send the message to the model, using a basic inference configuration.
        response = brt.converse(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":5,"temperature":0},
            additionalModelRequestFields={"top_k":500}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke 'Claude'. Reason: {e}")
        exit(1)

def check_response(rep):
    regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    if 'yes' in rep.lower():
        ip = re.search(regex,rep)
        if ip:
            ip = ip.group() + "/32"
            BRETAGNE.utils.SDN_action.BlockTraffic(ip,"0.0.0.0/0")
            
def run(network):
    pcap_file = f"simu/shared/capture/ovs_{network.lower()}.pcap"
    csv_file = f"simu/shared/capture/ovs_{network.lower()}.csv"
    while 1:     
        clean_file(pcap_file,csv_file)
        BRETAGNE.monitoring.monitor(network.lower())
        time.sleep(15)
        pcap_to_csv(pcap_file,csv_file)
        time.sleep(1)
        respon = send_to_bedrock(csv_file)
        #check_response(respon)
        print(respon)