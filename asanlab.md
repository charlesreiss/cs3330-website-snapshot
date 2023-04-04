---
title: Memory Safety Lab
---

# Memory Safety Lab

In this lab, you will diagnose and fix memory errors in a simple program.
To do this, we will be using a debugging tool intended to help identify
memory errors. This tool is built-in into the C compiler you can use after
running `module load gcc` on the lab machines. It is also usually included in
recent versions of `gcc` or `clang`.


# Your Task

1.  Download [asanlab.tar](files/asanlab.tar) and extract it. 
    This contains an example broken implementation of a circular
    doubly-linked list library and a test program for it.

2.  If you are on a department machine, run `module load gcc` before
    running any of the commands below, to use aa sufficiently recent
    version of GCC.

2.  Run `make` in the root directory the given program.

3.  Run `make test` to run our test program under a memory error
    detector called AddressSanitizer.

4.  Modify `ll.c` so `make test` reports **no errors**. (This includes
    errors from the test program itself **and** from AddressSanitizer.)

5.  Submit your fixed `ll.c` to [the submission site]({{site.submit_site}}){:target="_top"}.
    You may work with other students in your lab, but each student must
    submit an `ll.c`.

# Troubleshooting

1. If you run into trouble with *not getting line numbers in stack traces*,
    ***try doing the lab on a department machine***, such by [SSH'ing](sshscp.html),
    and running `module load gcc`, then `make clean` followed by `make` to
    force everything to be recompiled
    and linked on those machines.

2. If you get an error like `/usr/bin/ld: cannot find /usr/lib64/libasan.so.0.0.0`,
   and you're logged into portal or nxfront, run `module load gcc`, then `make clean`,
   then try again.

# Hints

## Files in the Archive

*  `ll.c` and `ll.h` are the linked list implementation. `ll.h` describes
   what each of the given functions are supposed to do.

*  `ll-test.c` contains a testing program that we run.

*  After running `make`, `ll-test-sanitize` is the test program built against
   the debugging tool called [AddressSanitizer](https://github.com/google/sanitizers/wiki/AddressSanitizer). This is what `make test` runs.
   
*  After running `make`, `ll-test` is a version of the test program built
   without using AddressSanitizer. It will
   run faster than  `ll-test-sanitize`, but some errors may not cause
   tests to consistently fail.

## Understanding AddressSanitizer

*  AddressSanitizer is a tool for helping programmers diagnose memory errors.
   It is a combination of a compiler extension and a runtime library.

   Using this, AddressSanitizer tracks what memory in a program is valid
   and checks every single memory read and write to make sure it only
   accesses valid memory.

### The Shadow Memory

*  AddressSanitizer works by maintaining a "shadow memory". This is a data
   structure which indicates the status of **every byte** of memory
   allocated by the program. The shadow memory is an array with one
   byte for every 8 bytes of normal memory.
   
   For every 8 bytes of normal memory, the correspondoning byte of the
   shadow memory is 0 if the memory is addressable (legal to access)
   and has another value otherwise.

*  In order to detect out-of-bounds accesses AddressSanitizer ensures
   that there is a "redzone" before and after variables in memory.
   These "redzones" have invalid status in the shadow memory.

### Interpreting Output

#### Invalid reads and writes 

*  Typical output from AddressSanitizer includes two stack traces, which have the most important information:
    
        ==12270==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000f000 at pc 0x7f66d0f09709 bp 0x7ffd854ca110 sp 0x7ffd854c98b8
        WRITE of size 17 at 0x60200000f000 thread T0
            #0 0x7f66d0f09708  (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x62708)
            #1 0x400e6b in strcpy /usr/include/x86_64-linux-gnu/bits/string3.h:110
            #2 0x400e6b in ll_add_after /home/cr4bd/cs3330-site/asanlab/ll.c:34
            #3 0x40169f in singleton_list_test /home/cr4bd/cs3330-site/asanlab/ll-test.c:61
            #4 0x402174 in main /home/cr4bd/cs3330-site/asanlab/ll-test.c:133
            #5 0x7f66d0afe82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)
            #6 0x400bf8 in _start (/home/cr4bd/cs3330-site/asanlab/ll-test-sanitize+0x400bf8)

        0x60200000f000 is located 0 bytes to the right of 16-byte region [0x60200000eff0,0x60200000f000)
        allocated by thread T0 here:
            #0 0x7f66d0f3f602 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98602)
            #1 0x400e2f in ll_add_after /home/cr4bd/cs3330-site/asanlab/ll.c:32
            #2 0x40169f in singleton_list_test /home/cr4bd/cs3330-site/asanlab/ll-test.c:61
            #3 0x402174 in main /home/cr4bd/cs3330-site/asanlab/ll-test.c:133
            #4 0x7f66d0afe82f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

*  If you don't see line any numbers in your stack traces, try using a lab machine (e.g. via SSH) instead.

*  The first stack trace is ***where the invalid memory access happened***. In the example above, this was a write inside `strcpy`.
   This stack trace is ***usually the more important one***.

*  The second stack trace is ***where the object whose bounds were exceeded was allocated***.
   In the above example, this was a call to `malloc` at line 32 of `ll.c` in the function `ll_add_after`.
   The invalid write in this case was "0 bytes to the right" --- that is, just after the end of this 16-byte memory allocation.

*  Typical output from AddressSanitizer also includes the values in the "shadow memory" around the allocation.
   ***Usually this "shadow memory" information is not particularly useful.***

*  The locations specified in the stack traces ***may not be the right location to fix every problem***.
   For example, if the bounds of an array are exceeded, you need to figure out whether the initial allocation is wrong
   or whether the size was changed without it being reallocated.

#### Memory leaks 

*  AddressSanitizer also reports memory leaks, where memory is allocated and never freed. In this case, AddressSanitizer will only
   be able to provide one stack trace, where the memory was allocated:
        
        ==23580==ERROR: LeakSanitizer: detected memory leaks

        Direct leak of 24 byte(s) in 1 object(s) allocated from:
            #0 0x7f6499eb4602 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98602)
            #1 0x400e65 in ll_new /home/cr4bd/cs3330-site/asanlab/ll.c:16
            #2 0x4012de in ll_copy_list /home/cr4bd/cs3330-site/asanlab/ll.c:75
            #3 0x401b84 in replace_add_test /home/cr4bd/cs3330-site/asanlab/ll-test.c:81
            #4 0x402353 in main /home/cr4bd/cs3330-site/asanlab/ll-test.c:138
            #5 0x7f6499a7382f in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x2082f)

*  To fix a memory leak, you need to figure out where the memory should be freed. This will **almost never** be where it is allocated.
    
## General debugging advice

*  We recommend working from the **first** AddressSanitizer message and fixing it, and repeating this process until you eliminate all errors.

*  You are welcome to add `printf` statements or use a debugger to figure out what is going on when test program runs. (Your submission, however, must work with an **unmodified** version of `ll.h` and `ll-test.c`)
