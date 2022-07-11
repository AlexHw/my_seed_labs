; Author: Alex
;
; /bin/sh -c "ls -la"
;
; argv[3] = 0
; argv[2] = "ls -la"
; argv[1] = "-c"
; argv[0] = "/bin/sh"

section .text

global _start

_start:
    xor eax, eax
    
    push eax        ; 0 to terminate the string
    push "//sh"
    push "/bin"
    mov ebx, esp    ; get the string address

    push eax
    mov edx, "-c##"
    shl edx, 16
    shr edx, 16
    push edx
    mov edx, esp

    push eax
    mov ecx, "la##"
    shl ecx, 16
    shr ecx, 16
    push ecx
    push "ls -"
    mov ecx, esp

    ; -----------------------------------
    ; construct the argument array argv[]           | ___ stack ___ |
    push eax        ; argv[3] -> 0                  | /bin/sh --- 0 |
    push ecx        ; argv[2] -> "ls -la"           | -c      --- 0 |
    push edx        ; argv[1] -> "-c"               | ls -la  --- 0 |
    push ebx        ; argv[0] -> "/bin/sh"          | 000     --- 0 |
    mov ecx, esp    ; get the address of argv[]

    ; for the environment variable
    xor edx, edx

    xor eax, eax
    mov al, 0x0b
    int 0x80