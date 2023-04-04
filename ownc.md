---
title: "Lab 0.1 (native compilers)"
...

# C compilers and Unix-like environments

## Linux

C files can be compiled on any Linux system using `gcc -x c filename.c`, `clang -x c filename.c`, or `llvm-gcc -x c filename.c`. Most systems will have only one of these three installed; it does not matter which one you use. Makefiles we distribute may sometimes assume `gcc`, but you ought to be able to edit them if necessary.

If you have a C compiler installed on Linux, you very likely have other important build tools like `make` also installed. If not, many Linux distributions have a `build-essential` or similarly named package you can install that will ensure that utilities needed for compiling typical C programs/etc. are installed.

## Windows

On Windows, the [Windows Subsystem for Linux](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) (WSL), Microsoft's own Linux port is a good option. You may need to do something like `sudo apt install build-essential gdb` to get a C compiler and debugger installed after setting up WSL.

[MinGW](http://mingw.org) project has a version of `gcc` that will probably work for most C labs, though you will need to install it yourself. Microsoft's compiler toolchain can compile C using `cl.exe /Tc filename.c`, but we have never tested how well it works.  If you do, please report how you found it.

Alternatively, the following all attempt to create more complete Unix-like environments for Windows:

- [Cygwin](http://cygwin.com/), which tries to add the entirety of the GNU project to windows
- [MSYS](http://mingw.org/wiki/msys), a lighter-weight GNU environment associated with the MinGW project
- [MSYS2](http://msys2.github.io/), a re-design of MSYS

## OS X

On OS X, Xcode ships with a version of `clang` or with `llvm-gcc` (they call it just `gcc`). On some versions of the OS it is located inconveniently (`/Applications/Xcode.app/Contents/Developer/usr/bin/gcc` in 10.7 <q>Lion</q>) but can be placed where you can more easily access it from the Terminal via XCode's Preferences &rarr; Downloads &rarr; Command Line Tools &rarr; Install.

We believe that Xcode also comes with a suitable `make`, and you should be able to install Python3 in a straightforward matter for when that is required.

## Other

If you use another OS (FreeBSD, Haiku, Irix, etc) hopefully you know how run a C compiler already.

