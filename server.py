import sys

# Some kind of dict here to keep track of each player's correct number?
# Maybe index could be the socket id, value as the correct number

def generate_user_number():
	"""Function to generate a number for the connected user."""
	pass

def server():
	"""Connection logic handler."""

	# Connection handling here, the random guessing part will likely be handled in separate function calls.
	# It would be cleaner that way.
	pass

def main():
	"""Main entry function."""
	# Probably just going to accept a single argument as the port, and let the program decide the number randomly. 

	if len(sys.argv) > 0:
		sys.exit("Not ready yet!")


if __name__ == "__main__":
	main()
