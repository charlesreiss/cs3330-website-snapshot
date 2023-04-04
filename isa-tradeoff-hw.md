---
title: "HW: ISA tradeoff exercises"
...

# Introduction

In this assignment, you will explore several tradeoffs made in ISA design, including:

*  variable- versus fixed-length instructions
*  two-operand (source, source/destination) versus three-operand (source, source, destination) instructions
*  number of registers
*  placement of operands within an instruction

A difficulty in evaluating many of these tradeoffs is that they depend on how well the compiler can
take advantage of ISA features. For example, if a compiler can usually avoid register-to-register moves
on an ISA two-operand instructions (doing something like `rrmovq %rax, %r10`, `addq %rbx, %r10`
to simulate `3-operand-addq %rbx, %rax, %r10`), then the benefits of three-operand instructions may be minimal.
So, we'll try to examine these in the context of how they change the microarchitecture
and how they are likely to affect compiled code, using some satistics from actual programs.

Enter your answers <a href="https://kytos.cs.virginia.edu/cs3330-fall2021/quizzes/quiz.php?qid=isa-tradeoff-hw">here</a>.

# Program analysis tool and output

We have built a tool that captures on 64-bit x86 Linux programs some statistics about the instructions in
that program. We both check how many times the instruction is present in the program's executable and its
libraries and how many times the instruction is actually issued. For example, given the program:

main:
    movq $0, %rax
start_loop:
    addq $1, %rax
    cmp $20, %rax
    jle start_loop
    ret

we would say that the `cmp` instruction is in the program 1 time and is *issued* 20 times (the number
of iterations the loop is executed).

Our tool identifies each instruction fits into categories like "register-to-register unconditional mov",
and outputs both counts: the number of times those instructions appear in the program and its libraries
and the number of times the instruction was issued during a particular execution.

We supply several outputs from this tool that you will
use for later questions:

*  from a matrix multiply of size 1024x1024
*  from a 1024-variable linear solve
*  from a program counting the number of solutions to the N-queens problem for N=13
*  from GCC compiling the N-queens program with optimizations enabled

You can download these in [this archive](files/isaex/instr-reports.tar.gz).

