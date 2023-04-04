---
title: "Bomb Lab"
...

# Introduction

A Mad Programmer got really mad and planted a slew of “binary bombs” on our class machines. A binary bomb is a program that consists of a sequence of phases. Each phase expects you to type a particular string on `stdin`. If you type the correct string, then the phase is *defused* and the bomb proceeds to the next phase. Otherwise, the bomb *explodes* by printing `"BOOM!!!"` and then terminating. The bomb is defused when every phase has been defused.

There are too many bombs for us to deal with, so we are giving each student a bomb to defuse. Your mission is to defuse your bomb before the due date.  Good luck, and welcome to the bomb squad!

# Your task 

*  Obtain a "binary bomb" as [described below](#get-bomb).
    *  Note that this program will automatically communicate with our server. This is how you will be graded.
    *  If your bomb "explodes", it will notify our server. Too many explosions will lose you points.

*  The bomb program will ask you you for a secret input. 

*  Defuse the "phases" of the bomb by figuring out (e.g. using a debugger) what the secret input for each "phase" is.
   (You will **not** get credit for using the debugger to jump over the code that checks whether input is valid;
    the bomb must send a correct input to our server.)

*  **For lab**: defuse phase 1.
    *  You will get full credit for defusing phase 1 with less than 20 explosions.
    *  There is a small grade penalty for explosions beyond 20.

*  **For homework**: defuse phases 2 and 3.
    *  You will get full credit for defusing phases 2 and 3 with less than 30 explosions.
    *  There is a small grade penalty for explosions beyond 30.
    *  There is a very small amount of extra credit for each additional phase defused.

## Submission

There is no explicit submission. The bomb will notify your instructor automatically about your progress as you work on it.

## Viewing your results

You can see your grade, updated with about a 1-hour delay on the [submission site]({{site.submit_site}}){:target="_top"} under the [bomblab]({{site.submit_site}}/task.php?task=bomblab) and [bombhw]({{site.submit_site}}/task.php?task=bombhw) tasks.

There is scoreboard showing how many explosions and phases defused all bombs have [here](http://{{site.kytos}}:15213/scoreboard),
which is updated more frequently.

## About Collaboration

For phase 1, anything goes.  Being a lab, you can work together as much as you want.

For phases 2 and beyond, it is homework so more restrictions apply.
You are welcome to discuss with one another the process and tools you use, but please do not look at or describe one another's code.

{: #get-bomb}
# Obtaining your bomb

0.  Use Linux.

    This lab only works on 64-bit Linux machines.
    The department Unix machines qualify; see [these instructions](sshscp.html) if you need help accessing them remotely.

1.  You can obtain your bomb by pointing your Web browser at:

    <center>
    <a href="http://kytos02.cs.virginia.edu:15213/">http://kytos02.cs.virginia.edu:15213/</a>
    </center>

    This will display a binary bomb request form for you to fill in. Enter your computing ID and email address and hit the Submit button. The server will build your bomb and return it to your browser in a `tar` file called `bombk.tar`, where `k` is the unique number of your bomb.

    Save the `bombk.tar` file to a (protected) directory in which you plan to do your work. Then give the command: `tar -xvf bombk.tar`. This will create a directory called `./bombk` with the following files:

    -   `README`: Identifies the bomb and its owners.
    -   `bomb`: The executable binary bomb.
    -   `bomb.c`: Source file with the bomb's main routine and a mad greeting from the Mad Mad Programmer.

    If for some reason you request multiple bombs, this is not a problem. Choose one bomb to work on and delete the rest.

## Getting a bombs from ssh

If you are trying to do the lab without a browser on the machine being used, try the following:

~~~~bash
curl "http://kytos02.cs.virginia.edu:15213/?username=$USER&usermail=$USER@virginia.edu&submit=Submit" > bomb.tar
mv bomb.tar $(head -1 bomb.tar | cut -d'/' -f1).tar
~~~~

Note, this might fail if the remote machine you run it on is not a department machine because `$USER` might not be set correctly by other machines.  Replace `$USER` with your computing ID if you are running this command e.g. in cloud9, koding, or codio.

# Hints

## Basic Strategy

*  The best way is to use your favorite debugger to step through the disassembled binary. **Almost no students succeed without using a debugger like gdb or lldb.**  On the department Unix machines, `gdb` is the debugger that is available. By default GDB verison 7.3 is available, and you can use GDB version 8 by running `module load gdb-8.1` then running `gdb`. You will need to run this `module load` command in each new terminal (the setting will not persist).

*   Try running `objdump -t bomb`. This will show you the symbols in the executable, including the names of all methods. Look for one that looks dangerous, as well as some that looks like interesting methods (perhaps something like "Phase 1").

*  To avoid accidentally detonating the bomb, you will need to learn how to single-step through the assembly code and how to set breakpoints. You will also need to learn how to inspect both the registers and the memory states.

*  It may be helpful to use various utilities for examining the bomb program outside a debugger, as described in "examining the executable" below.

*  Although you may be able to defuse the first phase without looking at assembly, you probably won't be able to avoid this for subsequent phases.

## Bomb Usage

*  The bomb ignores blank input lines.

*  If you run your bomb with a command line argument, for example,

        linux> ./bomb psol.txt

    then it will read the input lines from `psol.txt` until it reaches EOF (end of file), and then switch over to `stdin`. This will keep you from having re-type solutions.

## Examining the Executable

*  `objdump -t`  will print out the bomb's symbol table. The symbol table includes the names of all functions and global variables in the bomb, the names of all the functions the bomb calls, and their addresses. You may learn something by looking at the function names!

*  `objdump -d` will disassemble all of the code in the bomb. You can also just look at individual functions. Reading the assembler code can tell you how the bomb works.

   If you prefer to get Intel syntax disassembly from `objdump`, you can use `objdump -M intel -d`.

*  `strings` is a utility which will display the printable strings in your bomb.

## Using GDB

-   If you are on a department Unix machine, `module load gdb-8.1` first (this needs to be done once per terminal), so `gdb` is the most recent available version of GDB. (By default you will get GDB 7.3.)

-   Run bomb from a debugger like gdb instead of running it directly. The debugger will allow you to stop the bomb before it detonates.

    For example, if I ran
    
        linux> gdb bomb
        (gdb) b methodName
        (gdb) run
        (gdb) kill
    
    this will start `gdb`, set a **breakpoint** at `methodName`, and run the code. The code will halt *before* it runs `methodName`; calling `kill` will stop the bomb and exit the current debugging session without `methodName` running.

-   Use “step” and “stepi” to examine this function. “step” runs your code one line of **source code** at a time. “stepi” runs your code one line of **machine instruction** at a time. This allows you to run “phase_1()” piece by piece.

-   Use this to step *carefully* through `phase_1()` to see if you can find the passphrase.

        linux> gdb bomb
        (gdb) b lineNumberForPhase1Call
        (gdb) run

    *input test passphrase here*

        (gdb) stepi
        (gdb) info registers

    *Generally some parameters are stored in local variables in registers or on the stack. You should be able to find something that points to your test passphrase here
    (but it may take some work to extract the text, see also the gdb commands below).*
    Ordinarily when you are debugging, `info locals` would also be useful for getting information about local variables, but our `bomb` executables are compiled without debugging information (the `-g` option);
    fortunately, however, you can still find the values of local variables in registers or on the stack, and use these to retrieve any corresponding values in memory.

        (gdb) stepi

    *If you want to see the assembly code you're stepping through, use "disas methodName".*

    *keep `stepi`ing until you see `strings_not_equal` method (a suspicious name that might be checking your passphrase)*

        (gdb) info locals
        (gdb) info registers

    *Which one holds your passphase? Try "examining" that and others...*


-   Some useful `gdb` commands:

    `(gdb) info locals`
    :   prints out the name and value of local variables in scope at your current place in the code. Requires the application to have compiled with debugging information available (`-g` option with most compilers).

    `(gdb) info registers`
    :   prints the values of all registers except floating-point and vector registers

    `(gdb) x/20bx 0x...`
    :   examine the values of the 20 bytes of memory stored at the specified memory address (0x...). Displays it in hexadecimal bytes.

    `(gdb) x/20bd 0x...`
    :   examine the values of the 20 bytes of memory stored at the specified memory address (0x...). Displays it in decimal bytes.

    `(gdb) x/gx 0x...`
    :   examine the value of the 8-byte integer stored at the specified memory address.

    `(gdb) x/s 0x...`
    :   examines the value stored at the specified memory address. Displays the value as a string.

    <code>(gdb) x/s $<i>someRegister</i></code>
    :   examines the value at register someRegister (where someRegister is a name like `rax`). Displays the value as a string (assuming the register contains a pointer).

    <code>(gdb) p $<i>someRegister</i></code>
    :   examines the value at register someRegister. Displays the value as an base-10 integer.

    <code>(gdb) p/x $<i>someRegister</i></code>
    :   examines the value at register someRegister. Displays the value as an base-16 integer.

    `(gdb) print expr`
    :   evaluates and prints the value of the given expression

    `(gdb) call (void) puts (0x...)`
    :   calls the built-in output method `puts` with the given `char *` (as a memory address).  See `man puts` for more.

    <code>(gdb) disas <i>methodName</i><code>
    :   gives you the to get the machine instruction translation of the method `methodName`. (If you see a `call` instruction in this output that does not indicate what function it refers to, if on the department machines, make sure you are using gdb version 8.1.)

    `(gdb) disas`
    :   gives you the to get the machine instruction translation of the currently executing method.

    `(gdb) x/6i 0x...`
    :   try to disassemble 6 instructions in memory starting at the memory address 0x...

    `(gdb) set disassembly-flavor intel`
    :   switches GDB to Intel syntax disassembly (the syntax you used in 2150; not the syntax we will use for the rest of the course)

    `(gdb) set disassembly-flavor att`
    :   switches GDB back to AT&T syntax disassembly, the default and the syntax we will use for the rest of the course

    `(gdb) b *0x...`
    :   set a breakpoint at the specified memory address (0x...).

    <tt>(gdb) b <i>function_name</i></tt>
    :   set a breakpoint at the beginning of the specificed function.

    `(gdb) nexti`
    :   step forward by one instruction, skipping any called function.

    `(gdb) kill`
    :   termiante the program immediately

    `(gdb) help`
    :   brings up gdb's built-in help menu

    The textbook also has a nice summary of useful gdb commands on page 280 (or 255 of the 2nd edition). You can also find sources like [this one from the textbook authors](http://csapp.cs.cmu.edu/2e/docs/gdbnotes-x86-64.txt) that list and describe other useful gdb commands. 

## On interpreting the disassembly

-   Reviewing the x86-64 calling convention (Figure 3.28 in the textbook or [this reference you may remember from 2150](https://aaronbloomfield.github.io/pdr/book/x86-64bit-ccc-chapter.pdf)) may be helpful. Using
    this you can find the values of function argument and return values from the assembler and/or debugger.

-   Pay attention to the names of functions being called.

-   Disassembling a standard library function instead of reading the documentation for the function is probably a poor use of time.

-   The C standard library function `sscanf` is called `__isoc99_sscanf` in the executable. sscanf's documentation (for example, obtained [here](https://en.cppreference.com/w/c/io/fscanf) or by typing "`man sscanf`") may be helpful. `sscanf` parses a string based on a "format" specified similarly to how one specifies values to output with `printf`.

-  `%fs:0x1234` refers to a value in a "[thread-local storage](https://en.wikipedia.org/wiki/Thread-local_storage)" region at offset `0x1234`. The bomb only has one thread (using multiple threads would allow the bomb to do multiple things at once, but that is not something the bomb needs), so this is effectively a region for extra global variables. In the bomb, this appears mostly to implement [stack canaries](https://en.wikipedia.org/wiki/Stack_buffer_overflow#Stack_canaries), a security feature designed to cause out-of-bounds accesses to arrays on the stack to more consistently trigger a crash.

-   `endbr64` is basically a nop and `notrack jmp` and `notrack call` (sometimes written `ds jmp` or `ds call`) are basically the same as `jmp` and `call` respectively. Recent x86 processors support a mode where `jmp`s and `call`s need to go to an instruction that's marked as safe to jump to with something like `endbr64`. The `notrack` prefix disables this checking.


-   Some of the things later phases might be using include:

*  linked data structure traversal
*  recursion
*  string literals
*  `switch` statements

