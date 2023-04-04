
# Part 3: Operand placement questions

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

## Questions

Assume a design similar to the single-cycle procesor described in lecture, with a register file
similar to the one we described in lecture with two read ports and one write port.
Rank the schemes above by how good they are in terms of: (There may be ties.)

*  (Question 4) the number of MUXes or MUX inputs likely required to extract source register numbers for the register file

*  (Question 5) the number of MUXes or MUX inputs likely required to extract destination register numbers for the register file

*  (Quesiton 6) the number of MUXes or MUX inputs likely required to select ALU inputs

# Part 4

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

## Question 6 and 7

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


# Part 4

## three- versus two-operand instructions
Making a typical instruction have three operands, so that assembly to compute C = A + B is like:

    add A, B, C

rather than like:

    mov B, C
    add A, C

should allow many (maybe most?) mov instructions to be avoided. x86-64, of course, requires
the second form. However, compilers can usually find ways of allocating registers to avoid copying
the value. For example:
*  if B is not used after `C = A + B`, the compiler can select to store `C` in the register previously
   being used for `B` and avoid a `mov` instruction; or
*  if the original code is doing an operation `A = A + B` instead of `C = A + B`,
   the compiler can store the result in `A` by doing `add B, A`
   (taking advantage of the `add` being communitative).

One might worry that these cases are rare and so having only two operands will have
a very large cost. We'll try to observe whether that's true in these hopefully
typical programs from the instruction statistics we have.

## quantifying "extra" movs
Below we ask you to estimate the number of mov instructions avoided. For example,
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
argue that that extra `mov` is accounted for in the prior register-to-memory load. Since you do not
have sufficiently precise information to tell in this back-of-the-envelope estimate, you may use
whatever strategy you feel is most viable in answering the question in this lab.

## Subpart a
For this problem, use the instruction information from benchmarks original supplied in 
[the lab](link-isa-hw.html#benchmark-data).

Quantify an *estimate* of how many more `mov` instructions would be **executed** if the compiler
needed to preserve the originally operands to every two-operand instruction.
Because you have relatively limited information, this estimate will not be precise.
Describe how you obtained your estimate.
