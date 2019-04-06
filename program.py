from services import Service
import socket
import threading
import sys
import os
import json


# this is the default value for the switch statement below
def service_undefined():
    print("Service undefined.")
    sys.exit(-1)


class Thread(threading.Thread):
    def __init__(self, port, host="localhost", client=False):
        threading.Thread.__init__(self)
        self.client = client
        self.host = host
        self.port = port
        self.resources = {}

    def run(self):
        self.select_server_or_client()

    # since python doesn't have a switch case statement, this is a way to implement it
    def server_switch(self, service):
        return {
            Service.SIGN_UP.value: self.server_sign_up
        }.get(service, service_undefined)

    # since python doesn't have a switch case statement, this is a way to implement it
    def client_switch(self, service):
        return {
            Service.SIGN_UP.value: self.client_sign_up
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
        try:
            files = os.listdir(folder)
            data = {'files': files}
            sock.sendto(json.dumps(data).encode(), server_address)
            print('Waiting server response')
            data, server = sock.recvfrom(4096)
            print(f'Received: {data.decode()}')
        except FileNotFoundError:
            print("This folder doesn't exist.")
            self.client_sign_up()
        except socket.gaierror:
            print("Host unavailable.")
            sys.exit(-2)
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
