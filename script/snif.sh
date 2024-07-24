#!/bin/bash

# Nom du fichier PCAP de sortie
OUTPUT_FILE=/shared/capture/$(hostname).pcap

# Démarrer la capture avec tcpdump et enregistrer dans le fichier PCAP
tcpdump -U -i any not net 20.0.1.0/24 and not \(ether proto 0x010b or ether proto 0x88cc\) -w $OUTPUT_FILE
