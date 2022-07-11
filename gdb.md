# GDB

## run & start

Run the program:
- run (r)
- r my_argument
- r < input

The *start* command does the equivalent of setting a temporary breakpoint at the beginning of the main procedure and then invoking the ‘run’ command. 
- start

Runs until the current function is finished:
- finish

- bt

- quit (q)

## breakpoints

Put a breakpoint:
- break my_func
- break * 0x0804840c
- info breakpoints

You can proceed onto the next breakpoint:
- continue

Execute just the next line of code:
- step

Delete a specific breakpoint:
- delete (d)

Similar to *step*,” the *next* command single-steps as well, except this one doesn’t execute each line of a sub-routine, it just treats it as one instruction:
- n (next)
- ni

## print & examine

- print $register
- print my_var
- print &my_function
- print/x my_var

Print value of a variable:
- p info
- p option

Whenever my var’s value is modified, the program will interrupt and print out the old and new values:
- watch my_var

Displays the memory contents at a given address using the specified format:
[To see more about x](https://visualgdb.com/gdbreference/commands/x).
- x address [examine]
- x/s address [see content of an address in string format]
- x/wx $ebp - 8
- x/4xw $sp [4 words ]
- x/20x $sp

## utilities

- info functions
- info frame [show stack frame info]
- info proc map

- set disassembly-flavor intel
- disassemble main
- disas main

- catch syscall write

- dump binary memory file.dump 0xmem 0xmem

- canary

## hooks

Define hooks to print at breakpoints. These hooks run the commands defined in them at every breakpoint:
> define hook-stop 
> > info registers
> > x/24wx $esp
> > x/2i $eip
> > end 

## batch mode

First put commands into a text file and then run:
> gdb -q -batch -x gdb_command.txt ./retlib

## Tips:

- Typing “step” or “next” a lot of times can be tedious. If you just press ENTER, gdb will repeat the same command you just gave it.
