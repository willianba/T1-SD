import argparse
import sys
from program import Thread
from services import Service


def start_server():
    print("Running server.")
    threads = [
        Thread(Service.SIGN_UP.value),
        Thread(Service.QUERY.value)
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def start_client(args):
    print("Running client.")
    thread = None
    server_ip = args.client[0]
    if args.signup:
        thread = Thread(Service.SIGN_UP.value, server_ip, client=True)
    elif args.query:
        thread = Thread(Service.QUERY.value, server_ip, client=True)
    thread.start()
    thread.join()


def main():
    ap = argparse.ArgumentParser(description="Client Server / P2P", prog="app")
    ap.add_argument("-c", "--client", metavar="SERVER", nargs=1,
                    help="Start program as client. Need to specify host as parameter and service with another flag.")
    ap.add_argument("-s", "--server", action='store_true',
                    help="Start program as server. Run all services in different threads.")
    ap.add_argument("-su", "--sign_up", action='store_true', help="Execute sign up service.")
    ap.add_argument("-q", "--query", action='store_true', help="Execute query service.")
    ap.add_argument("-hb", "--heartbeat", action='store_true', help="Execute heartbeat service.")
    args = ap.parse_args()
    if args.client:
        start_client(args)
    elif args.server:
        start_server()
    else:
        print("Need to start server or run a client with a service.")
        sys.exit(0)


if __name__ == "__main__":
    main()

