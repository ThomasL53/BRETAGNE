import argparse
import os 
from Kathara.model.Lab import Lab
import BRETAGNE.blueAgent
import BRETAGNE.init
import BRETAGNE.stop
import BRETAGNE.control
import BRETAGNE.Generate_traffic
import BRETAGNE.monitoring
import BRETAGNE.utils.Sim_tools

def main(args):
    start = False
    if not os.path.exists("simu") and args.start:
        os.makedirs("simu")
    elif os.path.exists("simu"):
        start = True
    if args.start:
        lab = Lab("simu","simu")
        BRETAGNE.init.create_network(lab)
        if args.metasploit:
            for metasploit in args.metasploit:
                BRETAGNE.utils.Sim_tools.add_metasploit_on(metasploit,lab)
        BRETAGNE.init.start(lab)
    if start:
        if args.control:
            BRETAGNE.control.control(args.control)
        elif args.generate_traffic:
            BRETAGNE.Generate_traffic.start(args.generate_traffic)
        elif args.monitor:
            for monitor in args.monitor:
                BRETAGNE.monitoring.monitor(monitor.lower())
        elif args.BlueAgent:
            for network in args.BlueAgent:
                BRETAGNE.blueAgent.run(network.lower())
        elif args.stop:
            BRETAGNE.stop.stop()
    elif not args.start:
        print("Please start the simulation before use this command")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cage challenge 4 scenario simulation with kathara")
    parser.add_argument("--start",action="store_true", help="Simple simulation start-up")
    parser.add_argument("--stop",action="store_true", help="Stop simulation")
    parser.add_argument("--monitor",nargs="+", help="monitors the network and generates a pcap file with all traffic in simu/shared/capture")
    parser.add_argument("--metasploit",nargs="+", help="Deploy Metasploit instances on the networks specified in the command line")
    parser.add_argument("--control",type=str, help="Open a terminal on the specified node")
    parser.add_argument("--generate_traffic",type=int, help="Generate x random connection")
    parser.add_argument("--BlueAgent",nargs="+", help="Deploy BlueAgent on the networks specified in the command line")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
    else:
        main(args)