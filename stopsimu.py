from Kathara.manager.Kathara import Kathara
import shutil
import os

if os.path.exists("simu"):
    shutil.rmtree("simu")
Kathara.get_instance().wipe()