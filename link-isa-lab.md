---
title: "Linking and ISA tradeoffs"
...

{:.changelog}
Changelog:

{:.changelog}
*  13 Feb 2023: update date on linking lecture

# Your task

1.  For all of the tasks below, answer the corresponding question on the [answer sheet]({{site.submit_site}}/quizzes/quiz.php?qid=link-isa-lab). Remember that for the lab (but not the corresponding homework) you may collaborate with other students; if you do please, note this in the comments on the answer sheet.

## Linking

1.  (answer sheet part 1) Using the supplied object file [format description](linking-task-format.html)

    *  translate these Y86 files [sum-main.ys](files/linking-task/sum-main.ys) and [sum.ys](files/linking-task/sum.ys) into "object files" in our special human-readable format, and copy-and-paste it to the answer sheet. Assume that all labels declared in these assembly files become symbols in the corresponding object file's symbol table (even without any directives like `.global`).
    
    You may (and we would strongly recommend) use the `yas` (Y86 assembler tool) distributed with HCLRS to help you translate the assembly to machine code. *You will still need to identify what relocation and symbol table entries to create manually* (`yas` generates our equivalent of an executable). See the [instructions below](#using-yas).

    [You may want to refer to the lecture on the compilation pipeline from 31 January.]

## ISA tradeoffs

1.  (answer sheet part 2) Consider a fixed-instruction-length ISA. Complete the table below describing options for
    instruction layout and register count:

    |instruction size (bits)|opcode size (bits)|maximum register count (2 operands)|maximum register count (3 operands)
    |8|3|4|2|
    |16|4|64|16|
    |16|5|~|~|
    |16|8|~|~|
    |32|10|~|~|

    (You may assume the ISA only uses power-of-two register counts and that each operand can specify any of the registers.)

    See [below under the heading "register count limits"](#regcount-table) for an explanation of the first row of the table.

    Record your answers on the answer sheet.

2.   We have supplied some statistics from instructions in some benchmark programs [described below](#benchmark-data), which will be used for couple of the below questions and some questions on the corresponding homework.

4.  (answer sheet part 3)
    Suppose a processor took an average of 1 cycle to execute each instruction that is not a conditional jump and 1.1 cycles to execute each
    conditional jump instruction. Then, this processor design was improved (without changing its clock rate) to take an average of 1.05 cycles to execute
    each conditional jump instructions. By how much would the performance of
    the "blocked matmul" and "queens" programs improve?

3.  (answer sheet part 4) For three of the benchmarks, we provide statistics about them compiled
    with 8 registers available and 16 registers available. (For example,
    for the "gull" program, the CSV file or spreadsheet sheet "gull-with-8-regs" shows statistics
    from a version compiled with 8 registers available, and "gull" from a version compiled
    with the standard 16.)

    Suppose we are comparing two processors, one with 8 registers with a 2.1 GHz clock rate
    (2.1 billion clock cycles per second)         and another with 16 registers, a 2GHz clock rate.
    On both processors, instructions
    that only access registers take 1 cycle and instructions that access memory
    (either read or write or both) take an average of 3 cycles
    (You may assume that all instructions that only access registers do not access memory and
    vice-versa.)

    For the "queens" and "blocked matmul" programs, how much slower or faster would the benchmark
    programs be on the 16-register procesor based on our benchmark results?
    Write the estimate you compute to at least two significant figures and describe the
    calculation you performed.

    (Note that to compute the number instructions that access memory, you'll need to use
    the supplied counts of instructions that read memory, that write memory, and that both
    read and write memory.)


# using YAS

Our textbook authors have written a Y86 assembler, which we distribute with HCLRS.
Unlike a normal assembler, `yas` *does not generate the object files* (despite using the
extension `.yo`); it assumes that its assembly input is a self-contained program so no
separate linking step is needed (and therefore no file with linking information is needed).
To use `yas`:

1.  First download [hclrs.tar](files/hclrs.tar).

2.  Extract hclrs.tar. You can do this from the command line using `tar xvf hclrs.tar`, which will create
    an `hclrs` directory.

3.  In the `hclrs` directory, run `make`.

4.  In a text editor, create an example Y86 assembly program `simple.ys`:

        start:
            irmovq $100, %rax
            irmovq $1, %rbx
            irmovq $3, %rcx
            irmovq $4, %rdx
        loop:
            subq %rbx, %rax
            addq %rdx, %rcx
            jg loop
            halt

5.  Run `tools/yas simple.ys` to produce `simple.yo`:

        0x000:                      |         start:
        0x000: 30f06400000000000000 |             irmovq $100, %rax
        0x00a: 30f30100000000000000 |             irmovq $1, %rbx
        0x014: 30f10300000000000000 |             irmovq $3, %rcx
        0x01e: 30f20400000000000000 |             irmovq $4, %rdx
        0x028:                      |         loop:
        0x028: 6130                 |             subq %rbx, %rax
        0x02a: 6021                 |             addq %rdx, %rcx
        0x02c: 762800000000000000   |             jg loop
        0x035: 00                   |             halt

6.  This file includes the machine code for the assembly program on the right-hand side.
    For example, reading the line `0x00a: 30f30100000000000000` tells us that
    the byte with index 0xa is `0x30`, the byte with index `0xb` is `0xf3`, 
    with `0xc` is 0x01`, and so on.

    Note that this format is deliberately very similar to what our object file format
    expects, so you can copy-and-paste most of the instructions.

7.  `yas` only handles complete assembly programs, so if you try to assemble a file
    which references a label from elsewhere it will fail. To deal with this, I would recommend
    replacing the label with one that's actually present in the assembly file so `yas` will work, and then
    manually determining where that label's address was placed.

# benchmark statistics {#benchmark-data}

We've built a tool that records the activity of x86-64 Linux programs and reports statistics
about the instructions executed by that program. We've supplied the output of this program on several
different benchmark programs:

*  "blocked matmul": a matrix multiply of size 1024x1024
*  "gull": the chess engine [LazyGull](https://github.com/basil00/Gull) analyzing a particular chess position
*  "linear solve": a 1024-variable linear solve
*  "queens": a program counting the number of solutions to the N-queens problem for N=13
*  "gcc-queens": from GCC compiling the N-queens program with optimizations enabled

For the first four programs, we provide two sets of statistics: one from the program's compiled
normally and one from them compiled restricted to 8 registers.

You can download these statistics in [this archive](files/isaex/instr-reports.tar) 
(or, alternately, this [Excel-format spreadsheet](files/isaex/instr-reports.xlsx) *[last updated 2022-09-13]*.)
The CSV files each contain a table, whose columns are labeled in the second row of the output and are:
*  category (description of type of instruction)
*  retired (number of times instructions of that type executed completely)
*  % of retired (number of times instructions of that type executed divided total number of times instructions exectued completely times 100)
*  in program (number of instructions of that type)
*  % of in program (number of instructions of that type divided by total number of instructions times 100)

There are separate CSV files for each benchmark and a "combined.csv" file which merges them together (in case
you find that more convenient to work with).

The "types" we've categorized instructions into are **not** mutually exclusive, for example:

*  all "instructions with a non-zero immediate that fits in 10 bit (or smaller) signed number" are also "instructions with non-zero immediate".
*  all "instructions with disp(,rYY,scale) addressing (where scale is not 1)" are also "instructions with disp(rXX,rYY,scale) or disp(,rYY,scale) addressing (where scale is not 1)"

(In addition, we supply the [source code](files/isaex/benchmark-sources.tar.gz) for the custom programs
involved.)

Note that some of the categories of statistics overlap;
for example, we report both "instructions that write memory" and
"non-mov/cmov/push instructions that write memory".

## counting

Our statistics include counts of both the number of times an instruction is present and the number of times it
is actually "retired" (or completely executed). To give an example to explain what these means, given the program:

    main:
        movq $0, %rax
    start_loop:
        addq $1, %rax
        cmp $20, %rax
        jle start_loop
        ret

we would say that the `cmp` instruction is in the program 1 time and is *retired* 20 times
(the number of iterations the loop is executed).

Our statistics categorize instructions into categories like "register-to-register unconditional mov".
Many categories we provide overlap.

(I believe these statistics
are mostly correct, but given the complexities of obtaining them and interpreting x86-64 instructions, it's likely
there are some inaccuracies.)

## calculating with statistics example

Let's suppose we wanted to calculate what portion of executed instructions
read or wrote memory. The most
relevant categories in the statistics files are:

1.  "instructions that write memory"
2.  "non-mov/cmov/push instructions that write memory"
3.  "instructions that read memory"
4.  "non-mov/cmov/push instructions that read memory"
5.  "instructions [that] both read AND write memory"

The count for category 2 is included in category 1, and
for category 4 is included in cateogry 3. Therefore, we don't need to
include categories 2 and 4  in our calculation.

The count for category 5 is instructions that are *both* in categories
1 and 3. So the calculation of the number of executed instructions
that read or write memory is:

    #(instructions that write memory) + #(instructions that read memory) - #(instructions that both read AND write memory)

Reading the statistics from gull.csv, the relevant values are:

    instructions that write memory: 704257450
    instructions that read memory: 1160466519
    instructions that both read AND write memory: 269378093

so the *count* of isntructions that read/write memory is:
    
    704257450 + 1160466519 - 269378093 = 1595345876

and from gull.csv, the total number of instructions executed is 4444321834,
so the *portion* of instructions executed that read/write memory is:

    1624753259 / 4444321834 =~ 0.141


## the underlying tool

Our tool is based on processing a list of executed instructions, so *it does not count instructions that are never executed, even if they are present in the executable/library*.

Although it is not necessary to complete this lab (or the following homework),
you can download our tool  [here](files/isaex/icount.py) [*last updated 2020-09-14*];
it has only been tested on x86-64 Linux
and requires [valgrind](https://www.valgrind.org) and `objdump` (from [GNU binutils](https://www.gnu.org/software/binutils/)) to be installed.
(I believe both of these are present on department machines like portal.cs.virginia.edu.)


# register count limits {#regcount-table}

Above we stated that with 8-bit instruction size and 3-bit opcode size and power-of-two register
counts, we could have at most 4 registers with 2 operands.

To understand why this, let's consider what the instruction layout looks like. We have 8-bits to work
with, but 3 of those are taken up by an opcode.

If we have two operands, there are 5 bits left over to work with. We need to specify two register indices
in these bits. Since we know we have a power-of-two register count, the way we are going to do this is to use
some of these bits for each of the two register indices. The best way we can split up these bits is using
two bits for the first index, two bits for the second index, and having one bit left over. With two bits
specifying a register index, we can have at most 4 registers (00, 01, 10, and 11).

(If we allowed non-power-of-two register counts, we could support more registers at the cost
of making instruction decoding much more complicated: for example, we could treat the
5-bits as an unsigned number X which would range from 0 to 31 that is translated into
two register numbers. We could decide that floor(X / 5) is the first register
index, and X mod 5 is the second register index. This would allow us to support register
indices for either operand from 0 to 4 inclusive instead of 0 to 3 inclusive.

Instruction sets rarely use "tricks" like this, however, because they make instruction decoding
more complicated than alternatives. For example, instead of using this complicated encoding,
it would probably be simpler and about as space-efficient to support a variable-length encoding
where instructions that use higher register indices take up more bytes.)


