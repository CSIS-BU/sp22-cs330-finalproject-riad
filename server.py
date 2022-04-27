import sys
import socket

SERVER_IP = "127.0.0.1"
MAX_CONNECTIONS = 10
MAX_PACKET_SIZE = 1024

# Some kind of dict here to keep track of each player's correct number?
# Maybe index could be the socket id, value as another dict? {int correctNumber, int rangeStart, int rangeEnd, list guessHistory}?

def generate_user_number():
	"""Function to generate a number for the connected user."""
	pass

def do_server(server_port):
	"""Connection logic handler."""

	# Connection handling here, the random guessing part will likely be handled in separate function calls.
	# It would be cleaner that way.
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
		server.bind(("", server_port))
		server.listen(MAX_CONNECTIONS)
		print("Server listening on {}:{}".format(SERVER_IP, server_port))

		while True:
			(client, address) = server.accept()

			with client:
				# A client has connected, ask them for the number range they want.

				"""
				while True:
					data = client.recv(MAX_PACKET_SIZE)
					if not data:
						break
					print("Got data")
					print(data)
					sys.stdout.flush()
				"""

def main():
	"""Main entry function."""
	# Probably just going to accept a single argument as the port, and let the program decide the number randomly. 

	if len(sys.argv) != 2:
		sys.exit("Usage: python3 server.py [Server Port]")
	
	server_port = int(sys.argv[1])
	do_server(server_port)


if __name__ == "__main__":
	main()
