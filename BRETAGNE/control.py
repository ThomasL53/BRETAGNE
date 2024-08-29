from Kathara.manager.Kathara import Kathara

#Open a terminal on the specified node
def control(name):
    print(f"Opening a console on {name}")
    Kathara.get_instance().connect_tty(name, lab_name="simu")