#from poe_api_wrapper import PoeApi
import BRETAGNE.monitoring
import BRETAGNE.utils.SDN_action
import time
import re
import boto3
from botocore.exceptions import ClientError
tokens = {
}
'''
#This fonction send network trafic via a CSV file to BRETAGNE-BOT on POE 
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
'''

#This fonction send network trafic to BEDROCK directly on the prompt (for LLM whose doesn't support file)
def send_to_bedrock_prompt(csv_file, model):
    brt = boto3.client("bedrock-runtime", region_name="us-west-2")
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_string = file.read()

    prompt = f"This is network data captured on our network. Could you analyze this network traffic and say whether or not an attack has taken place.  The answer should be as short as possible:only yes or no with the attacker ip. : {csv_string}"
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]
    if model == "sonnet":
        modelId="anthropic.claude-3-5-sonnet-20240620-v1:0"
    elif model == "llama":
        modelId="meta.llama3-1-405b-instruct-v1:0"
    try:
        # Send the message to the model, using a basic inference configuration.
        response = brt.converse(
            modelId=modelId,
            messages=conversation,
            inferenceConfig={"maxTokens":40,"temperature":0.7,"topP":0.7},
            additionalModelRequestFields={}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke {modelId}. Reason: {e}")
        exit(1)

#This fonction send network trafic via a CSV file to BEDROCK
def send_to_bedrock(csv_file, model):
    if model == "mistral":
        modelId="mistral.mistral-large-2407-v1:0"
    elif model == "llama":
       respon=send_to_bedrock_prompt(csv_file,model)
       return respon
    elif model == "sonnet":
        respon=send_to_bedrock_prompt(csv_file,model)
        return respon
    brt = boto3.client("bedrock-runtime", region_name="us-west-2")
    with open(csv_file, 'rb') as file:
        csv_file = file.read()

    prompt = f"I have a CSV file containing network data captured on our network. Could you analyze this network traffic and say whether or not an attack has taken place.  The answer should be as short as possible: only yes or no with the attacker ip"
    conversation = [
        {
            "role": "user",
            "content": [
                {
                    "document": {
                        "name": "traffic",
                        "format": "csv",
                        "source": {
                            "bytes": csv_file
                        }
                    }
                },
                {
                    "text": prompt
                }
            ]
        }
    ]
    try:
        # Send the message to the model, using a basic inference configuration.
        response = brt.converse(
            modelId=modelId,
            messages=conversation,
            inferenceConfig={"maxTokens":40,"temperature":0.7,"topP":0.7},
            additionalModelRequestFields={}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke {modelId}. Reason: {e}")
        exit(1)

#This fonction check the response of the LLM in order to block the traffic
def check_response(rep):
    regex = r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
    if 'yes' in rep.lower():
        ip = re.search(regex,rep)
        if ip:
            ip = ip.group() + "/32"
            BRETAGNE.utils.SDN_action.BlockTraffic(ip,"0.0.0.0/0")

#Deploy a autonomous Blue Agent on the specified network
def run(network):
    pcap_file = f"simu/shared/capture/ovs_{network.lower()}.pcap"
    csv_file = f"simu/shared/capture/ovs_{network.lower()}.csv"
    while 1:     
        BRETAGNE.utils.tools.clean_file(pcap_file,csv_file)
        BRETAGNE.monitoring.monitor(network.lower())
        time.sleep(15)
        BRETAGNE.utils.tools.pcap_to_csv(pcap_file,csv_file)
        time.sleep(1)
        respon = send_to_bedrock(csv_file, "sonnet")
        check_response(respon)
        print(respon)
