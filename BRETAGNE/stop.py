from Kathara.manager.Kathara import Kathara
import shutil
import os
from yaspin import yaspin
from yaspin.spinners import Spinners

def stop():
    with yaspin(Spinners.dots, text="Stopping the simulation...") as spinner:
        if os.path.exists("simu"):
            shutil.rmtree("simu")
        try:
            Kathara.get_instance().wipe()
            spinner.text = ""
            spinner.ok("✔ Simulation stopped successfully!")
        except Exception as e:
            spinner.text = "✘ Simulation stop failed!"
            spinner.fail("✘ Simulation stop failed!")
            print(f"Error stopping the simulation: {e}")