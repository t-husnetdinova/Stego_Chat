TRYSTAN KAES, TAMMY HUSNETDINOVA, ALEX VERKEST

CSCI 4742

Video Demo:

Final Project: Totally Just a Picture Sending Service

**************************************************************
************ TO UNPACK ----- 'make all'	                 *****
************ TO RUN --------- see below section     	   *****
**************************************************************

TO RUN:
To unpack type `make all`. This will unpack the program into separate directories for
testing purposes the file directory should look like
```
.
├── README.txt
├── chat_client.py
├── chat_server.py
├── client1
│   ├── chat_client.py
│   ├── encoder.py
│   └── pic.png
├── client2
│   ├── chat_client.py
│   ├── encoder.py
│   └── pic.png
├── encoder.py
├── makefile
├── pic.png
└── server
    └── chat_server.py
```

To run locally, open a terminal window in server, client1, and client2.
Start server by running `python3 chat_server.py [port]`.
Start the clietns by running `python3 chat_client.py localhost [port]`.

DESCRIPTION:
This project is a steganography based chat room. Clients can connect to the server
and chat away with the option of sending an encrypted message.
This 'security by obscurity' is achieved using steganography.


************Structure***********
This program has a server and clients
spread across chat_client.py and chat_server.py.
The clients use the encoder module to encrypt and decrypt messages into pictures.
Available commands in the clients are:
/help     <------- Get help. You did that!
/open     <------- Open last sent picture
/encrypt [message]      <------- Encrypt this message
/decrypt  <------- decrypt last encrypted message
/list  <------- lists the contents of the current working directory
/exit  <------- exit the chat

/open opens the picture in whatever the default image viewer application on the
machine is.
/encrypt [message] embeds `[message]` into the specified picture and
sends it to the server.
/decrypt opens the specified file and extracts any message that is hidden inside.
/list shows the contents of the current working directory


STATE OF COMPLETION:
Currently on KaliVM the png file is getting corrupted on upload from client to
server. This will be fixed in future iterations. Also KaliVM does not handle
PIL.Image.show well and thus this is also broken. All other issues stem from
these two bugs.

**************Status************
IN PROGRESS

**********************
** WORKS PARTIALLY  **
**********************


Sources:
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/select.html
https://medium.com/better-programming/image-steganography-using-python-2250896e48b9
