import sys
import socket
import shared
from shared import *

# Variables here to remember the minimum and maximum range
# Maybe another to remember our previous inputs, so we don't waste more guesses by repeating guesses.

minimum_number = None
maximum_number = None
guess_history = []

def getGuess():
	while True:
		num = promptNumber("Guess between {} and {}: ".format(minimum_number, maximum_number))
		if num < minimum_number:
			print("\tThat's below the minimum!")
		elif num > maximum_number:
			print("\tThat's above the maximum!")
		elif num in guess_history:
			print("\tYou've already tried that number!")
		else:
			# All good.
			guess_history.append(num)
			return num

def promptNumber(prompt):
	while True:
		res = input(prompt)

		try:
			res = int(res)
			return res
		except ValueError:
			print("\tInvalid input, please input a number.")


def establishMinAndMax(min, max):
	global minimum_number, maximum_number

	# Get user's desired minimum number
	while True:
		minimum_number = promptNumber("Choose a minimum number between {} and {}: ".format(min, max - 2))
		if minimum_number < min or minimum_number > max - 2:
			print("\tPlease select a number between {} and {}".format(min, max - 2))
		else:
			break

	# Get user's desired maximum number
	while True:
		maximum_number = promptNumber("Choose a maximum number between {} and {}: ".format(minimum_number + 1, max))
		if maximum_number < minimum_number + 1 or maximum_number > max:
			print("\tPlease select a number between {} and {}".format(minimum_number + 1, max))
		else:
			break

	# Store the result
	print("Your minimum and maximum bounds are {} and {}".format(minimum_number, maximum_number))


def doClient(server_port):
	"""Connection to server."""

	# Connection handling here, maybe another function for receiving user input?
	# It would be cleaner that way.

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
		client.connect((shared.SERVER_IP, server_port))
		print("Connected to {}:{}".format(shared.SERVER_IP, server_port))

		#############################################################################################################################
		# We should get a message from the server asking us to pick a number with some bounds.
		data = receivePacket(client, PacketType.ASK_CLIENT_MIN_MAX)
		print("Server enforced min & max: {} & {}".format(data[0], data[1]))
		establishMinAndMax(data[0], data[1])
		
		# Reply to the server.
		send(client, PacketType.GIVE_SERVER_MIN_MAX, minimum_number, maximum_number)
		#############################################################################################################################
		# We should get a message saying we can start now.
		receivePacket(client, PacketType.START_GUESSING)
		# Let's begin the guessing!
		
		while True:
			num = getGuess()
			# Send our guess.
			send(client, PacketType.GUESS, num)
			# Wait for the server's response.
			packet, data = receive(client)
			if packet == PacketType.GUESS_CORRECT:
				print("We got it!")
				break
			elif packet == PacketType.GUESS_INCORRECT:
				print("Nope... Try again!")
			else:
				# print("Received unknown packet...")
				raise RuntimeError("Received unknown packet!")
		

	print("Connection closed")


def main():
	"""Main entry function."""

	if len(sys.argv) != 2:
		sys.exit("Usage: python3 client.py [Server Port]")
	
	server_port = int(sys.argv[1])
	doClient(server_port)


if __name__ == "__main__":
	main()
