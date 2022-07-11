; we need to construct an environment variable array on the stack
; and store the address of this array to edx before invoking execve()

; /usr/bin/env
; command to print environment variables

; env[3] = 0 end of the arry
; env[2] = address of "cccc=1234" string
; env[1] = address of "bbb=1234" string
; env[0] = address of "aaa=1234" string

section .text

global _start

_start:
    xor eax, eax

    push eax
    push "/env"
    push "/bin"
    push "/usr"
    mov ebx, esp

    ; construct the array argv[]
    push eax
    push ebx
    mov ecx, esp

    ; for env var
    push eax
    mov edx, "4###"
    shl edx, 24
    shr edx, 24
    push edx
    push "=123"
    push "cccc"
    mov edx, esp

    push eax
    push "5678"
    push "bbb="
    mov esi, esp

    push eax
    push "1234"
    push "aaa="
    mov edi, esp

    ; construct the array
    push eax
    push edx
    push esi
    push edi
    mov edx, esp

    ; invoke execve()
    xor eax, eax
    mov al, 0x0b
    int 0x80