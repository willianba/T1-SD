from services import Service
from time import sleep
import socket
import threading
import sys
import os
import json

resources = {}
connected_clients = {}
timeout = 2
verification_time = 5
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


def create_new_client(client_ip, files):
    semaphore.acquire()
    global resources
    global connected_clients
    resources[client_ip] = files
    connected_clients[client_ip] = timeout
    semaphore.release()


def decrease_all_clients():
    semaphore.acquire()
    global resources
    global connected_clients
    for client in connected_clients:
        connected_clients[client] -= 1
    semaphore.release()


def increase_client(client_ip):
    semaphore.acquire()
    global connected_clients
    connected_clients[client_ip] += 1
    semaphore.release()


def remove_inactive_clients():
    remove_value = 0
    removed_clients = []
    semaphore.acquire()
    global resources
    global connected_clients
    for client in connected_clients:
        client_value = connected_clients[client]
        if client_value <= remove_value:
            removed_clients.append(client)
    for client in removed_clients:
        print(f"Removing {client} due to inactivity")
        del resources[client]
        del connected_clients[client]
    semaphore.release()


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

    def select_server_or_client(self):
        if not self.client:
            self.sock.bind(self.server_address)
        self.execute_service()()

    # since python doesn't have a switch case statement, this is a way to implement it
    def execute_service(self):
        if self.client:
            return {
                Service.SIGN_UP.value: self.client_sign_up,
                Service.QUERY.value: self.client_query_files
            }.get(self.port, service_undefined)
        else:
            return {
                Service.SIGN_UP.value: self.server_sign_up,
                Service.QUERY.value: self.server_query_files
            }.get(self.port, service_undefined)

    def execute_client_func(self, func, folder=None):
        try:
            if folder:
                func(folder)
            else:
                func()
        except FileNotFoundError:
            print("This folder doesn't exist.")
            self.client_sign_up()
        except ConnectionResetError:
            print("There are no running hosts.")
            sys.exit(-2)
        except socket.gaierror:
            print("Host unavailable.")
            sys.exit(-2)
        finally:
            self.sock.close()

    def sign_up(self, folder):
        files = os.listdir(folder)
        data = {'files': files}
        self.sock.sendto(json.dumps(data).encode(), self.server_address)
        print('Waiting server response.')
        data, server = self.sock.recvfrom(4096)
        print(f'Received: {data.decode()}')

    def query(self):
        self.sock.sendto(b"query", self.server_address)
        print("Waiting files from server.")
        data = self.sock.recv(4096)
        data = json.loads(data)
        files = data['files']
        print(f"These are the available files: {', '.join([str(x) for x in files])}")

    def client_sign_up(self):
        folder = input("Specify folder to share files: ")
        self.execute_client_func(self.sign_up, folder)

    def client_query_files(self):
        self.execute_client_func(self.query)

    def server_sign_up(self):
        data, address = self.sock.recvfrom(4096)
        client_ip = address[0]
        data = json.loads(data)
        files = data['files']
        print(f"Client {client_ip} connected and sent {len(files)} files.")
        if data:
            print('Confirming connection.')
            semaphore.acquire()
            global resources
            resources[client_ip] = files
            semaphore.release()
            self.sock.sendto(b"Connected", address)

    def server_query_files(self):
        data, address = self.sock.recvfrom(4096)
        client_ip = address[0]
        print(f"Sending {client_ip} a list of available files.")
        files = get_all_files()
        self.sock.sendto(json.dumps(files).encode(), address)
