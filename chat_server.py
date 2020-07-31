""" Trystan Kaes
    July 27 2020
    Chat Server """
import socket
import select
import sys
import os

FILENAME = "image"
CONNECTION_LIST = []
USERNAME_TRANSLATOR = {}
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2

def size(fname):
    """ Get the size of a file. """
    return os.stat(fname).st_size

def sendfile(send_file, sock):
    """ Send file to client """
    photo_buffer = 4096

    picture = open(send_file, 'rb')
    print(f'SIUDVWEFJK {size(send_file)} ')
    sock.send(bytes('SIUDVWEFJK %s ' % size(send_file), "UTF-8"))

    data = sock.recv(96).decode("UTF-8")

    if "READY" in data:
        while True:
            data = picture.read(photo_buffer)
            if not data:
                # done
                break
            sock.sendall(data)
    picture.close()
    print("[message sent]")

def download_file(sock, filesize, download_count):
    """ Servers Download function """
    print(filesize)
    photo_buffer = 4096
    filename = FILENAME + str(download_count) + ".png"
    new_photo = open(filename, 'wb')

    newfile_size = photo_buffer
    # receive data and write it to file
    data = sock.recv(photo_buffer)
    new_photo.write(data)
    while data:
        data = sock.recv(photo_buffer)
        newfile_size += len(data)
        if int(filesize) <= newfile_size:
            break
        new_photo.write(data)
    new_photo.close()
    print("File Downloaded")
    return filename

def broadcast_message(server_socket, sending_sock, message):
    """ Function to broadcast chat messages to all connected clients """
    for connection in CONNECTION_LIST:
        if connection not in (server_socket, sending_sock):
            try:
                connection.send(bytes(message, "UTF-8"))
            except socket.error:
                connection.close()
                try:
                    CONNECTION_LIST.remove(socket)
                except ValueError:
                    print("Recovered from value error")

def broadcast_picture(server_socket, sending_sock, filename):
    """ Function to broadcast chat messages to all connected clients """
    for connection in CONNECTION_LIST:
        if connection not in (server_socket, sending_sock):
            try:
                print(f"Broadcasting to {connection.getpeername()}")
                sendfile(filename, connection)
            except socket.error:
                connection.close()
                try:
                    CONNECTION_LIST.remove(socket)
                except ValueError:
                    print("Recovered from value error")


def main():
    """ Main function for the chat server """

    # Check args
    if len(sys.argv) < 2:
        print('chat_server: insufficient system arguments')
        print('try: chat_server.py [port]')
        sys.exit()
    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port)) # Localhost
    server_socket.listen(5)

    CONNECTION_LIST.append(server_socket)

    print(f"Listening on {str(port)} ")

    downloads = 0

    while True:
        # Compile list for polling
        read_sockets, _, _ = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            # If this is the server socket this is a new connection
            if sock == server_socket:
                sockfd, addr = server_socket.accept()

                # Set username
                username = sockfd.recv(RECV_BUFFER).decode("UTF-8")
                CONNECTION_LIST.append(sockfd)

                if username:
                    USERNAME_TRANSLATOR[f"{addr[0]}:{addr[1]}"] = username
                else: # Fail case
                    USERNAME_TRANSLATOR[f"{addr[0]}:{addr[1]}"] = sockfd.getpeername()

                print(f"Client ({addr[0]}, {addr[1]}) connected as {username}")

                broadcast_message(server_socket, sockfd, f"\r[{username} entered room]\n")

            else:
                try:
                    addr = sock.getpeername()
                    key = f"{addr[0]}:{addr[1]}"
                except OSError:
                    print("I just almost died.")
                try:
                    data = sock.recv(RECV_BUFFER).decode("UTF-8")
                    if data:
                        if data.startswith('SIUDVWEFJK'):
                            filesize = data.split()[1]
                            print("Incoming Picture of size %", filesize)
                            sock.send(bytes("READY", "UTF-8"))
                            filename = download_file(sock, filesize, downloads)
                            downloads += 1
                            broadcast_message(server_socket, sock, \
                                              f"\r[{username} uploaded an encrypted message]\n")
                            broadcast_picture(server_socket, sock, filename)
                        else:
                            broadcast_message(server_socket, sock, "\r" +
                                              USERNAME_TRANSLATOR[key] + '> ' + data)

                except socket.error:
                    broadcast_message(server_socket, sock, "\r[" +
                                      USERNAME_TRANSLATOR[key] + " has left the chat]\n")
                    print(f"Client ({addr[0]}, {addr[1]}) is offline")
                    sock.close()
                    try:
                        CONNECTION_LIST.remove(sock)
                        USERNAME_TRANSLATOR.pop(key)
                    except ValueError:
                        print("Recovered from value error")
                    continue
                except KeyError:
                    print("I tried to access an invalid key and almost died.")

    server_socket.close()

if __name__ == "__main__":
    main()
