section .text

global _start

_start:
    BITS 32
    jmp short two

one:
    pop ebx
    xor eax, eax

    ; place 0x00 in the *
    mov [ebx+12], al
    mov [ebx+17], al
    mov [ebx+22], al
    mov [ebx+23], al

    mov [ebx+24], ebx           ; save ebx in AAAA
    mov [ebx+28], eax           ; save 0x00000000 in BBBB
    lea ecx, [ebx+24]           ; argv[] address | exc points to argv[]

    ; for environment variables
    lea edx, [ebx+13]           ; loading address of "a=11" into edx 
    mov [ebx+32], edx           ; saving the address of "a=11" into CCCC
    lea edx, [ebx+18]
    mov [ebx+36], edx
    mov [ebx+40], eax           ; save 0x0000000 in EEEE
    lea edx, [ebx+32]           ; ecx points to env[]

    mov al, 0x0b
    int 0x80

two:
    call one
    db "/usr/bin/env*a=11*b=22**AAAABBBBCCCCDDDDEEEE"