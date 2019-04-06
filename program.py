import socket
import threading
import sys
import os
import json

services = {
    5000: "Sign Up",
    5100: "future 1",
    5200: "future 2"
}


def service_undefined():
    print("Service undefined.\nAvailable are:")
    for service in services:
        print(f'{service}: {services[service]}')
    sys.exit(-1)


class Thread(threading.Thread):
    def __init__(self, host, port, client=False):
        threading.Thread.__init__(self)
        self.client = client
        self.host = host
        self.port = int(port)
        self.resources = {}

    def run(self):
        self.select_server_or_client()

    def server_switch(self, service):
        return {
            5000: self.server_sign_up
        }.get(service, service_undefined)

    def client_switch(self, service):
        return {
            5000: self.client_sign_up
        }.get(service, service_undefined)

    def select_server_or_client(self):
        if self.client is False:
            print("Running server.")
            self.run_service(self.port)
        else:
            print("Running client.")
            self.execute_service(self.port)

    def run_service(self, port):
        self.server_switch(port)()

    def execute_service(self, port):
        self.client_switch(port)()

    def client_sign_up(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.host, self.port)
        folder = input("Specify folder to share files: ")
        files = os.listdir(folder)
        data = {'files': files}
        try:
            sock.sendto(json.dumps(data).encode(), server_address)
            print('Waiting server response')
            data, server = sock.recvfrom(4096)
            print(f'Received: {data.decode()}')
        finally:
            sock.close()

    def server_sign_up(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = (self.host, self.port)
        sock.bind(server_address)
        while True:
            print('Waiting for client connection')
            data, address = sock.recvfrom(4096)
            client_ip = address[0]
            data = json.loads(data)
            files = data['files']
            print(f"Client {client_ip} connected and sent {len(files)} files")
            if data:
                print('Confirming connection')
                self.resources[client_ip] = files
                sock.sendto(b"Connected", address)
