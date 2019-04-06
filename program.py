import threading
import sys


def exit_service_undefined():
    print("Service Undefined. Exiting.")
    sys.exit(-1)


class Thread(threading.Thread):
    def __init__(self, port, host=None):
        threading.Thread.__init__(self)
        self.host = host
        self.port = int(port)
        self.resources = {}

    def run(self):
        self.select_server_or_client()

    def server_switch(self, service):
        return {
            4500: self.server_sign_up
        }.get(service, exit_service_undefined())

    def client_switch(self, service):
        return {
            4500: self.client_sign_up
        }.get(service, exit_service_undefined())

    def select_server_or_client(self):
        if self.host is None:
            print("Running server")
            while True:
                self.run_service(self.port)
        else:
            print("Running client")
            self.execute_service(self.port)

    def run_service(self, port):
        self.server_switch(port)

    def execute_service(self, port):
        self.client_switch(port)

    def client_sign_up(self):
        print("signed up")

    def server_sign_up(self):
        print("running sign up")
