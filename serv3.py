import os
import socket

# Server address and port
HOST = '127.0.0.1'
PORT = 8090

# Response status codes
STATUS_OK = '200 OK'
STATUS_NOT_FOUND = '404 Not Found'

# Response headers
HEADERS_OK = {
    'Content-Type': 'text/html; encoding=utf8',
    'Content-Length': 0,
    'Connection': 'close',
}
HEADERS_NOT_FOUND = {
    'Content-Type': 'text/html; encoding=utf8',
    'Content-Length': 0,
    'Connection': 'close',
}

class MyTCPHandler:
    def __init__(self, sock):
        self.sock = sock

    def handle(self):
        # Receive data from client
        data = self.sock.recv(1024)

        # Parse HTTP request
        try:
            request = data.decode().split('\r\n')
            method, path, version = request[0].split()
        except:
            return

        # Check if method is GET
        if method != 'GET':
            return

        # Build file path
        file_path = os.path.join(os.getcwd(), path.lstrip('/'))

        # Check if file exists
        if not os.path.isfile(file_path):
            self.send_response(STATUS_NOT_FOUND, HEADERS_NOT_FOUND)
            return

        # Read file
        with open(file_path, 'rb') as f:
            content = f.read()

        # Build response headers
        headers = HEADERS_OK.copy()
        headers['Content-Length'] = len(content)

        # Send response
        self.send_response(STATUS_OK, headers, content)

    def send_response(self, status, headers, content=b''):
        # Build response message
        response = f'HTTP/1.1 {status}\r\n'
        for key, value in headers.items():
            response += f'{key}: {value}\r\n'
        response += '\r\n'
        response = response.encode() + content

        # Send response to client
        self.sock.sendall(response)

if __name__ == '__main__':
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set socket options to reuse address and port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f'Server listening on {HOST}:{PORT}...')

    while True:
        # Accept incoming connection
        client_socket, client_address = server_socket.accept()

        # Handle incoming connection in a separate thread
        handler = MyTCPHandler(client_socket)
        handler.handle()