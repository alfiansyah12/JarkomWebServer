import socket

def tcp_server():
    SERVER_HOST = "localhost"
    SERVER_PORT = 8090

    # buat socket tcp IP
    sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # mengatur opsi socket untuk socket server
    sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # menyimpan alamat IP dan port
    sock_server.bind((SERVER_HOST, SERVER_PORT))

    # mulai socket server
    sock_server.listen()

    print("Server ready....")

    # melakukan perulangan hingga socket server menerima koneksi dari client
    while True:
        sock_client, client_address = sock_server.accept()

        request = sock_client.recv(1024).decode()
        print("Dari Client:"+request)

        response = handle_request()
        sock_client.send(response.encode())
        sock_client.close()
    #endwhile
    sock_server.close()

# membuat fungsi untuk menerima respons yang akan dikirimkan kepada client
def handle_request():
    response_line = "HTTP/1.1 200 OK\r\n"
    content_type = "Content-Type: text/html\r\n\r\n"

    file = open("html_docs/index.html", 'r')
    message_body = file.read()
    file.close()

    response = response_line+content_type+message_body
    return response
if __name__ == '__main__':
    tcp_server()