import sys
import socket
import shared
import json
from shared import PacketType, send, receive

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
		client.connect((shared.SERVER_IP, server_port))
		print("Connected to {}:{}".format(shared.SERVER_IP, server_port))

		# We should get a message from the server asking us to pick a number with some bounds.
		packet, data = receive(client)
		

		"""
		data = client.recv(config.MAX_PACKET_SIZE)
		if (data != PacketType.ASK_CLIENT_MIN_MAX.value):
			raise Exception("Expected ASK_CLIENT_MIN_MAX")
		"""
		
		# Respond to the server with a number.

		"""
		code = client.sendall(b"Hello")
		if code == 0:
			raise RuntimeError("Socket disconnected")
		"""

	print("Connection closed")


def main():
	"""Main entry function."""

	if len(sys.argv) != 2:
		sys.exit("Usage: python3 client.py [Server Port]")
	
	server_port = int(sys.argv[1])
	do_client(server_port)


if __name__ == "__main__":
	main()
