import argparse
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
                    help="Start program as client. Need to specify host and service with another flag.")
    ap.add_argument("-s", "--server", action='store_true',
                    help="Start program as server. Need to specify service with another flag.")
    ap.add_argument("--signup", action='store_true', help="Execute sign up service.")
    ap.add_argument("--query", action='store_true', help="Execute query service.")
    args = ap.parse_args()
    if args.client:
        start_client(args)
    elif args.server:
        start_server()


if __name__ == "__main__":
    main()

