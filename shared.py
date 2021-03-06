#########################################
# Imports
#########################################
import sys
from enum import Enum, unique, auto
import json

#########################################
# Shared Constants
#########################################
MAX_CONNECTIONS = 10
SERVER_IP = "127.0.0.1"
# Minimum number that can be generated. Hard cap.
MIN_NUMBER = 0 
# Maximum number that can be generated. Hard cap.
MAX_NUMBER = 100
MAX_PACKET_SIZE = 1024

#########################################
# Packet enum
#########################################
@unique
class PacketType(Enum):
	NONE = auto()
	ASK_CLIENT_MIN_MAX = auto()
	GIVE_SERVER_MIN_MAX = auto()
	START_GUESSING = auto()
	GUESS = auto()
	GUESS_INCORRECT = auto()
	GUESS_CORRECT = auto()


#########################################
# Methods
#########################################
def receive(skt):
	data = b""
	while True:
		got = skt.recv(MAX_PACKET_SIZE)
		if got == b"":
			break
		elif got[-1] == 0:
			#print("null check")
			data += got[:-1]
			break
		else:
			data += got
	
	if (data == b""):
		print("Got empty data.")
		return PacketType.NONE, []
	
	#print("receiving:", data)
	data = json.loads(data)
	packet = data["packet"]

	try:
		packet = PacketType(packet)
	except (ValueError):
		print("-----------------------------------------")
		print("Received unknown packet!")
		print(data)
		sys.exit(1)
	
	return packet, data["args"]


def receivePacket(skt, expected_packet):
	packet, data = receive(skt)
	if packet != expected_packet:
		print("-----------------------------------------")
		print(packet)
		print(data)
		raise RuntimeError("Received incorrect packet!")

	return data


def send(skt, packet, *args):
	data = {
		"packet": packet.value,
		"args": list(args)
	}
	data = json.dumps(data)

	skt.sendall(bytes(data, "utf-8"))
	skt.sendall(b"\x00")