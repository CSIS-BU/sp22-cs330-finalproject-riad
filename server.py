import sys
import socket
import shared
import json
from shared import PacketType, send, receive

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
		server.listen(shared.MAX_CONNECTIONS)
		print("Server listening on {}:{}".format(shared.SERVER_IP, server_port))

		try:
			while True:
				(client, address) = server.accept()

				with client:
					# A client has connected, ask them for the number range they want.
					# It should still be within our predefined values in config.
					send(client, PacketType.ASK_CLIENT_MIN_MAX, shared.MIN_NUMBER, shared.MAX_NUMBER)

					"""
					while True:
						data = client.recv(config.MAX_PACKET_SIZE)
						if not data:
							break
						print("Got data")
						print(data)
						sys.stdout.flush()
					"""
		except KeyboardInterrupt:
			print("Server cancelled. Exiting.")
			server.close()
			sys.exit(0)
		except Exception as err:
			print("Got unknown error")
			server.close()
			raise err

def main():
	"""Main entry function."""
	# Probably just going to accept a single argument as the port, and let the program decide the number randomly. 

	if len(sys.argv) != 2:
		sys.exit("Usage: python3 server.py [Server Port]")
	
	server_port = int(sys.argv[1])
	do_server(server_port)


if __name__ == "__main__":
	main()
