""" Trystan Kaes
    July 27 2020
    Chat Client """
import socket
import select
import sys
import os

from PIL import Image

import encoder

def size(fname):
    """ Get the size of a file. """
    return os.stat(fname).st_size

def upload_file(send_file, sock):
    """ Upload file to the server """
    photo_buffer = 4096

    picture = open(send_file, 'rb')
    # print(f'SIUDVWEFJK {size(send_file)} ')
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
    photo_buffer = 4096
    filename = f"totally_not_secret{download_count}.png"
    new_photo = open(filename, 'wb')

    newfile_size = photo_buffer
    # receive data and write it to file
    data = sock.recv(photo_buffer)
    while data:
        data = sock.recv(photo_buffer)
        newfile_size += len(data)
        if int(filesize) <= newfile_size:
            break
        new_photo.write(data)
    new_photo.close()
    print("[New File Available]")

def help_command():
    """ Help info for the chat """
    print()
    print()
    print("*************************************************************")
    print("**************************  HELP  ***************************")
    print("*************************************************************")
    print("/help     <------- Get help. You did that!")
    print("/open     <------- Open last sent picture")
    print("/encrypt [message]      <------- Encrypt this message")
    print("/decrypt  <------- decrypt last encrypted message ")
    print("/list  <------- lists the contents of the current working directory")
    print("/exit  <------- exit the chat ")
    print()
    print()

def parse_command(message, sock):
    """ parse_command checks the input for a command and executes if found """
    was_command = False
    if message == "":
        return was_command

    if message[0] == '/':
        was_command = True
        if '/help' in message:
            help_command()
        elif '/open' in message:
            open_command(message)
        elif '/encrypt' in message:
            encrypt_command(message, sock)
        elif '/decrypt' in message:
            decrypt_command(message)
        elif '/list' in message:
            list_directory()
        elif '/exit' in message:
            sys.exit()
        else:
            print("**** Unknown Command ****")
    return was_command

def open_command(message):
    """ open_command opens the last recieved incrypted messages """
    if message[5:] == "":
        print("[No File Specificed]")

    filename = message[5:]

    if os.path.isfile(filename):
        try:
            picture = Image.open(filename, 'r')
            picture.show()
        except Image.UnidentifiedImageError:
            print("That message is no longer available.")
    else:
        print("[FileNotFoundError]")

def list_directory():
    """ list_directory shows the directory contents of cwd """
    os.system("ls")
    print()

def encrypt_command(message, sock):
    """ encrypt_command encrypts and sends the message """
    message = message[9:]

    filename = input("Enter a file you would like to hide your message in: ")

    if os.path.isfile(filename):
        send_file = encoder.encode(filename, message)
        upload_file(send_file, sock)
    else:
        print("[FileNotFoundError]")


def decrypt_command(message):
    """ encrypt_command decrypts the last recieved encrypted message """
    filename = input("Enter a file you would like to decrypt: ")

    if os.path.isfile(filename):
        picture = Image.open(filename, 'r')
        message = encoder.decode(picture)
        print(f"[[[%#   {message}   #%]]]")
    else:
        print("[FileNotFoundError]")

def user_prompt():
    """ user_prompt displays a formated prompt that waits for their input """
    sys.stdout.write('\nYou > ')
    sys.stdout.flush()

def main():
    """ Main function for the chat client """
    # Check args
    if len(sys.argv) < 3:
        print('chat_client: insufficient system arguments')
        print('try: chat_client.py [hostname] [port]')
        sys.exit()
    host = sys.argv[1]
    port = int(sys.argv[2])

    downloads = 0

    # Initialize Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    # Try to connect
    try:
        sock.connect((host, port))
        name = input("Enter your username: ")
        sock.send(bytes(name, "UTF-8"))
    except socket.error:
        print('Unable to connect: %s' % socket.error)
        sys.exit()

    print('Connected.')
    print('Type /help to get a list of commands.')
    print('Happy Chatting!')
    user_prompt()
    while True:
        input_sources = [sys.stdin, sock]

        # Poll the inputs
        system_input, _, _ = select.select(input_sources, [], [])

        for source in system_input:

            # If it is from the server
            if source == sock:
                data = source.recv(4096).decode("UTF-8")
                if not data:
                    print('\nDisconnected from chat server')
                    sys.exit()
                else:
                    if data.startswith('SIUDVWEFJK'):
                        filesize = data.split()[1]
                        print("*** Incoming encrypted message ***")
                        sock.send(bytes("READY", "UTF-8"))
                        download_file(sock, filesize, downloads)
                        downloads += 1
                    else:
                        #print data
                        sys.stdout.write(data)
                        user_prompt()

            # If it is from the user
            else:
                msg = input().rstrip()
                if not parse_command(msg, sock):
                    sock.send(bytes(msg, "UTF-8"))
                user_prompt()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit()
