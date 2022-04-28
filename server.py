import sys
import socket
import shared
import random
import threading
from shared import PacketType, receivePacket, send, receive

clients = {}

def handleClient(client, address):
	with client:
		print(client)
		# A client has connected, ask them for the number range they want.
		# It should still be within our predefined values in config.
		send(client, PacketType.ASK_CLIENT_MIN_MAX, shared.MIN_NUMBER, shared.MAX_NUMBER)

		#############################################################################################################################
		# The client has sent back the min and max they want.
		data = receivePacket(client, PacketType.GIVE_SERVER_MIN_MAX)
		# Verify what we got to be sure it fits our bounds. If not, kill the connection.
		if data[0] < shared.MIN_NUMBER or data[1] > shared.MAX_NUMBER:
			print("Client sent invalid min & max.")
			client.close()
		else:
			# They're valid.
			clients[client] = {
				"correctNumber": random.randint(data[0], data[1]),
				"minimum": data[0],
				"maximum": data[1],
				"guessHistory": []
			}
			print("Client {} chose {} and {} as their min & max.".format(client.fileno(), data[0], data[1]))
		
		# Tell them to start guessing.
		send(client, PacketType.START_GUESSING)
		#############################################################################################################################
		while True:
			# We should be receiving guesses now.
			data = receivePacket(client, PacketType.GUESS)
			if not data[0]:
				# Invalid response. Close the connection.
				client.close()
			
			clientData = clients[client]
			clientData["guessHistory"].append(data[0])

			if data[0] == clientData["correctNumber"]:
				print("They got it right! It only took {} guesses.".format(len(clientData["guessHistory"])))
				send(client, PacketType.GUESS_CORRECT)
				break
			elif data[0] < clientData["minimum"]:
				print("They sent a number below their previously defined minimum, despite safeguards. Kill the connection.")
				client.close()
			elif data[0] > clientData["maximum"]:
				print("They sent a number above their previously defined maximum, despite safeguards. Kill the connection.")
				client.close()
			else:
				# Incorrect guess.
				send(client, PacketType.GUESS_INCORRECT)


def doServer(server_port):
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

				threading.Thread(target = handleClient, args = (client,address)).start()

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
	doServer(server_port)


if __name__ == "__main__":
	main()