It is not necessary for the assignment, but you can also download our tool [here](files/isaex/icount.py); it has only been tested on x86-64 Linux
and requires [valgrind](https://www.valgrind.org) and `objdump` (from [GNU binutils](https://www.gnu.org/software/binutils/)) to be installed.
(I believe both of these are present on department machines like portal.cs.virginia.edu.)

(In addition, we supply the [source code](files/isaex/benchmark-sources.tar.gz) for the custom programs
involved.)
# Number of registers and number of registers per instruction

## Impact on instruction encoding

In addition to the complexities of a larger register file, increasing the number of registers affects
the size of instructions. Let's suppose we want to have fixed-size instructions in an encoding with
an opcode, and either two or three register numbers.

### Answer Sheet Part 1

Complete the table below in your answer sheet text file:

|instruction size (bits)|opcode size (bits)|maximum register count (2 operands)|maximum register count (3 operands)
|8|3|4|2|
|16|4|64|16|
|16|5|~|~|
|16|8|~|~|
|32|8|~|~|
|32|10|~|~|

## Two- versus Three-register Instructions

Making a typical instruction have three operands, so that assembly to compute C = A + B is like:

    add A, B, C

rather than like:

    mov B, C
    add A, C

should allow many mov instructions to be avoided. x86-64, of course, requires
the second form. However, compilers can usually find ways of allocating registers to avoid copying
the value. For example:
*  if B is not used after `C = A + B`, the compiler can select to store `C` in the register previously
   being used for `B` and avoid a `mov` instruction; or
*  if the original code is doing an operation `A = A + B` instead of `C = A + B`,
   the compiler can store the result in `A` by doing `add B, A`
   (taking advantage of the `add` being communitative).

To quantify, we ask you below to estimate the number of mov instructions avoided. For example,
given the assembly snippet:

    mov    -0x30(%rax),%rdi
    imul   0x10(%rcx),%rdi
    add    %r15,%rdi
    mov    -0x28(%rax),%r15
    imul   0x18(%rcx),%r15
    add    %r15,%rdi

we might say that the compiler avoided an extra `mov` for each `add` instruction
that would have been required in the worst case because it managed to find a way to accumulate
into the same register as the source operand and produce a correct result, and so managed to avoid
2 mov instructions in the code above.

One might argue that the compiler also avoided two more extra `mov` instructions for the `imul`
instructions because there is not following register-to-register `mov`. Alternately, one might
argue that that extra `mov` is accounted for int he prior register-to-memory load. Since you do not
have sufficiently precise information to tell in this back-of-the-envelope estimate, you may use
whatever strategy you feel is most viable in the question below.

### Answer Sheet Part 2

Based on the instruction statistics provided and the description below,
estimate how effective the compiler is at avoiding these
extra mov instructions in each of the example program *executions*. (That is, estimate how many fewer
movs are executed, not how many fewer movs are present in the executable.)
Briefly explain any assumptions and limitations of your estimate.


## Number of registers and generated code

Having more registers available should allow compilers to generate code that makes less use of memory.

In order to support systems that reserve registers for special purposes (like for the operating system),
GCC has a command line option to specify that particular registers are "fixed". When this is done, GCC's
generated code will not be used. For several of our benchmark programs, we made versions of the programs
compiled in this way to reduce the number of available registers from 16 to 8 (for both general purpose
and floating point registers). The results of our instruction counting tool are included here:

*  from a naive blocked matrix multiply of size 1024x1024
*  from a 1024-variable linear solve
*  from a program counting the number of solutions to the N-queens problem for N=20

### Part 3

#### Subpart a
Some of the programs have fewer total instructions when fewer registers are available.
This is related to x86-64 allowing most instructions to compute on values in memory (unlike
Y86-64, where they must be moved into a register first). Give an example of how a compiler
would generate code with fewer instructions when computing on a value in memory versus in register.

#### Subpart b
Suppose we are comparing two processors, one with 8 registers with a 2 GHz clock rate where instructions
that only access registers take 1 cycle and instructions that access memory take an average of 3 cycles
and another with 16 registers, a 2.2GHz clock rate and the same cycles per instruction.

For the benchmark programs, how much slower or faster would the benchmark programs be based on our benchmark
results?

# Operand placement

Suppose an architecture is to have the following instructions, each of which is marked with a "type":

*  `rrradd SRC_REGISTER1, SRC_REGISTER2, DESTINATION_REGISTER3` (type A)
*  `riradd SRC_REGISTER1, CONSTANT, DESTINATION_REGISTER2` (type B)
*  `rrrsub SRC_REGISTER1, SRC_REGISTER2, DESTINATION_REGISTER3` (type A)
*  `rirsub SRC_REGISTER1, CONSTANT, DESTINATION_REGISTER2` (type B)
*  `beq `<small>(branch if equal)</small>` SRC_REGISTER1, SRC_REGISTER2, TARGET_LABEL` (type C)
*  `blt `<small>(branch if less than)</small>` SRC_REGISTER1, SRC_REGISTER2, TARGET_LABEL` (type C)
*  `rmmov `<small>(register to memory move)</small>` SRC_REGISTER1, CONSTANT(SRC_REGISTER2)` (type D)
*  `mrmov `<small>(memory to register move)</small>` CONSTANT(SRC_REGISTER1), DESTINATION_REGISTER2` (type E)
*  `irmov `<small>(immediate to register move)</small>` CONSTANT, DESTINATION_REGISTER1` (type F)
*  `call TARGET_LABEL` (type G)
*  `ret` (type H)

<!-- FIXME: come up with better set of schemes -->
<!-- FIXME: example answer -->

Suppose register numbers are 5-bits (so there are 32 registers) and opcodes are 4 bits. Consider the following
instruction layout schemes:

*  scheme 1:

        type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
        type B, C, D, E: [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
        type F:          [opcode (4 bits)][register 1 (5b)][constant (23b)]
        type G:          [opcode (4 bits)][constant (28b)]
        type H:          [opcode (4 bits)][unused (28b)]

*  scheme 2:

        type A:          [opcode (4 bits)][register 3 (5b)][register 1 (5b)][register 2 (5b)][unused (13b)]
        type B, C, D, E: [opcode (4 bits)][register 2 (5b)][register 1 (5b)][constant (18b)]
        type F:          [opcode (4 bits)][register 1 (5b)][constant (23b)]
        type G:          [opcode (4 bits)][constant (28b)]
        type H:          [opcode (4 bits)][unused (28b)]

*  scheme 3:

        type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
        type B, D:       [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
        type C, E:       [opcode (4 bits)][constant bits 13-18 (5b)][register 1 (5b)][register 2 (5b)][constant bits 1-13 (13b)]
        type F:          [opcode (4 bits)][constant bits 13-18 (5b)][constant bits 18-23 (5b)][register 1 (5b)][constant bits 1-13 (13b)]

        type G:          [opcode (4 bits)][constant (28b)]
        type H:          [opcode (4 bits)][unused (28b)]

*  scheme 4:

        type A:          [opcode (4 bits)][register 1 (5b)][register 2 (5b)][register 3 (5b)][unused (13b)]
        type B, C:       [opcode (4 bits)][register 1 (5b)][register 2 (5b)][constant (18b)]
        type D:          [opcode (4 bits)][constant bits 13-18 (5b)][register 1 (5b)][register 2 (5b)][constant bits 1-13 (13b)]
        type E:          [opcode (4 bits)][constant bits 13-18 (5b)][register 2 (5b)][register 1 (5b)][constant bits 1-13 (13b)]
        type F:          [opcode (4 bits)][constant bits 13-18 (5b)][constant bits 18-23 (5b)][register 1 (5b)][constant bits 1-13 (13b)]

        type G:          [opcode (4 bits)][constant (28b)]
        type H:          [opcode (4 bits)][unused (28b)]


## Answer Sheet Part 4 

Assume a design similar to the single-cycle procesor described in lecture, with a register file
similar to the one we described in lecture with two read ports and one write port.
Rank the schemes above by how good they are in terms of: (There may be ties.)

*  the number of MUXes or MUX inputs likely required to extract source register numbers for the register file

*  the number of MUXes or MUX inputs likely required to extract destination register numbers for the register file

*  the number of MUXes or MUX inputs likely required to select ALU inputs

# Fixed and variable-length encoding

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

## Answer Sheet Part 5

Suppose we compare a processor like Y86-64, where all immediate values are 8 bytes to a design with
smaller immediates that requires multiple instruction sequences for larger values.

### Part a

Based on the instruction information for the benchmarks, suppose instructions with an immediate support
a signed 16-bit immediate. Otherwise, to construct larger numbers one needs:

*  2 instructions and an extra register to construct a 32-bit value
*  4 instructions and an extra register to construct a 48-bit value
*  6 instructions and an extra register to construct a 64-bit value

Based on this, about how many more instructions would be executed in the benchmark programs?

### Part b
Under the same assumptions as part a, about how much larger would the benchmark programs executables
be?


<!-- FIXME:
# Complicated instructions
    * difficulty to implement with single-cycle design
    * ability for compilers to replace with multiple instructions
    * ??? something with pipelining
-->

# Complex instructions

A major consideration in ISA design is whether the complexity of implementing certain instructions would
be excessive. This is especially true when targetting a design like the ones we have been discussing where
there's no "preprocessing" step for instructions. (As we'll discuss later, many high-performance
processors have a "front-end" that converts machine code to an internal form, which allow complicated
instructions visible to assembler to be converted to multiple simpler operations for the processor's
"back-end".)

For these questions, let's consider a
Y86-like processor built using the single-cycle design we described in lecture that only
implements *only* the following instructions:

*  nop, halt, irmovq, OPq (addq, subq, xorq, andq), cmovXX (including rrmovq), mrmovq, rmmovq, jXX

(that is, Y86-64 without stack-related instructions).

## Requirements for this processor

1.  How many read ports does this processor require on its register file? (In the processor above, 2.)

2.  How many write ports does this processor require on its register file? (In the proecssor above 1.)

3.  How many operations should its ALU support? (In the processor above, 4 (add, sub, and, xor).)

4.  How many reads or writes of *memory* must the procesor be capable of doing at the same time? (In the processor above, 1 read or 1 write, besides the instruction memory access.)

5.  How many constant values can be fed to the ALU? (In the processor above, either 0 (`irmovq` implemented by bypassing the ALU or by taking advantage of `REG_NONE`) or 1 (`irmovq` implemented by being able to provide `0` as an ALU input).)

## Answer Sheet Part 6: Effect of adding select instructions

Choose any two of the following instructions and describe the effects of adding them to the processor
in terms of the requirements listed above? The first is done as an example.

*  `popq REGISTER`

    *Example solution:*
    *  Does not require additional read ports, reads only `%rsp`.
    *  Does require additonal write ports. Previously the processor only needed one, now needs two
       (`%rsp` plus REGISTER)
    *  Does not require a new ALU operation assuming we can feed a new constant.
    *  Does require feeding the constant 8 or -8.

*  supporting memory move instructions that take a base and index register and a scale like:

      rmmovq %rax, 123(%rbx, %rcx, 4)

*  `pushq REGISTER`

*  allowing **all** instructions to be conditional. To take an example, this means that there are forms
   of `irmovq` for each possible condition, such as:

        cirmovle $100, %rax

   which sets `%rax` to `100` if the condition codes indicate "less than", otherwise leaves `%rax`
   unchanged.

   (This is a feature supported by the ARM instruction set.)


*  supporting a `push` instruction that can push an arbitrary set of registers. For example,

        pushq { %rax, %rbx, %rcx, %rdx }

   would be a single instruction equivalent to

       pushq %rax
       pushq %rbx
       pushq %rcx
       pushq %rdx

   (This is a feature supported by the ARM instruction set.)


