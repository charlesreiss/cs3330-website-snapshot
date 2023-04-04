---
title: "Getting C/Unix"
...

{:.changelog}
Changelog:

{:.changelog}
*  24 August 2022: remove dead link to koding

This lab is optional. The lab rooms will not be staffed.
If you run into problems, use Piazza or office hours to get help.

For this class, we would suggest that you have access to a Unix-like environment where you can compile C code.

Assignments in this class will often use C.  C is very close to machine language without the headaches associated with assembly. We will distribute some tools written in C that we expect to compile and run relatively early in the semester, and later in the semester, we will have some assignments that require modifying C code.

In addition to using C, we generally assume a Unix-like environment for compiling and running the C code. Several assignments will be distributed with Makefiles, which require the Unix utility `make` and Unix-like command line to be available. In addition, for one assignment, we distribute an autograder tool which uses Python 3.

We have been developed and tested our assignments on a Linux-like environment similar to the lab machines. They may work in other environments, and in the past students have in fact had success, for example, using OS X or the Windows Subsystem for Linux for almost all assignments. (The first assignment (bomb lab/HW) is an exception; it will definitely not work on OS X without something like a VM.)

However, we do not have the staffpower to support arbitrary student systems. If the suggestions below fail for any reason, our official answer is <q>you may program on the lab machines instead.</q> It is on you to arrange access to those machines in order to complete your assignments. Excuses such as <q>my computer crashed</q> or <q>I had trouble installing the compiler</q> will not be accepted.

That said, we will sometimes provide suggestions for how a lab or homework could be done from your home machine. If those work for you, great. If they do not, <q>you may program on the lab machines instead.</q> If you have your own tip, post it on piazza so everyone can benefit.


# Suggested Techniques

Not all paths to C and a Unix-like environment are created equal, but there are a lot of paths.  We official support using the department machines (the first option below), but many students perfer other options:

1. **Program remotely on the department Unix machines.**  For how to do this from home, see [how to use remote desktop, `ssh` and `scp`](sshscp.html). These machines come with a version of `gcc` by default, but you can access a more recent C compiler by running `module load gcc` (for `gcc`) or `module load clang` (for `clang`). (See also [this guide to modules on the department machines](files/UVA_linux_environment_modules.pdf).)

    > Warning: Do not submit files by copy-paste from `ssh` terminals without looking at them first!  Copy-paste can introduce line breaks, backslashes, and so on where they do not belong.

2. Go native.  Install [a good Linux distro](http://www.linuxmint.com/edition.php?id=188), or make do with [C and a Unix-like environment on other OSs](ownc.html)

3. Use virtualization, such as virtualbox.  Note, you'll need a 64-bit image of Linux, like the one 2150 has used recently.  Virtualization occasionally messes up timing, so it might not be good for the last part of the course, but it should hold you over until then.

4. Use an online IDE; [Cloud9](https://c9.io/) have in prior semesters worked for this course (but may be a bit slow for the performance assignments); [codio](http://codio.com), [ideone](http://ideone.com/), and [ShiftEdit](https://shiftedit.net/education) might as well.  One bit of setup, though: once you log in and open a project in one of these online IDEs, get a terminal and type

        sudo apt-get update
        sudo apt-get install xdg-utils libc6-dev-i386 gcc-multilib make

# C command line


C files can be compiled on any Linux system using `gcc -x c filename.c`, `clang -x c filename.c`, or `llvm-gcc -x c filename.c`. Most systems will have only one of these three installed; it does not matter which one you use.

If you have no `main` method or otherwise want to produce an object file instead of a final executable, add `-c` to the command line.

## Recent compilers on the department machines

On the department machines, the default `gcc` is pretty old, but you can get access to more recent one by running `module load gcc`. Similarly, a recent verison of `clang` is available with `module load clang`.

# 2150's Unix Tutorial

You might refer to [CS 2150's Unix tutorial](https://uva-cs.github.io/pdr/tutorials/01-intro-unix/index.html)
for information about how to use Unix. Alternatively, we provide an extremeley brief introduction below.

This tutorial includes instructions for using the native Unix enviornment on OS X in addition to
more Linux-like environments. As noted above, we need a x86-64 Linux environment for certain assignments,
including the first one (bomb lab/HW). So, although the native OS X environment may be most convenient for
future assignments, if you are using OS X, I would recommend following the tutorial on the
department machines (via SSH or NX; first option on "suggested techniques" above).

# Linux Lite

We assume you'll use Linux for the labs in this course.

Upon logging into Linux, assuming you're logging in via graphical interface (such as through NX), you'll want access to

1. A terminal window
2. An editor of some kind
3. A web browser

I suggest getting the terminal first by pressing Alt-F2 and typing `gnome-terminal`, `konsole`, or `xterm` (they may not all work, but at least one should).

You can then get an editor by typing into the terminal one of `geany &`, `gedit &`, `kate &`, `nano`, `pico`, `emacs`, or `vim` (or others, if you know others); and you can get a browser with `firefox &` or `chromium-browser &`. The `&` means "Run this in the background and let me type other stuff in the terminal while it is running".

Other important commands you can use in the terminal:

- `pwd` tells you where you are currently in the file system
- `ls` tells you what files are in the current folder
- `mkdir` makes a new directory
- `cd ..` go one spot higher in the directory tree (if you are in `/home/mst3k/funbox/whee/` then `cd ..` will move you to `/home/mst3k/funbox/`)
- `cd dirname` to enter directory dirname (if you are in `/home/mst3k/funbox/` then `cd whee` will move you to `/home/mst3k/funbox/whee/`)
- The Tab key will autocomplete what you are typing; pressing it twice will list all possible autocompletions.  For example, instead of typing `/home/mst3k/funbox/whee/` I can probably type `/h`Tab`m`Tab`fu`Tab`wh`Tab.  This not only saves typing, it reduces the chances of typos.

## Linux Lite with SSH
If you login into Linux via [SSH](sshscp.html) instead of via a graphical interface,
you won't have to do any work to get a terminal, but that's all you'll have.

You won't be able to (usefully) run a web browser on the remote machine; instead, you'll probably using a web browser on
your local (non-Linux) machine and transferring files using our instructions on SCP.

However, you'll still be able to take advantage of the above advice regarding using the terminal
and finding text editors (though you won't be able to use any of the text editors you'd run in the background).

# Testing your compiler

If you think you have a compiler properly installed,

1. create `hello.c` from Figure 1.1 on page 2 of the textbook (or [here](http://csapp.cs.cmu.edu/3e/ics3/code/intro/hello.c))
2. compile it as described in &sect;1.2, and 
3. run it as described in &sect;1.4

