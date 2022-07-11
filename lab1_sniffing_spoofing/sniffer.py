#!/usr/bin/env python3
from scapy.all import *
IFACE = "br-5de3b839fd4f"  # set here the interface of docker
SPOOFED_IP = "10.9.0.5"
VERBOSE=0

def print_pkt(pkt):
    pkt.show()

def send_spoofed_icmp(ip=SPOOFED_IP):
    a = IP()
    a.dst=ip
    # a.src="10.9.0.6"
    p = a/ICMP()
    send(p)

"""
    Task 1.3: traceroute
"""
def traceroute(ip=SPOOFED_IP):
    TTL = 1
    print(f"Traceroute to {ip}...")
    while(TTL<255):
        response = sr1(IP(dst=ip, ttl=TTL)/ICMP(), iface=IFACE, verbose=VERBOSE)
        if response[0].src != ip:
            print(f"\t{TTL} ({response[0].src})")
            TTL += 1
        else:
            print(f"\t{TTL} ({response[0].src})")
            print("Done!")
            return 
    print("Error")


"""
    Task 1.4: spoof responses to every ping request
"""
def _send_icmp(pkt):
    if pkt[ICMP].type != 0:
        send(IP(src=pkt[IP].dst, dst=pkt[IP].src)
            /ICMP(type=0, code=pkt[ICMP].code, id=pkt[ICMP].id, seq=pkt[ICMP].seq)
            /pkt[Raw], verbose=VERBOSE)                
        print(f"Spoofed response for {pkt[IP].dst}")

def sniff_and_then_spoof():
    print("CTRL+C to stop!")
    sniff(iface=IFACE, filter="icmp", prn=_send_icmp)


if __name__ == "__main__":
    #pkt = sniff(iface=IFACE, filter="icmp", prn=print_pkt)

    #send_spoofed_icmp()

    #traceroute("8.8.8.8")

    sniff_and_then_spoof()
    
    
    
