import sys
import socket
import shared
import json
from shared import *

# Variables here to remember the minimum and maximum range
# Maybe another to remember our previous inputs, so we don't waste more guesses by repeating guesses.

minimum_number = None
maximum_number = None
		

def getUserInput():
	"""Function to get user input?"""

	# Read the user's input
	# Make sure it's within the expected number range
	# If acceptable, return back to client

	pass

def promptNumber(prompt):
	while True:
		res = input(prompt)

		try:
			res = int(res)
			return res
		except ValueError:
			print("\tInvalid input, please input a number.")
	

def do_client(server_port):
	"""Connection to server."""

	# Connection handling here, maybe another function for receiving user input?
	# It would be cleaner that way.

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
		client.connect((shared.SERVER_IP, server_port))
		print("Connected to {}:{}".format(shared.SERVER_IP, server_port))

		#############################################################################################################################
		# We should get a message from the server asking us to pick a number with some bounds.
		data = receive_packet(client, PacketType.ASK_CLIENT_MIN_MAX)
		print("Server enforced min & max: {} & {}".format(data[0], data[1]))
		
		# Get user's desired minimum number
		while True:
			min = promptNumber("Choose a minimum number between {} and {}: ".format(data[0], data[1] - 1))
			if min < data[0] or min > data[1] - 1:
				print("\tPlease select a number between {} and {}".format(data[0], data[1] - 1))
			else:
				break

		# Get user's desired maximum number
		while True:
			max = promptNumber("Choose a maximum number between {} and {}: ".format(min + 1, data[1]))
			if max < min + 1 or max > data[1]:
				print("\tPlease select a number between {} and {}".format(min + 1, data[1]))
			else:
				break
		
		# Store the result and reply to the server.
		minimum_number = min
		maximum_number = max
		print("Your minimum and maximum bounds are {} and {}".format(minimum_number, maximum_number))
		#send(client, PacketType.GIVE_SERVER_MIN_MAX, minimum_number, maximum_number)
		#############################################################################################################################

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
