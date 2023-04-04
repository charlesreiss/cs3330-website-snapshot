---
title: "Object file/linking exercise"
...

# Your task

0.  Download the supplied Y86 assembly files and an incomplete `format.txt` file in archive TBA. <!-- [this archive](files/linking-task.tar) -->


1.  Devise an object file format to allow linking multiple Y86 assembly files without reassembling

    Your object file format should:
    
    *  only store instructions in machine code format; it should not include mnemonics, etc.;

    *  not have any dependencies on Y86 machine code other than labels being stored in machine
       code as 8-byte integers. (This means that the same object file format should be suitable for some
       other instruction set that shares this property.);

    *  endeavour to make the linker simple to write;

    *  allow for the linker to choose the memory location of the code and data segments of
       each object file when it links the executable. (Nothing about these locations should
       be decided earlier.)

    Describe your chosen format in a file called `format.txt`. We've supplied a template for you.

    Since you may be translating to your object file format by hand, we recommend choosing a format
    that can be edited in a text editor.

2.  Translate (perhaps by hand) the supplied assembly files to your object file format.

    Name the translated files by replacing `.s` with `.obj`

3.  Link (perhaps by hand) the assembly files above from your object files. Order the files so the
    file containing the symbol `main` is first.

    Format the executable as a list of hexadecimal byte values, starting with address 0.

    Name your executlabe file `a.exe`

4.  Create tar archive containing each of the files you created above (`format.txt`, each of the `.obj` files
    and `a.exe` and submit it to the submission site. The supplied `Makefile` will do this when you run
    `make submit`.
