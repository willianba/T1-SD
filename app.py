from program import Thread
import sys
import argparse


def start_program(args):
    if args.client:
        Thread(args.client[0], args.client[1], client=True).start()
    elif args.server:
        Thread(args.server[0], args.server[1]).start()
    else:
        print("Unknown error.")
        sys.exit(-1)


def main():
    ap = argparse.ArgumentParser(description="Client Server / P2P", prog="app")
    ap.add_argument("-c", "--client", metavar=("SERVER", "PORT"), nargs=2,
                    help="Start program as client. Need to specify host, port, and folder with resources.")
    ap.add_argument("-s", "--server", metavar=("SERVER", "PORT"), nargs=2,
                    help="Start program as server. Need to specify port.")
    args = ap.parse_args()
    start_program(args)


if __name__ == "__main__":
    main()
