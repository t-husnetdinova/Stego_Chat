all:
	mkdir client1
	mkdir client2
	cp chat_client.py client1/chat_client.py
	cp chat_client.py client2/chat_client.py
	cp pic.png client1/pic.png
	cp pic.png client2/pic.png

	mkdir server
	cp chat_server.py server/chat_server.py
	python3 chat_server.py 5000

clean:
	rm -rf client1 client2 server
