import argparse
from program import Thread
from services import Service


def start_program(args):
    if args.client:
        if args.signup:
            Thread(Service.SIGN_UP.value, args.client[0], client=True).start()
    elif args.server:
        if args.signup:
            Thread(Service.SIGN_UP.value).start()


def main():
    ap = argparse.ArgumentParser(description="Client Server / P2P", prog="app")
    ap.add_argument("-c", "--client", metavar="SERVER", nargs=1,
                    help="Start program as client. Need to specify host and service with another flag.")
    ap.add_argument("-s", "--server", action='store_true',
                    help="Start program as server. Need to specify service with another flag.")
    ap.add_argument("--signup", action='store_true', help="Start sign up service.")
    args = ap.parse_args()
    start_program(args)


if __name__ == "__main__":
    main()
