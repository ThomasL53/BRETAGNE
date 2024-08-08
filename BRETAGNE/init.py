from Kathara.manager.Kathara import Kathara
import os
import random
import ipaddress
from yaspin import yaspin
from yaspin.spinners import Spinners
import BRETAGNE.utils.Sim_tools



def create_subnet(name,lab,subnet_count,subnet_addr=None):
    eth=1
    name=name.lower()
    #choice of number of subnet hosts
    nb_PC=random.randint(3, 10)
    PC_list=[]
    #choice of number of subnet serveurs
    nb_SRV=random.randint(1, 6)
    SRV_list=[]
    #creation of an IPv4 object
    network = ipaddress.IPv4Network(subnet_addr)
    ips = []
    #Creation of the network address (by definition, the last address in the range)
    gateway=".".join(subnet_addr.rsplit(".", 1)[:-1] + ["254"])
    #copy packages to machines
    BRETAGNE.utils.Sim_tools.add_package()
    OvS=BRETAGNE.utils.Sim_tools.add_SDN_switch(name,subnet_count,lab)

    #creating and connecting PCs to the switch
    for pc in range(1,nb_PC+1):
        PC_name="pc_" + name + str(pc)
        PC = lab.new_machine(PC_name)
        lab.connect_machine_to_link(PC.name,(name+PC.name).upper())
        lab.connect_machine_to_link(OvS.name,(name+PC.name).upper())
        lab.update_file_from_list(
            [
                f"ovs-vsctl add-port s1 eth{eth}"
            ],
            f"ovs_{name}.startup"
        )
        eth=eth+1
        PC_list.append(PC)

    #creating and connecting SRVs to the switch
    for srv in range(1,nb_SRV+1):
        SRV_name="srv_" + name + str(srv)
        SRV = lab.new_machine(SRV_name)
        lab.connect_machine_to_link(SRV.name,(name+SRV.name).upper())
        lab.connect_machine_to_link(OvS.name,(name+SRV.name).upper())
        lab.update_file_from_list(
            [
                f"ovs-vsctl add-port s1 eth{eth}"
            ],
            f"ovs_{name}.startup"
        )
        eth=eth+1
        SRV_list.append(SRV)
        BRETAGNE.utils.Sim_tools.add_srv_service_on(SRV_name,lab)

    #Creating IPs for machines
    for i in range(1,nb_PC+nb_SRV+1):
        ip = str(network.network_address + i)
        ips.append(ip)

    machines= PC_list + SRV_list

    #Machine IP configuration
    for i, machine in enumerate(machines):
        lab.update_file_from_list(
            [
                f"/sbin/ifconfig eth0 {ips[i]}/24 up",
                f"route add default gw {gateway}",
                "apt install ./shared/packages/ftp.deb"
            ],
        f"{machine.name}.startup"
        )
        #Create a file with server IPs and configure SRV service
        if "srv" in machine.name:
            file_path="simu/srv_iplist"
            if os.path.exists(file_path):
                with open(file_path, "a") as file:
                    file.write( ips[i] + "\n")
            else:
                with open(file_path, "w") as file:
                    file.write( ips[i] + "\n")

