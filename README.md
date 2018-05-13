# TinyPwn
AsisCTF - Saos : https://github.com/VoidMercy/CTFs/blob/master/AsisCTF-2018/TinyPwn/README.md
"I did this problem at school, so I didn't have ida ```xD```. You'll have to bear with objdump."

Oke, soal memberi kita binary yang sudah di strip, coba kita checksec :
```
blaccmail@localhost:~/ROPgadget$ checksec TinyPwn 
[*] '/home/blaccmail/ROPgadget/TinyPwn'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
```

Karena binary ini di strip kita tidak dapat menggunakan gdb, maka ```objdump```  akan digunakan :
```
blaccmail@localhost:~/ROPgadget$ objdump -d TinyPwn 
TinyPwn:     file format elf64-x86-64
Disassembly of section .text:
00000000004000b0 <.text>:
  4000b0:	48 31 c0             	xor    %rax,%rax
  4000b3:	48 31 db             	xor    %rbx,%rbx
  4000b6:	48 31 c9             	xor    %rcx,%rcx
  4000b9:	48 31 d2             	xor    %rdx,%rdx
  4000bc:	48 31 ff             	xor    %rdi,%rdi
  4000bf:	48 31 f6             	xor    %rsi,%rsi
  4000c2:	4d 31 c0             	xor    %r8,%r8
  4000c5:	4d 31 c9             	xor    %r9,%r9
  4000c8:	4d 31 d2             	xor    %r10,%r10
  4000cb:	4d 31 db             	xor    %r11,%r11
  4000ce:	4d 31 e4             	xor    %r12,%r12
  4000d1:	4d 31 ed             	xor    %r13,%r13
  4000d4:	4d 31 f6             	xor    %r14,%r14
  4000d7:	4d 31 ff             	xor    %r15,%r15
  4000da:	48 31 ed             	xor    %rbp,%rbp
  4000dd:	e8 10 00 00 00       	callq  0x4000f2
  4000e2:	b8 3c 00 00 00       	mov    $0x3c,%eax
  4000e7:	48 31 ff             	xor    %rdi,%rdi
  4000ea:	48 31 f6             	xor    %rsi,%rsi
  4000ed:	48 31 d2             	xor    %rdx,%rdx
  4000f0:	0f 05                	syscall 
  4000f2:	48 81 ec 28 01 00 00 	sub    $0x128,%rsp
  4000f9:	48 89 e6             	mov    %rsp,%rsi
  4000fc:	ba 48 01 00 00       	mov    $0x148,%edx
  400101:	0f 05                	syscall 
  400103:	48 81 c4 28 01 00 00 	add    $0x128,%rsp
  40010a:	c3                   	retq  
```
kita temukan tampungan inputnya sebesar ```0x148``` kemudian dia akan menjalankan perintah ```syscall```, lalu ukuran padding sebesar ```0x128``` sebelum ```return```.Oke sekarang kita tahu jumlah payload untuk buffer oferflow namun program tidak memiliki function ```get_flag``` seperti soal - soal biasanya, lalu apa yang harus dilakukan ?. Terpaksa kita harus mendapatkan shell-nya sendiri.

Untuk mendapatkan shell kita dapat melakukan teknink ROP Chain. Teknik ini dapat digunakan dengan memanfaatkann potongan opcode dari program yang menggunakan perintah ```ret```(return) atau disebut juga dengan gadget. Untuk mencari gadget-gadget tersebut dapat menggunakan tool ROPgadget :
```
blaccmail@localhost:~/ROPgadget$ ROPgadget --binary TinyPwn
Gadgets information
============================================================
0x0000000000400108 : add byte ptr [rax], al ; ret
0x00000000004000ff : add byte ptr [rax], al ; syscall
0x0000000000400104 : add esp, 0x128 ; ret
0x0000000000400103 : add rsp, 0x128 ; ret
0x00000000004000e9 : dec dword ptr [rax + 0x31] ; test byte ptr [rax + 0x31], 0xd2 ; syscall
0x00000000004000fc : mov edx, 0x148 ; syscall
0x00000000004000fa : mov esi, esp ; mov edx, 0x148 ; syscall
0x00000000004000f9 : mov rsi, rsp ; mov edx, 0x148 ; syscall
0x000000000040010a : ret
0x0000000000400106 : sub byte ptr [rcx], al ; add byte ptr [rax], al ; ret
0x00000000004000f0 : syscall
0x00000000004000ec : test byte ptr [rax + 0x31], 0xd2 ; syscall
0x00000000004000e8 : xor edi, edi ; xor rsi, rsi ; xor rdx, rdx ; syscall
0x00000000004000ee : xor edx, edx ; syscall
0x00000000004000eb : xor esi, esi ; xor rdx, rdx ; syscall
0x00000000004000e7 : xor rdi, rdi ; xor rsi, rsi ; xor rdx, rdx ; syscall
0x00000000004000ed : xor rdx, rdx ; syscall
0x00000000004000ea : xor rsi, rsi ; xor rdx, rdx ; syscall
```
