from program import *
import argparse


def start_program(args):
    if args.client:
        Thread(args.client[1], args.client[0]).start()
    elif args.server:
        Thread(args.server[0]).start()


def main():
    ap = argparse.ArgumentParser(description="Client Server / P2P", prog="app")
    ap.add_argument("-c", "--client", metavar=("SERVER", "PORT"), nargs=2,
                    help="Start program as client. Need to specify host and port.")
    ap.add_argument("-s", "--server", metavar="PORT", nargs=1, type=int,
                    help="Start program as server. Need to specify port.")
    args = ap.parse_args()
    start_program(args)


if __name__ == "__main__":
    main()
