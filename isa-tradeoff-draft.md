---
title: "Lab: ISA tradeoff exercises"
...

# Introduction

In this lab, you will explore several tradeoffs made in ISA design, including:

*  variable- versus fixed-length instructions
*  two-operand (source, source/destination) versus three-operand (source, source, destination) instructions
*  number of registers
*  placement of operands within an instruction

A difficulty in evaluating many of these tradeoffs is that they depend on how well the compiler can
take advantage of ISA features. For example, if a compiler can usually avoid register-to-register moves
on an ISA two-operand instructions (doing something like `rrmovq %rax, %r10`, `addq %rbx, %r10`
to simulate `3-operand-addq %rbx, %rax, %r10`), then the benefits of three-operand instructions may be minimal.
So, we'll try to examine these in the context of how they change the microarchitecture
and how they are likely to affect compiled code, using some satistics from actual assembly programs.

These are the sort of analyses that should motivate architecture designs.

# Operand placement

Suppose an architecture is to have the following instructions, each of which is marked with a "type":

*  `rrradd SRC_REGISTER, SRC_REGISTER, DESTINATION_REGISTER` (type A)
*  `riradd SRC_REGISTER, CONSTANT, DESTINATION_REGISTER` (type B)
*  `rrrsub SRC_REGISTER, SRC_REGISTER, DESTINATION_REGISTER` (type A)
*  `rirsub SRC_REGISTER, CONSTANT, DESTINATION_REGISTER` (type B)
*  `beq `<small>(branch if equal)</small>` SRC_REGISTER, SRC_REGISTER, TARGET_LABEL` (type C)
*  `blt `<small>(branch if less than)</small>` SRC_REGISTER, SRC_REGISTER, TARGET_LABEL` (type C)
*  `rmmov `<small>(register to memory move)</small>` SRC_REGISTER, CONSTANT(SRC_REGISTER)` (type D)
*  `mrmov `<small>(memory to register move)</small>` CONSTANT(SRC_REGISTER), SRC_REGISTER` (type E)
*  `irmov `<small>(immediate to register move)</small>` CONSTANT, SRC_REGISTER` (type F)
*  `call TARGET_LABEL` (type G)
*  `ret` (type H)

Suppose register numbers are 5-bits (so there are 32 registers) and opcodes are 4 bits. Consider the following
instruction layout schemes:

