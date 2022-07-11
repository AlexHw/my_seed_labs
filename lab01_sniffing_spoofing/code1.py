# Run interactive shell

from scapy.all import sniff, IP, ICMP, send

def print_pkt(pkt):
    pkt.show()
    #pkt.summary()

#iface=['eth0','wlan0']
pkt = sniff(iface='br-fdf474324adb', filter='icmp', prn=print_pkt)

sniff(iface='br-9d134d542608', filter="tcp and src host 10.9.0.6 and dst port 23")

#############################################################
 
a = sniff(iface='br-9d134d542608', filter="icmp and host 10.9.0.6", count=10)
#a = _
a.nsummary()
a[1]

############################################################

ip = IP()
IP.show() # or ls(IP)
ip.src = 'something'
ip.dst = '10.0.0.1'
icmp = ip/ICMP()
send(icmp)

# send() function will send packets at level 3.
# sendp() function will work at level 2.

# =====================
# Task 1.3 - traceroute
# =====================

count = 0
def trigger(pkt):
    global count 
    #if pkt[0][2].type == 0: # echo reply
    if str(pkt.getlayer(ICMP).type) == "0": 
        print(count)
        exit()
    else:
        count = count +1 
        ip = IP()
        ip.dst = '8.8.8.8'
        ip.ttl = count
        send(ip/ICMP())

#pkt = sniff(iface='wlo1', filter="icmp", prn=trigger)

ip = IP()
ip.dst = '8.8.8.8'
ip.ttl = 0
send(ip/ICMP())

# Other way
"""
def jump(ttl):
    a = IP()
    a.dst = '8.8.8.8'
    a.ttl = ttl
    a = se1(a/ICMP())
    print("Source:", a.src)
"""