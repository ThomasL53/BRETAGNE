from Kathara.model.Lab import Lab
from Kathara.manager.Kathara import Kathara
import os
import random
import ipaddress

if not os.path.exists("simu"):
    os.makedirs("simu")
lab = Lab("simu","simu")
def create_subnet(name,subnet_addr=None):
    name=name.lower()
    nb_PC=random.randint(3, 10)
    PC_list=[]
    nb_SRV=random.randint(1, 6)
    SRV_list=[]
    network = ipaddress.IPv4Network(subnet_addr)
    ips = []
    gateway=".".join(subnet_addr.rsplit(".", 1)[:-1] + ["254"])
    for pc in range(1,nb_PC+1):
        PC_name="pc_" + name + str(pc)
        PC = lab.new_machine(PC_name)
        PC_list.append(PC)
    
    for srv in range(1,nb_SRV+1):
        SRV_name="srv_" + name + str(srv)
        SRV = lab.new_machine(SRV_name)
        SRV_list.append(SRV)
    
    for i in range(1,nb_PC+nb_SRV+1):
        ip = str(network.network_address + i)
        ips.append(ip)

    machines= PC_list + SRV_list

    for i, machine in enumerate(machines):
        lab.connect_machine_to_link(machine.name, name.upper())
        lab.create_file_from_list(
            [
                f"/sbin/ifconfig eth0 {ips[i]}/24 up",
                f"route add default gw {gateway}"
            ],
        f"{machine.name}.startup"
        )

wireshark_on=lab.new_machine("wireshark_on", **{"image": "lscr.io/linuxserver/wireshark"})
lab.connect_machine_to_link(wireshark_on.name, "ON")
test=wireshark_on.add_meta("bridged","true")
test=wireshark_on.add_meta("port","3000:3000/tcp")
# Configure and create fw_ra
fw_ra=lab.new_machine("fw_ra", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 1.1.1.254/24 up",
        "/sbin/ifconfig eth1 1.1.0.254/24 up",
        "/sbin/ifconfig eth2 10.10.10.1/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_ra.startup"
)
# Configure frr on fw_ra
fw_ra.create_file_from_path(os.path.join("config", "fw_ra.conf"), "/etc/frr/frr.conf")
fw_ra.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_ra.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_ra.update_file_from_string(content="hostname fw_ra\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_oa
fw_oa=lab.new_machine("fw_oa", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 1.1.2.254/24 up",
        "/sbin/ifconfig eth1 1.1.0.253/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_oa.startup"
)
# Configure frr on fw_oa
fw_oa.create_file_from_path(os.path.join("config", "fw_oa.conf"), "/etc/frr/frr.conf")
fw_oa.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_oa.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_oa.update_file_from_string(content="hostname fw_oa\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_rb
fw_rb=lab.new_machine("fw_rb", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 1.2.1.254/24 up",
        "/sbin/ifconfig eth1 1.2.0.254/24 up",
        "/sbin/ifconfig eth2 10.10.10.2/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_rb.startup"
)
# Configure frr on fw_rb
fw_rb.create_file_from_path(os.path.join("config", "fw_rb.conf"), "/etc/frr/frr.conf")
fw_rb.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_rb.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_rb.update_file_from_string(content="hostname fw_rb\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_ob
fw_ob=lab.new_machine("fw_ob", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 1.2.2.254/24 up",
        "/sbin/ifconfig eth1 1.2.0.253/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_ob.startup"
)
# Configure frr on fw_ob
fw_ob.create_file_from_path(os.path.join("config", "fw_ob.conf"), "/etc/frr/frr.conf")
fw_ob.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_ob.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_ob.update_file_from_string(content="hostname fw_ob\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_cn
fw_cn=lab.new_machine("fw_cn", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 192.168.1.254/24 up",
        "/sbin/ifconfig eth1 10.10.10.3/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_cn.startup"
)
# Configure frr on fw_cn
fw_cn.create_file_from_path(os.path.join("config", "fw_cn.conf"), "/etc/frr/frr.conf")
fw_cn.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_cn.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_cn.update_file_from_string(content="hostname fw_cn\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_dmz
fw_dmz=lab.new_machine("fw_dmz", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 100.100.0.254/24 up",
        "/sbin/ifconfig eth1 10.10.10.4/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_dmz.startup"
)
# Configure frr on fw_dmz
fw_dmz.create_file_from_path(os.path.join("config", "fw_dmz.conf"), "/etc/frr/frr.conf")
fw_dmz.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_dmz.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_dmz.update_file_from_string(content="hostname fw_dmz\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_AN
fw_an=lab.new_machine("fw_an", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 100.100.1.254/24 up",
        "/sbin/ifconfig eth1 100.100.0.253/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_an.startup"
)
# Configure frr on fw_AN
fw_an.create_file_from_path(os.path.join("config", "fw_an.conf"), "/etc/frr/frr.conf")
fw_an.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_an.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_an.update_file_from_string(content="hostname fw_an\n", dst_path="/etc/frr/vtysh.conf")
# Configure and create fw_OFN
fw_ofn=lab.new_machine("fw_ofn", **{"image": "kathara/frr"})
lab.create_file_from_list(
    [
        "/sbin/ifconfig eth0 100.100.2.254/24 up",
        "/sbin/ifconfig eth1 100.100.0.252/24 up",
        "/etc/init.d/frr start"
    ],
    "fw_ofn.startup"
)
# Configure frr on fw_ofn
fw_ofn.create_file_from_path(os.path.join("config", "fw_ofn.conf"), "/etc/frr/frr.conf")
fw_ofn.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
fw_ofn.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
fw_ofn.update_file_from_string(content="hostname fw_ofn\n", dst_path="/etc/frr/vtysh.conf")


#deployed network A
create_subnet("RA","1.1.1.0")
create_subnet("OA","1.1.2.0")
#deployed network B
create_subnet("RB","1.2.1.0")
create_subnet("OB","1.2.2.0")
#Contractor network
create_subnet("CN","192.168.1.0")
#HQ network and Public services
create_subnet("DMZ","100.100.0.0")
create_subnet("AN","100.100.1.0")
create_subnet("OFN","100.100.2.0")

lab.connect_machine_to_link(fw_ra.name, "RA")
lab.connect_machine_to_link(fw_ra.name, "A")
lab.connect_machine_to_link(fw_ra.name, "ON")

lab.connect_machine_to_link(fw_oa.name, "OA")
lab.connect_machine_to_link(fw_oa.name, "A")

lab.connect_machine_to_link(fw_rb.name, "RB")
lab.connect_machine_to_link(fw_rb.name, "B")
lab.connect_machine_to_link(fw_rb.name, "ON")

lab.connect_machine_to_link(fw_ob.name, "OB")
lab.connect_machine_to_link(fw_ob.name, "B")

lab.connect_machine_to_link(fw_cn.name, "CN")
lab.connect_machine_to_link(fw_cn.name, "ON")

lab.connect_machine_to_link(fw_dmz.name, "DMZ")
lab.connect_machine_to_link(fw_dmz.name, "ON")

lab.connect_machine_to_link(fw_an.name, "AN")
lab.connect_machine_to_link(fw_an.name, "DMZ")

lab.connect_machine_to_link(fw_ofn.name, "OFN")
lab.connect_machine_to_link(fw_ofn.name, "DMZ")

Kathara.get_instance().deploy_lab(lab)