def create_network(lab):
    subnet_count=1
    print("Creation of the scenario")
    # Configure and create fw_ra
    fw_ra=BRETAGNE.utils.Sim_tools.add_router_frr("fw_ra",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ra","eth0","1.1.1.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ra","eth1","1.1.0.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ra","eth2","10.10.10.1/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_ra)

    # Configure and create fw_oa
    fw_oa=BRETAGNE.utils.Sim_tools.add_router_frr("fw_oa",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ra","eth0","1.1.2.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ra","eth1","1.1.0.253/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_oa)

    # Configure and create fw_rb
    fw_rb=BRETAGNE.utils.Sim_tools.add_router_frr("fw_rb",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_rb","eth0","1.2.1.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_rb","eth1","1.2.0.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_rb","eth2","10.10.10.2/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_rb)

    # Configure and create fw_ob
    fw_ob=BRETAGNE.utils.Sim_tools.add_router_frr("fw_ob",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ob","eth0","1.2.2.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ob","eth1","1.2.0.253/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_ob)

    # Configure and create fw_cn
    fw_cn=BRETAGNE.utils.Sim_tools.add_router_frr("fw_cn",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_cn","eth0","192.168.1.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_cn","eth1","10.10.10.3/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_cn)

    # Configure and create fw_dmz
    fw_dmz=BRETAGNE.utils.Sim_tools.add_router_frr("fw_dmz",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_dmz","eth0","100.100.0.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_dmz","eth1","10.10.10.4/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_dmz)

    # Configure and create fw_AN

    fw_an=BRETAGNE.utils.Sim_tools.add_router_frr("fw_an",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_an","eth0","100.100.1.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_an","eth1","100.100.0.253/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_an)

    # Configure and create fw_OFN
    fw_ofn=BRETAGNE.utils.Sim_tools.add_router_frr("fw_ofn",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ofn","eth0","100.100.2.254/24",lab)
    BRETAGNE.utils.Sim_tools.add_ip_addr_on("fw_ofn","eth1","1000.1000.0.252/24",lab)
    BRETAGNE.utils.Sim_tools.configure_frr_on(fw_ofn)

    #deployed network A
    create_subnet("RA",lab,subnet_count,"1.1.1.0")
    subnet_count=subnet_count+1
    create_subnet("OA",lab,subnet_count,"1.1.2.0")
    subnet_count=subnet_count+1
    #deployed network B
    create_subnet("RB",lab,subnet_count,"1.2.1.0")
    subnet_count=subnet_count+1
    create_subnet("OB",lab,subnet_count,"1.2.2.0")
    subnet_count=subnet_count+1
    #Contractor network
    create_subnet("CN",lab,subnet_count,"192.168.1.0")
    subnet_count=subnet_count+1
    #HQ network and Public services
    create_subnet("DMZ",lab,subnet_count,"100.100.0.0")
    subnet_count=subnet_count+1
    create_subnet("AN",lab,subnet_count,"100.100.1.0")
    subnet_count=subnet_count+1
    create_subnet("OFN",lab,subnet_count,"100.100.2.0")
    subnet_count=subnet_count+1

    #connection of fw_ra
    lab.connect_machine_to_link(fw_ra.name, "RA")
    lab.connect_machine_to_link(fw_ra.name, "A")
    lab.connect_machine_to_link(fw_ra.name, "ON")

    #connection of fw_oa
    lab.connect_machine_to_link(fw_oa.name, "OA")
    lab.connect_machine_to_link(fw_oa.name, "A")

    #connection of fw_rb
    lab.connect_machine_to_link(fw_rb.name, "RB")
    lab.connect_machine_to_link(fw_rb.name, "B")
    lab.connect_machine_to_link(fw_rb.name, "ON")

    #connection of fw_ob
    lab.connect_machine_to_link(fw_ob.name, "OB")
    lab.connect_machine_to_link(fw_ob.name, "B")

    #connection of fw_cn
    lab.connect_machine_to_link(fw_cn.name, "CN")
    lab.connect_machine_to_link(fw_cn.name, "ON")

    #connection of fw_dnz
    lab.connect_machine_to_link(fw_dmz.name, "DMZ")
    lab.connect_machine_to_link(fw_dmz.name, "ON")

    #connection of fw_an
    lab.connect_machine_to_link(fw_an.name, "AN")
    lab.connect_machine_to_link(fw_an.name, "DMZ")

    #connection of fw_ofn
    lab.connect_machine_to_link(fw_ofn.name, "OFN")
    lab.connect_machine_to_link(fw_ofn.name, "DMZ")

    #alloy monitoring on the network
    BRETAGNE.utils.Sim_tools.add_SDN_comtroller(lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("RA",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("OA",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("RB",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("OB",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("CN",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("DMZ",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("AN",lab)
    BRETAGNE.utils.Sim_tools.add_monitoring("OFN",lab)

def start(lab):
    with open("simu/labhash", "w") as file:
        file.write(lab.hash)
    with yaspin(Spinners.dots, text="Starting the simulation...") as spinner:
        try:
            Kathara.get_instance().deploy_lab(lab)
            spinner.text = ""
            spinner.ok("✔ Simulation started successfully!")
        except Exception as e:
            spinner.text = "✘ Simulation start failed!"
            spinner.fail("✘ Simulation start failed!")
            print(f"Error starting the simulation: {e}")