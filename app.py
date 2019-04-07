import argparse
import sys
from program import Thread
from services import Service


def run_threads(threads):
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


def start_server():
    print("Running server.")
    threads = [
        Thread(Service.SIGN_UP.value),
        Thread(Service.QUERY.value),
        Thread(Service.HEARTBEAT.value)
    ]
    run_threads(threads)


def start_client(args):
    print("Running client.")
    threads = []
    server_ip = args.client[0]
    services = args.__dict__
    for service in services:
        if services[service] is True:
            threads.append(client_threads_factory(service, server_ip))
    run_threads(threads)


def client_threads_factory(service, server_ip):
    return {
        Service.SIGN_UP.name: Thread(Service.SIGN_UP.value, server_ip, client=True),
        Service.HEARTBEAT.name: Thread(Service.HEARTBEAT.value, server_ip, client=True),
        Service.QUERY.name: Thread(Service.QUERY.value, server_ip, client=True)
    }.get(service.upper())


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

