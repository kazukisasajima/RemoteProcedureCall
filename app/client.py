import json
import socket
import sys

class Client:
    def __init__(self, server_address):
        self.server_address = server_address

    def start(self):
        flag = True
        while flag:
            input_str = input('Enter request file number (or "exit" to quit): ')
            if input_str == 'exit':
                flag = False
            else:
                try:
                    with open(f'../api/request{input_str}.json', 'r') as f:
                        message = f.read()

                    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    sock.connect(self.server_address)
                    sock.sendall(message.encode())

                    sock.settimeout(2)

                    try:
                        data = sock.recv(4096).decode()
                        if data:
                            print(f'Server response: {data}')
                    except socket.timeout:
                        print('Socket timeout, ending listening for server messages')
                    finally:
                        sock.close()
                except FileNotFoundError:
                    print(f'File request{input_str}.json not found.')

if __name__ == '__main__':
    client = Client("/tmp/socket_file")
    client.start()
