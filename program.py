from services import Service
import socket
import threading
import sys
import os
import json

resources = {}
semaphore = threading.Condition()


# this is the default value for the switch statement below
def service_undefined():
    print("Service undefined.")
    sys.exit(-1)


def get_all_files():
    semaphore.acquire()
    global resources
    result = {'files': []}
    for nested_list in list(resources.values()):
        for key_list in nested_list:
            result['files'].append(key_list)
    semaphore.release()
    return result


class Thread(threading.Thread):
    def __init__(self, port, host="localhost", client=False):
        threading.Thread.__init__(self)
        self.client = client
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.host, self.port)

    def run(self):
        self.select_server_or_client()

    # since python doesn't have a switch case statement, this is a way to implement it
    def server_switch(self, service):
        return {
            Service.SIGN_UP.value: self.server_sign_up,
            Service.QUERY.value: self.server_query_files
        }.get(service, service_undefined)

    # since python doesn't have a switch case statement, this is a way to implement it
    def client_switch(self, service):
        return {
            Service.SIGN_UP.value: self.client_sign_up,
            Service.QUERY.value: self.client_query_files
        }.get(service, service_undefined)

    def select_server_or_client(self):
        if self.client is False:
            self.sock.bind(self.server_address)
            while True:
                self.run_service(self.port)
        else:
            self.execute_service(self.port)

    def run_service(self, port):
        self.server_switch(port)()

    def execute_service(self, port):
        self.client_switch(port)()

    def client_sign_up(self):
        folder = input("Specify folder to share files: ")
        try:
            files = os.listdir(folder)
            data = {'files': files}
            self.sock.sendto(json.dumps(data).encode(), self.server_address)
            print('Waiting server response')
            data, server = self.sock.recvfrom(4096)
            print(f'Received: {data.decode()}')
        except FileNotFoundError:
            print("This folder doesn't exist.")
            self.client_sign_up()
        except socket.gaierror:
            print("Host unavailable.")
            sys.exit(-2)
        finally:
            self.sock.close()

    def server_sign_up(self):
        data, address = self.sock.recvfrom(4096)
        client_ip = address[0]
        data = json.loads(data)
        files = data['files']
        print(f"Client {client_ip} connected and sent {len(files)} files")
        if data:
            print('Confirming connection')
            semaphore.acquire()
            global resources
            resources[client_ip] = files
            semaphore.release()
            self.sock.sendto(b"Connected", address)

    def client_query_files(self):
        self.sock.sendto(b"query", self.server_address)
        print("Waiting files from server")
        data = self.sock.recv(4096)
        data = json.loads(data)
        files = data['files']
        print(f"These are the available files: {', '.join([str(x) for x in files])}")

    def server_query_files(self):
        data, address = self.sock.recvfrom(4096)
        client_ip = address[0]
        print(f"Sending {client_ip} a list of available files")
        files = get_all_files()
        self.sock.sendto(json.dumps(files).encode(), address)
