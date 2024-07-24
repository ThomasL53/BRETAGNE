from Kathara.manager.Kathara import Kathara

Kathara.get_instance().exec("ovs_ra"," chmod 777 /shared/script/snif.sh",lab_name="simu")
Kathara.get_instance().exec("ovs_ra","./shared/script/snif.sh",lab_name="simu")