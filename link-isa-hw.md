---
title: "Linking and ISA tradeoffs"
...

Record your answers on the [answer sheet]({{site.submit_site}}/quizzes/quiz.php?qid=link-isa-hw).


# Part 1: Linking

Using the supplied object file/executable [format description](linking-task-format.html) (same as in the lab):

*  translate this following object files into an executable file in our special human-readable format:

    * [multiply.obj](files/linking-task/multiply.obj)
    * [square.obj](files/linking-task/square.obj)
    * [square-main.obj](files/linking-task/square-main.obj)

When creating the executable, make sure to place the "`main`" symbol at address `0x0`.

Copy-and-paste your executable into the answer sheet.

(Shortly after the lab is due, you should be able to access [this possibly helpful example](https://collab.its.virginia.edu/access/content/group/08eed933-d447-48f4-9b19-f86b9f076c52/linkisalab-combine.txt)
(also on Collab under Resources) of combining the object files from the lab.)

# Part 2:  Complex Addressing Modes

x86-64 allows for the complex addressing modes where a memory location is specified using two registers
as in `(%rax, %rbx)`, including the most complicated form of something like `1234(%rax, %rbx, 4)`.
Although this makes instruction encoding more complicated, perhaps a x86-64 processor
can obtain a benefit by including hardware specialized for performing the two-register+scale 
address computation.

## Subpart a

Using only the `0x1234(%rax)`-style of addressing memory (like supported in Y86-64), write
out assembly code equivalent to
    
    movq 0x1234(%rax, %rbx, 8), %rcx

using not more than 6 instructions. 
(In Intel syntax, this instruction would be written `mov RCX, [RAX + RBX * 8 + 0x1234]`. In pseudocode,
its effect might be written `RCX <- ReadEightBytesFromMemoryAtAddress(RAX + RBX * 8 + 0x1234)`.)
Your assembly code:

*  may _not_ change the values of any registers other than `%rcx`; but
*  _can_ use x86-64 instructions that don't exist in Y86-64, like `imul` or `shl`;

## Subpart b
For this problem, use the instruction information from benchmarks originally supplied in 
[the lab](link-isa-lab.html#benchmark-data). (Note especially the calculation example.)

If the compiler used a simple translation (similar to what you did in part a)
of these instructions to avoid the complex addressing to specify memory locations
(that is, specifying memory locations using only the `offset(base register)`
addressing supported by Y86-64),
then about how many times more
instructions would the processor execute? Record your answers for the gull, queens, and gcc-queens
benchmarks on the answer sheet, along with an explanation of your method. Include at least three significant
figures in your estimate (so we can more easily figure out what computation you did,
even though the estimate is far from that accurate).

(Since you do not have precise
information about the programs, your estimate does not have to be exact, it just needs to
be consistent with a reasonable method. Since we are asking for
**simple** translations, you do not have to come up with the best possible assembly translation.
You do not need to handle converting instructions like `movq 0x100000, %rax`
(no index register or scale) to the `offset(base register)` style addressing, as we don't consider
that a complex addressing mode (but we will not deduct credit if you attempted this).)

#  Part 3
Fixed-length encodings simplify instruction sets, but usually at the cost of making programs larger.
In a fixed-length encoding, instructions that take fewer operands must take up the same amount of
space as an instruction that uses many operands.

Based on the Y86-instruction set one might imagine that this means that an equivalent fixed-length instruction
set would have 10-byte instructions. While this is certainly a possibility, typically fixed-length instruction
sets compromise by limiting the size of constants in instructions. For example, the RISC V 64-bit ISA supports
an encoding where all instructions are 32-bits, even though registers are 64-bits. So rather than being
able to do something like:

    irmovq $0x12345678, %r10

to load the 32-bit value `0x12345678`, one must use two instructions. If Y86-64 was designed
more like RISC V, this might look like:

    lui $0x1234, %r10 /* load upper immediate (constant) --- move into top -bits of destination */
    iaddq $0x5678, %r10 /* add immediate (constant) --- with 16-bit immediate */

where the encoding of `lui` and `iaddq` wouldn't have room for much more than a 16-bit immediate after fitting
in the opcode and register number into the 32-bit instructions.

To put a 64-bit value like `0x1234567890ABCDEF` in a register in this design,
one would need a sequence of several instructions like:

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
   
## Subpart a
For this problem, use the instruction information from benchmarks originally supplied in 
[the lab](link-isa-lab.html#benchmark-data).

Since our benchmark programs were run on X86-64, instructions supporting 32- and 64-bit constants
were readily available to the compiler. Let's consider how the compiler would perform if the instruciton
set only supported 16-bit constants, so instructions
using larger constants required a sequence to load the larger constant value.
To get a rough estimate of the effect of a fixed-length instruction set, lets suppose the compiler would need:

*  1 additional instructions to construct a 32-bit signed value
*  3 additional instructions to construct a 48-bit signed value
*  4 additional instructions to construct a 64-bit signed value

Assume that using 16-bit signed values requires no additional instructions and
that the largest immediate used in any of the benchmark programs fit in a 64-bit
signed value.

Most likely, the compiler would also need to use some extra registers. To keep things simpler, let's assume
that effect is negligible. Based on these assumptions, about how many times more instructions would be executed in the "blocked-matmul", "gull", and "gcc-queens" benchmarks? Include at least three significant figures in your
estimate.

(When counting instructions executed for this part, if an instruction is executed 10 times, count it 10 times. This is what the "retired" column in our benchmark data does.)

## Subpart b

Under the same assumptions as subpart a,
about how much larger would the "blocked-matmul", "gull" and "gcc-queens" benchmarks be in terms of number of instructions stored in
the program's executable or libraries that were executed at least once? Include at least three significant figures in your estimate.

(When counting instructions stored and executed at least once for this part, count each instruction once. This is what the "in program" column in our benchmark data does.)

(Since variable-length instruction sets typically have shorter instructions, this is probably
an underestimate of increase in file size.)

# Part 4

## three- versus two-operand instructions
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
   (taking advantage of the `add` being communicative).

One might worry that these cases are rare and so having only two operands will have
a very large cost, but looking at what compilers do in practice often seems to show that it is not.

## Subpart a

Consider the following C expression:

    r8 = ((r9 * r10 + r8 * r11) & (r12 * r13));

Assuming `r8` through `r13` are assigned to variables `%r8` through `%r13`, this could
be written using the three-operand form of `add`s as follows (and using
`%rax` and `%rbx` as temporary registers):

        imulq %r9, %r10, %rax
        imulq %r8, %r11, %rbx
        addq %rax, %rbx, %rbx
        imulq %r12, %r13, %rax
        andq %rax, %rbx, %r8

A naive translation of this to the two-operand form might be like:

        movq %r10, %rax
        imulq %r9, %rax
        movq %r11, %rbx
        imulq %r8, %rbx
        addq %rax, %rbx
        movq %r13, %rax
        imulq %r12, %rax
        movq %rbx, %r8
        andq %rax, %r8

This would seem to suggest a large cost (at least in terms of total number of instructions)
to using three-operand expressions over two-operand
expressions, but this naive translation is substantially worse than a compiler can do. Write an
alternate translation to a two-operand form that produces the same values for the registers
`%r8` through `%r13` and has fewer instructions.


