import argparse
import os 
from Kathara.model.Lab import Lab
import BRETAGNE.init
import BRETAGNE.stop
import BRETAGNE.control
import BRETAGNE.Generate_traffic

def main(args):
    wireshark_count=0
    if args.start:
        if not os.path.exists("simu"):
            os.makedirs("simu")
        lab = Lab("simu","simu")
        BRETAGNE.init.create_network(lab)
        if args.wireshark:
            for wireshark in args.wireshark:
                BRETAGNE.init.add_wireshark_on(wireshark, wireshark_count,lab)
                wireshark_count=wireshark_count+1
        if args.metasploit:
            for metasploit in args.metasploit:
                BRETAGNE.init.add_metasploit_on(metasploit,lab)
        BRETAGNE.init.start(lab)
    elif args.control:
        BRETAGNE.control.control(args.control)
    elif args.generate_traffic:
        BRETAGNE.Generate_traffic.start(args.generate_traffic)
    elif args.stop:
        BRETAGNE.stop.stop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="cage challenge 4 scenario simulation with kathara")
    parser.add_argument("--start",action="store_true", help="Simple simulation start-up")
    parser.add_argument("--stop",action="store_true", help="Stop simulation")
    parser.add_argument("--wireshark",nargs="+", help="Deploy Wireshark instances on the networks specified in the command line")
    parser.add_argument("--metasploit",nargs="+", help="Deploy Metasploit instances on the networks specified in the command line")
    parser.add_argument("--control",type=str, help="Open a terminal on the specified node")
    parser.add_argument("--generate_traffic",type=int, help="Generate x random connection")
    args = parser.parse_args()

    if not any(vars(args).values()):
        parser.print_help()
    else:
        main(args)