*  scheme 1:

    type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
    type B, C, D, E: [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
    type F:          [opcode (4 bits)][register 1 (5b)][constant (23b)]
    type G:          [opcode (4 bits)][constant (28b)]
    type H:          [opcode (4 bits)][unused (28b)]

*  scheme 2:

    type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
    type B, E:       [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
    type C, D:       [opcode (4 bits)][constant bits 13-18 (5b)[register 1 (5b)][register 2 (5b)][constant bits 1-13 (13b)]
    type F:          [opcode (4 bits)][register 1 (5b)][constant (23b)]
    type G:          [opcode (4 bits)][constant (28b)]
    type H:          [opcode (4 bits)][unused (28b)]

*  scheme 3:

    type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
    type B, D:       [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
    type C, E:       [opcode (4 bits)][constant bits 13-18 (5b)][register 1 (5b)][register 2 (5b)][constant bits 1-13 (13b)]
    type F:          [opcode (4 bits)][register 1 (5b)][constant (23b)]
    type G:          [opcode (4 bits)][constant (28b)]
    type H:          [opcode (4 bits)][unused (28b)]


*  scheme 4:

    type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
    type B, D:       [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
    type C, E:       [opcode (4 bits)][constant bits 13-18 (5b)][register 1 (5b)][register 2 (5b)][constant bits 1-13 (13b)]
    type F:          [opcode (4 bits)][constant bits 13-18 (5b)][constant bits 18-23 (5b)][register 1 (5b)][constant bits 1-13 (13b)]

    type G:          [opcode (4 bits)][constant (28b)]
    type H:          [opcode (4 bits)][unused (28b)]

*  scheme 5:

    type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
    type B, C:       [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
    type D:          [opcode (4 bits)][constant bits 13-18 (5b)][register 1 (5b)][register 2 (5b)][constant bits 1-13 (13b)]
    type E:          [opcode (4 bits)][constant bits 13-18 (5b)][register 2 (5b)][register 1 (5b)][constant bits 1-13 (13b)]
    type F:          [opcode (4 bits)][constant bits 13-18 (5b)][constant bits 18-23 (5b)][register 1 (5b)][constant bits 1-13 (13b)]

    type G:          [opcode (4 bits)][constant (28b)]
    type H:          [opcode (4 bits)][unused (28b)]

Assume a design similar to the single-cycle procesor described in lecture, with a register file
with two read ports and one write port.
Rank the schemes by how good they are in terms of: (There may be ties.)

*  the number of MUXes or MUX inputs likely required to extract source register numbers for the register file

*  the number of MUXes or MUX inputs likely required to extract destination register numbers for the register file

*  the number of MUXes or MUX inputs likely required to select ALU inputs

*  the number of MUXes or MUX inputs required to extract inputs to the PC register

*  the number of MXUes or MUX inputs required to select data memory address inputs

# (due with lab) Fixed and variable-length encoding

Fixed-length encodings simplify instruction sets, but usually at the cost of making programs larger.
In a fixed-length encoding, instructions that take fewer operands must take up the same amount of
space as an instruction that uses many operands.

Based on the Y86-instruction set one might imagine that this means that an equivalent fixed-length instruction
set would have 10-byte instructions. While this is certainly a possibility, typically fixed-length instruction
sets compromise by limiting the size of constants in instructions. For example, the RISC V 64-bit ISA supports
an encoding whereall instructions are 32-bits, even though registers are 64-bits. So rather than being
able to do something like:

    irmovq $0x12345678, %r10

to load the 32-bit value `0x12345678`, one must use two instructions. If Y86-64 was designed
more like RISC V, this might look like:

    lui $0x1234, %r10 /* load upper immediate (constant) --- move into top -bits of destination */
    iaddq $0x5678, %r10 /* add immediate (constant) --- with 16-bit immediate */

where the encoding of `lui` and `iaddq` wouldn't have room for much more than 16-bit immediate after fitting
in the opcode and register number into the 32-bit instructions.

To put a 64-bit value like `0x1234567890ABCDEF` in a register in this design,
one would need a sequence of several insturctions like:

    /* "load upper immediate" */
    lui $0x1234, %r10
    /* "immediate add" */
    iaddq $0x5678, %r10
    /* "logical shift left by immediate (constant)" */
    isll $16, %r10
    iaddq $0x90AB, %r10
    isll $16, %r10
    iaddq $0xCDEF, %r10

Or, alternately, a compiler might prefer to generate a `rmmovq` instruction rather than attempt to
use the equivalent of `irmovq`.

## Exercise

Suppose we have a variant of Y86-64 which uses 32-bit instructions that only support 16-bit immediate
values. To make this simpler, the following instructions are added:

    *  `lui IMMEDIATE, DESTINATION-REGISTER`: sets `DESTINATION-REGISTER` to `IMMEDIATE << 16` (left shift by 16)

    *  `iaddq IMMEDIATE, DESTINATION-REGISTER`: adds `IMMEDIATE` to `DESTINATION-REGISTER`

    *  `isll IMMEDIATE, DESTINATION-REGISTER`: left-shift destination-register by `IMMEDIATE` bits

    *  `orq REGISTER, REGISTER`: bitwise-or OPq variant

Assume immediates are always interpreted as unsigned integers.

    irmovq $0x12345678, %r10
    irmovq $0x9ABCDEF0, %r11
    irmovq $0x100000000, %r8
    irmovq $1, %r13
    irmovq $0xFFFFFFFFFFFFFFFF, %r14
    rrmovq %r11, %r12
    subq %r10, %r11
    andq %r10, %r12
    cmove %r14, %r13
    addq %r13, %r12
    xorq %r12, %r8

Compute and write in your answersheet:

*  (a) How large the original assembly's machine code was?
*  (b) How large would the original assembly's machine code be if `irmovq` had two encodings: one with 32-bit constants and one with 64-bit constants?
*  (c) How large the new assembly's machine code would be?

# Number of registers

## Impact on instruction encoding

In addition to the complexities of a larger register file, increasing the number of registers affects
the size of instructions. Let's suppose we want to have fixed-size instructions in an encoding with
an opcode, and either two or three register numbers.

Complete the table below in your answer sheet text file:

|instruction size (bits)|opcode size (bits)|maximum register count (2 operands)|maximum register count (3 operands)
|8|3|4|2|
|16|4|64|16|
|16|5|~|~|
|16|8|~|~|
|32|8|~|~|
|32|10|~|~|
|48|12|~|~|

## How many registers can a compiler effectively use?

Since a larger register file is slower than a smaller one, providing extra registers will slow down
programs unless they make effective use of these registers.

Although exactly how a compiler decides what and how many registers to use is a topic we won't cover in detail
in this class, we can explore this by examining how compiler output changes when the number of registers
it can use is restricted. To do this, we can examine the assembly generated by a compiler configured to
make variable numbers of registers available. In GCC, we can reduce the number of registers available
by using a command-line option like `-ffixed-r10`. When `-ffixed-r10` is specified, GCC assumes that `r10`
cannot be used by its generated code (even temporarily) and so will not use it.

(A more flexible way to do this experiment would be to define a new ISA for GCC which is like X86-64 but
with a different number of registers. This would allow us to experiment with adding registers in addition to
removing them, but would require us to recompile GCC, which would be too inconvenient for this assignment.)

To assist in this, we've supplied a program TBA that will examine an .o or executable file and count:

*  the number of registers each function uses
*  the number of instructions each function contains
*  the number of instructions that access memory each function contains
*  the number of register-to-register move instructions (for the next part)

Complete the table below for the benchmark programs TBA by comparing how GCC behaves with

# Number of operands

A major concern with including only two-operand instructions is that compilers will need to
generate a lot of register-to-register move instructions that would be unnecessary if
the three-argument form was supported.
Examine the suite of benchmark programs you examined for the previous part with the program.

Suppose we needed about 4 extra bits (the number bits neeeded to encode an x86-64 register number)
for each instruction to accomodate three-argument form. If so, about how much space would be
added or saved for each of the benchmark program by switching to the four-argument form?

<!-- FIXME: something with instruction traces -->

