import socket
import struct
from uuid import getnode as get_mac
from random import randint

def macByte():
    mac = f"{get_mac():012x}"
    return bytes.fromhex(mac)

class DHCPDiscover:
    def __init__(self):
        self.transaction_id = bytes([randint(0, 255) for _ in range(4)])

    def build_packet(self):
        bigMAC = macByte()
        packet = (
            b'\x01\x01\x06\x00' + self.transaction_id +
            b'\x00\x00\x80\x00' + b'\x00\x00\x00\x00' * 4 +
            bigMAC + b'\x00' * 10 + b'\x00' * 192 +
            b'\x63\x82\x53\x63\x35\x01\x01\x3d\x06' + bigMAC +
            b'\x37\x03\x03\x01\x06\xff'
        )
        return packet

class DHCPOffer:
    def __init__(self, data, trans_id):
        self.data = data
        self.trans_id = trans_id
        self.offer_ip = ''
        self.next_server_ip = ''
        self.dhcp_server_id = ''
        self.lease_time = ''
        self.router = ''
        self.subnet_mask = ''
        self.dns = []
        self.unpack()

    def unpack(self):
        if self.data[4:8] == self.trans_id:
            self.offer_ip = '.'.join(map(str, self.data[16:20]))
            self.next_server_ip = '.'.join(map(str, self.data[20:24]))
            self.dhcp_server_id = '.'.join(map(str, self.data[245:249]))
            self.lease_time = str(struct.unpack('!L', self.data[251:255])[0])
            self.router = '.'.join(map(str, self.data[257:261]))
            self.subnet_mask = '.'.join(map(str, self.data[263:267]))
            dns_count = self.data[268] // 4
            self.dns = ['.'.join(map(str, self.data[i:i + 4])) for i in range(269, 269 + 4 * dns_count, 4)]

    def print_offer(self):
        key_val = [
            ('DHCP Server', self.dhcp_server_id),
            ('Offered IP address', self.offer_ip),
            ('subnet mask', self.subnet_mask),
            ('lease time (s)', self.lease_time),
            ('default gateway', self.router),
        ]
        for key, value in key_val:
            print(f"{key:20s} : {value:15s}")

        print('DNS Servers         :', end=' ')
        if self.dns:
            print(f"{self.dns[0]:15s}")
            for dns in self.dns[1:]:
                print(f"{' ':22s}{dns:15s}")

if __name__ == '__main__':
    dhcps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dhcps.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        dhcps.bind(('', 68))
    except Exception:
        print('port 68 in use...')
        dhcps.close()
        input('press any key to quit...')
        exit()

    discover_packet = DHCPDiscover()
    dhcps.sendto(discover_packet.build_packet(), ('<broadcast>', 67))
    print('DHCP Discover sent waiting for reply...\n')

    dhcps.settimeout(3)
    try:
        while True:
            data = dhcps.recv(1024)
            offer = DHCPOffer(data, discover_packet.transaction_id)
            if offer.offer_ip:
                offer.print_offer()
                break
    except socket.timeout as e:
        print(e)

    dhcps.close()

    input('press any key to quit...')
    exit()