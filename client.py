import sys
import socket

SERVER_IP = "127.0.0.1"

# Variables here to remember the minimum and maximum range
# Maybe another to remember our previous inputs, so we don't waste more guesses by repeating guesses.

def getUserInput():
	"""Function to get user input?"""

	# Read the user's input
	# Make sure it's within the expected number range
	# If acceptable, return back to client

	pass

def do_client(server_port):
	"""Connection to server."""

	# Connection handling here, maybe another function for receiving user input?
	# It would be cleaner that way.

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
		client.connect((SERVER_IP, server_port))
		print("Connected to {}:{}".format(SERVER_IP, server_port))

		code = client.sendall(b"Hello")
		if code == 0:
			raise RuntimeError("Socket disconnected")

	print("Connection closed")


def main():
	"""Main entry function."""

	if len(sys.argv) != 2:
		sys.exit("Usage: python3 client.py [Server Port]")
	
	server_port = int(sys.argv[1])
	do_client(server_port)


if __name__ == "__main__":
	main()
