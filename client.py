import sys

# Variables here to remember the minimum and maximum range
# Maybe another to remember our previous inputs, so we don't waste more guesses by repeating guesses.

def getUserInput():
	"""Function to get user input?"""

	# Read the user's input
	# Make sure it's within the expected number range
	# If acceptable, return back to client

	pass

def client():
	"""Connection to server."""

	# Connection handling here, maybe another function for receiving user input?
	# It would be cleaner that way.

	pass


def main():
	"""Main entry function."""

	# Probably just going to accept a single argument as the port to connect to.
	if len(sys.argv) > 0:
		sys.exit("Not ready yet!")


if __name__ == "__main__":
	main()
