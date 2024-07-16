import argparse
import os 
from Kathara.model.Lab import Lab
import BRETAGNE.init
import BRETAGNE.stop
import BRETAGNE.control


def main(args):
    wireshark_count=0
    if args.start:
        if not os.path.exists("simu"):
            os.makedirs("simu")
        lab = Lab("simu","simu")
        BRETAGNE.init.create_network()
        if args.wireshark:
            for wireshark in args.wireshark:
                BRETAGNE.init.add_wireshark_on(wireshark, wireshark_count)
                wireshark_count=wireshark_count+1
        if args.metasploit:
            for metasploit in args.metasploit:
                BRETAGNE.init.add_metasploit_on(metasploit)
        BRETAGNE.init.start()
    elif args.control:
        BRETAGNE.control.control(args.control)
    elif args.stop:
        BRETAGNE.stop.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cage challenge 4 scenario simulation with kathara")
    parser.add_argument("--start",action="store_true", help="Simple simulation start-up")
    parser.add_argument("--stop",action="store_true", help="Stop simulation")
    parser.add_argument("--wireshark",nargs="+", help="Deploy Wireshark instances on the networks specified in the command line")
    parser.add_argument("--metasploit",nargs="+", help="Deploy Metasploit instances on the networks specified in the command line")
    parser.add_argument("--control",type=str, help="Open a terminal on the specified node")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
    else:
        main(args)