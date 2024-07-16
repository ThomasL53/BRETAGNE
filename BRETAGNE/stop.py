from Kathara.manager.Kathara import Kathara
import shutil
import os

def stop():
    print("Stop simulation in progress")
    if os.path.exists("simu"):
        shutil.rmtree("simu")
    try:
        Kathara.get_instance().wipe()
    except Exception:
        pass

    print("done !")