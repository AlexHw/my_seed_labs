######################
# TASK 1.4
######################


from scapy.all import IP, ICMP, Raw, send, sniff

def trigger(pkt):
    if str(pkt.getlayer(ICMP).type) == "8": 
        print("It's an echo request")
        #pkt.show()
        ip = IP(src=pkt[IP].dst, dst=pkt[IP].src)
        icmp = ICMP(type=0, id=pkt[ICMP].id, seq=pkt[ICMP].seq)
        data = pkt[Raw].load
        send(ip/icmp/data)

pkt = sniff(iface='br-fdf474324adb', filter="icmp and src host 10.9.0.5", prn=trigger)
