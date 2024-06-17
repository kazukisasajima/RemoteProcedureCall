import json
import math
import os
import socket
import sys
import threading

class Process:
    @staticmethod
    def process_method(method, params):
        try:
            if method == "floor":
                return Process.method_floor(params)
            elif method == "nroot":
                return Process.method_nroot(params)
            elif method == "reverse":
                return Process.method_reverse(params)
            elif method == "validAnagram":
                return Process.method_validAnagram(params)
            elif method == "sort":
                return Process.method_sort(params)
            else:
                raise ValueError("Invalid method")
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def method_floor(params):
        return math.floor(params[0])

    @staticmethod
    def method_nroot(params):
        n = params[0]
        x = params[1]
        return math.pow(x, 1/n)

    @staticmethod
    def method_reverse(params):
        string = params[0]
        return string[::-1]

    @staticmethod
    def method_validAnagram(params):
        return sorted(params[0]) == sorted(params[1])

    @staticmethod
    def method_sort(params):
        return sorted(params[0])

class Server:
    def __init__(self, server_address):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.server_address = server_address

    def bind_handler(self):
        try:
            os.unlink(self.server_address)
        except FileNotFoundError:
            pass

        print('Starting up on {}'.format(self.server_address))
        self.sock.bind(self.server_address)
        self.sock.listen(3)

    def receive_handler(self, connection, client_address):
        try:
            message = connection.recv(4096)
            if not message:
                raise ValueError("Empty message received")

            message_str = message.decode('utf-8')
            request = json.loads(message_str)

            method = request.get("method")
            params = request.get("params")
            id = request.get("id")

            if method is None or params is None or id is None:
                raise ValueError("Invalid request format")

            response_data = {}
            result = Process.process_method(method, params)
            response_data["results"] = result
            response_data["result_type"] = type(result).__name__
            response_data["id"] = id

            connection.sendall(json.dumps(response_data).encode())
        except Exception as e:
            try:
                response_data = {
                    "error": str(e),
                    "id": request.get("id", None) if 'request' in locals() else None
                }
                connection.sendall(json.dumps(response_data).encode())
            except:
                pass
        finally:
            connection.close()

    def start(self):
        self.bind_handler()

        while True:
            try:
                connection, client_address = self.sock.accept()
                thread = threading.Thread(target=self.receive_handler, args=(connection, client_address))
                thread.start()
            except KeyboardInterrupt:
                print('Closing socket')
                os.unlink(self.server_address)
                self.sock.close()
                sys.exit(1)

if __name__ == "__main__":
    server = Server("/tmp/socket_file")
    server.start()
