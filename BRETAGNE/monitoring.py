from Kathara.manager.Kathara import Kathara

def monitor(network):
    Kathara.get_instance().exec(f"ovs_{network}"," chmod 777 /shared/script/snif.sh",lab_name="simu")
    Kathara.get_instance().exec(f"ovs_{network}","./shared/script/snif.sh",lab_name="simu")