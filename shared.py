import sys
from enum import Enum, unique, auto
import json

MAX_CONNECTIONS = 10
SERVER_IP = "127.0.0.1"
# Minimum number that can be generated. Hard cap.
MIN_NUMBER = 0 
# Maximum number that can be generated. Hard cap.
MAX_NUMBER = 100
MAX_PACKET_SIZE = 1024

@unique
class PacketType(Enum):
	#NONE = auto()
	ASK_CLIENT_MIN_MAX = auto()


def receive(skt):
	data = b""
	while True:
		got = skt.recv(MAX_PACKET_SIZE)
		if got == b"":
			break
		data += got

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


def send(skt, packet, *args):
	data = {
		"packet": packet.value,
		"args": list(args)
	}
	skt.sendall(bytes(json.dumps(data), "utf-8"))