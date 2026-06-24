import socket

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)

DEFAULT_BUFFER_SIZE = 2048
DEFAULT_DECODE_FORMAT = "utf-8"

CERTIFICATE = "cert.pem"
KEY = "key.pem"

# Sniffer
INTERFACE = 'lo'
TIMEOUT_MS = 1000
PACKET_LEN = 65536