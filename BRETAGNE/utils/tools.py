import os

#convert PCAP to CSV by using tshark
def pcap_to_csv(pcap_file,csv_file):
    os.system('tshark -r ' + pcap_file + ' >' + csv_file)

#delete the specified CSV and PCAP file
def clean_file(pcap_file,csv_file):
    if os.path.isfile(pcap_file):
        os.remove(pcap_file)
    if os.path.isfile(csv_file):
        os.remove(csv_file)