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
