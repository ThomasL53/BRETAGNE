from Kathara.manager.Kathara import Kathara

#This function launches TCPDUMP on the specified network with the dedicated script
def monitor(network):
    Kathara.get_instance().exec(f"ovs_{network}"," chmod 777 /shared/script/snif.sh",lab_name="simu")
    Kathara.get_instance().exec(f"ovs_{network}","./shared/script/snif.sh",lab_name="simu")