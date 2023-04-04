
## Exercise setup

Suppose we have a variant of Y86-64 which uses 32-bit instructions that only support 16-bit immediate
values. To make this simpler, the `irmovq` instruction is replaced with the following instructions are added:
    
*  `irmovlowq IMMEDIATE, DESTINATION-REGISTER`: set `DESTINATION-REGISTER` to the signed 16-bit value IMMEDIATE
    
    e.g. `irmovlowq $10, %rax` sets `%rax` to `10`
    
    e.g. `irmovlowq $-24, %rax` sets `%rax` to `-24`

    e.g. `irmovlowq $0x12345, %rax` and `irmovlowq $0x8000, %rax` do not assemble because the constant is out of range
    
*  `lui IMMEDIATE, DESTINATION-REGISTER`: sets `DESTINATION-REGISTER` to `IMMEDIATE << 16` (left shift by 16)

*  `iaddq IMMEDIATE, DESTINATION-REGISTER`: adds signed 16-bit `IMMEDIATE` to `DESTINATION-REGISTER`

*  `iorq IMMEDIATE, DESTINATION-REGISTER`: adds unsigned 16-bit `IMMEDIATE` to `DESTINATION-REGISTER`

*  `isll IMMEDIATE, DESTINATION-REGISTER`: left-shift destination-register by `IMMEDIATE` (always positive) bits

## Question 5

Then consider the following assembly code:

    irmovq $0x12345678, %r10
    irmovq $0x9ABCDEF0, %r11
    irmovq $0x100000000, %r8
    irmovq $1, %r13
    irmovq $-1, %r14
    rrmovq %r11, %r12
    subq %r10, %r11
    andq %r10, %r12
    cmove %r14, %r13
    addq %r13, %r12
    xorq %r12, %r8

Compute and write in your answersheet:

*  (a) How large the original assembly's machine code was?
*  (b) How large would the original assembly's machine code be if `irmovq` had two encodings: one with 32-bit *unsigned* constants and one with 64-bit constants?
*  (c) To produce the best fixed-length assembly, what would be a good thing to replace each of the `irmovq` instructions with? You may use %rax a temporary register in your assembly. How long (in bytes) would the resulting assembly be?

<!-- FIXME: empirical analysis with real program and instruction sizes
    suppose constants X-Y take N instructions,
    constant distribution
    estimate size with this scheme versus size with storing constants in memory and loading them
-->


