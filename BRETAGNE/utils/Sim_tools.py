import os
import shutil
import re
#function to count the number of switch ports
def count_port(switchname):
    nbport = 0
    with open(f"simu/{switchname}.startup", 'r') as file:
        for line in file:
            if 'ovs-vsctl add-port' in line:
                nbport = nbport +1
        return nbport

def get_ip_network(network):
    with open(f"simu/pc_{network.lower()}1.startup", "r") as file:
        content = file.read()
    ip_match = re.search(r"/sbin/ifconfig eth\d (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/\d{1,2} up", content)
    if ip_match:
        ip_address = ip_match.group(1)
        return ip_address

#function to setting up a monitoring port on a switch 
def add_monitoring(network,lab):
    nbport = count_port(f"ovs_{network.lower()}")
    lab.connect_machine_to_link(f"ovs_{network.lower()}","MNT")
    lab.update_file_from_list(
        [
         f"ovs-vsctl add-port s1 eth{nbport+1} -- --id=@p get port eth{nbport+1} -- --id=@m create mirror name=m0 select-all=true -- set bridge s1 mirrors=@m"
        ],
    f"ovs_{network.lower()}.startup"
    )
    os.makedirs(f"simu/shared/script", exist_ok=True)
    os.makedirs(f"simu/shared/capture", exist_ok=True)
    src_file = f"script/snif.sh"
    dst_file = f"simu/shared/script/snif.sh"
    shutil.copy(src_file, dst_file)

#Function for deploying metasploit on a network
def add_metasploit_on(network,lab):
    nbport = count_port(f"ovs_{network.lower()}")
    print(f"Add metasploit_{network.lower()} to network {network.upper()}")
    redagent=lab.new_machine(f"metasploit_{network.lower()}", **{"image": "metasploitframework/metasploit-framework"})
    lab.connect_machine_to_link(redagent.name, f"META{network}")
    lab.connect_machine_to_link(f"ovs_{network.lower()}",f"META{network}")
    lab.update_file_from_list(
        [
         f"ovs-vsctl add-port s1 eth{nbport+1}"
        ],
    f"ovs_{network.lower()}.startup"
    )
    os.makedirs(f"simu/shared/script", exist_ok=True)
    src_file = f"script/password"
    dst_file = f"simu/shared/script/password"
    shutil.copy(src_file, dst_file)

#Function for sharing packages with machines in the simu
def add_package():
    packages_dir="packages"
    os.makedirs(f"simu/shared/packages", exist_ok=True)
    for filename in os.listdir(packages_dir):
        src_path = os.path.join(packages_dir, filename)
        dst_path = os.path.join(f"simu/shared/packages", filename)
        shutil.copy(src_path, dst_path)

#Function for add a predefined service to a node 
def add_srv_service_on(SRV,lab):
    lab.create_file_from_list(
        [
            "/etc/init.d/apache2 start",
            "apt install ./shared/packages/vsftpd.deb",
            "/etc/init.d/vsftpd start",
            "/etc/init.d/ssh start",
            "/etc/init.d/named start",
            "/etc/init.d/bind start"
        ],
    f"{SRV}.startup"
    )

#Function for add SDN switch an the network
def add_SDN_switch(name,subnet_count,lab):
    OvS=lab.new_machine(f"ovs_{name}", **{"image":"thomasl53/bretagne_ovs:1.0"})
    lab.connect_machine_to_link(OvS.name,"SDN")
    lab.create_file_from_list(
        [
            f"ip addr add 20.0.1.{subnet_count}/24 dev eth0",
            "/usr/share/openvswitch/scripts/ovs-ctl --system-id=random start",
            "ovs-vsctl add-br s1",
            "ovs-vsctl set-controller s1 tcp:20.0.1.254:6653"
        ],
        f"ovs_{name}.startup"
    )
    return OvS

#Function for add SDN switch an the network
def add_SDN_comtroller(lab):
    controller=lab.new_machine("controller", **{"image": "thomasl53/bretagne_floodlight"})
    lab.connect_machine_to_link(controller.name,"SDN")
    lab.create_file_from_list(
        [
            "ip addr add 20.0.1.254/24 dev eth0"
        ],
        "controller.startup"
        )
    controller.add_meta("bridged","true")
    controller.add_meta("port",f"8080:8080/tcp")
    print("Add controller floodlight to network SDN. Manage SDN at http://localhost:8080/ui/pages/index.html")

#Function for add SDN switch an the network
def configure_frr_on(router):
    router.create_file_from_path(os.path.join("config", f"{router.name}.conf"), "/etc/frr/frr.conf")
    router.create_file_from_path(os.path.join("config", "daemons"), "/etc/frr/daemons")
    router.create_file_from_string(content="service integrated-vtysh-config\n", dst_path="/etc/frr/vtysh.conf")
    router.update_file_from_string(content=f"hostname {router.name}\n", dst_path="/etc/frr/vtysh.conf")

#Function for IP configuration
def add_ip_addr_on(machine,eth,ip,lab):
    if os.path.isfile(f"simu/{machine}.startup"):
        lab.update_file_from_list(
        [
            f"/sbin/ifconfig {eth} {ip} up",
        ],
        f"{machine}.startup"
        )
    else:
        lab.create_file_from_list(
        [
            f"/sbin/ifconfig {eth} {ip} up",
        ],
        f"{machine}.startup"
        )

#Function for add a fr routing router
def add_router_frr(name,lab):
    router=lab.new_machine(name.lower(), **{"image": "kathara/frr"})
    lab.create_file_from_list(
        [
            "/etc/init.d/frr start",
        ],
        f"{name}.startup"
    )
    return router
