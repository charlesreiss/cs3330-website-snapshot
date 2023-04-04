# Virtual Memory Lab

> Note: This lab is a **tentative** draft.

In this lab, you will write code to create an initial page table mapping for
a program. To avoid dealing with the difficulties of debugging an full OS,
we have written a simple simulator for the page table lookup. This simulator
provides the following functionality:

*  reading from a simulated physical memory address
*  writing to a simulated physical memory address
*  allocating a new page of simulated physical memory
*  reading from or writing to a simulated virtual memory address

These pieces of functionality are provided as C functions you can call.
Against these functions, you will implement a function that takes
ranges of allocated physical pages and the virtual addresses they
should be mapped at. Given these, this function should return
a newly allocated page table that maps those functions correctly.

## Handout

Download the code handout [here](files/vmlab-handout.tar). This contains
the following files:

*   `vmsim.h`: header file for our virtual memory simulator. This contains the data structures and functions you must use.
*   `vmsim.c`: implementation of the functions in vmsim.h. You should not need to modify this file.
*   `vmlab.c`: This is the file you should modify. We have provided a correct implementation of a function that allocates an empty page table for you. Your task is to complete the `create_page_table_for_program` function.
*   `vmtest.c`: file to test your program in `vmlab.c`.

## Page Table Format

The simulator uses a 4-level page table with 4096 byte pages.
Each level of the page table uses 8-byte page table entries containing:

*  a "present" bit, which if set, indicates that the page or next level of the page table is present
*  "read", "write", and "execute" bits which indicates if the page or pages are readable, writeable, or executable;
*  a 30-bit physical page number; and
*  30 unused bits, which should always be 0

A page table at each level is one page long, containing 512 of these 8-byte page table entries.
Physical addresses are 42 bits long (30-bit page number plus 12-bit page offset) though very
few of the possible physical addresses are usable. Virtual addresses are 48 bits long 
(36-bit page number, divided into four 9-bit pieces, plus 12-bit page offset).

In `vmsim.h` we define a struct type `pte_t` to represent a page table entry and functions to convert
it to and from a 64-bit integer.

## Simulator functions

We define the following useful types in `vmsim.h`:

*  `pa_t`: represents a physical address (a 64-bit unsigned integer)
*  `va_t`: represents a virtual addresss
*  `pte_t`: represents a page table entry

Also, we include `<stdint.h>` which defines the type `uint64_t`, which is a 64-bit unsigned integer.

We define the following useful functions in `vmsim.h`:

*   `read_pa`, `write_pa`: read of write a 64-bit value at a particular simulated physical address
*   `allocate_physical_pages(NUM)`: allocate NUM new contiguous physical pages. Aborts the program if not enough simulated memory is available. Returns the newly allocated pages.
*   `dump_page_table(page_table, levels, prefix)`: display the contents of a page table given its physical address. Displays up to `levels` levels of page tables, so to display an entire nested page table pass `4`. `prefix` is a string to print before each line of output.
*   `uint64_to_pte`, `pte_to_uint64`: convert a PTE to a 64-bit unsigned integer and vice-versa

In addition, the following functions exist to support our testing code:

*   `reset()`: reset all simulated memory.
*   `set_page_table_base_pointer`, `get_page_table_base_pointer`: get or set the page table base pointer to use for the functions below. You should not need to call this function unless you are writing your own tests.
*   `va_to_pa_noisy(virtual_address, need_read, need_write, need_exec)`: convert a virtual address to a physical address, printing out messages if anerror occurs. Returns the constant `INVALID_ADDRESS` if the conversion fails. The converted address will be checked for the read/write/exec permissions indicated.

## Test file

We include some testing code, including a `main()` in `vmtest.c`.

## Your task

You should modify `vmlab.c` to implemen the `create_page_table_for_program` function. We have supplied a version
which return an empty page table (one where everything is invalid). You need to modify it to return a page
table which maps the indicated code, data, and stack regions. Each of these regions has a contiguous area of virtual memory, starting at the address specified. These virtual addresses should be mapped to a contiguous area of physical memory, starting at the address specified.

If you are successful, the output of `make test` (excluding compilation messages, etc.) should look like:

    ./vmtest
    Running test case 1
    5 pages allocated (4 used for page tables)
    Running test case 2
    18 pages allocated (8 used for page tables)
    Running test case 3
    18 pages allocated (12 used for page tables)
    Running test case 4
    30 pages allocated (4 used for page tables)
    Running test case 5
    31 pages allocated (7 used for page tables)
    Running test case 6
    1035 pages allocated (8 used for page tables)
    Tests passed.

## Submission

Submit whatever you have completed in `vmlab.c` to the submission site.
