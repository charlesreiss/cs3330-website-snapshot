---
title: OOO Exercise
...

> This assignment is subject to change.

<!-- TODO:
    *  here's some Y86 code
    *  identify when each instruction would be issued with simple OOO pipeline
-->

# Hypothetical OOO processor

For this assignment, we will consider an out-of-order processor which has two execution units for
arithmetic instructions, and one execution unit for memory instructions.

When instructions execute in this processor they are:

*  fetched, in one cycle up to two instructions at a time, in the order they appear in the program. For this exercise, we will assume that branch prediction is perfect.
*  decoded (including processing icodes and renaming registers, but not including reading registers) and placed in an instruction queue, in one cycle up to two instructions at a time, in the order they appear in the program
*  issued from the instruction queue when their operands are available. If multiple instructions all have their operands available, then the instructions that appeared earlier in the program are issued first. For simplicity, do not need to worry about the order in which memory instructions are issued.
*  executes instructions on each arithmetic execution unit in one cycle
*  executes instructions on the memory execution unit in three cycles in a pipelined manner (multiple memory instructions can be pending at once)
*  writes the results of instructions once they finish executing in the same cycle as when they finish executing. Instructions that depend on the values computed can be issued in the following cycle.
*  retires instrutions from the reorder buffer, up to two at a time, starting with the first instruction that was fetched. Instructions are only retired if all the instructions before them have already completed having their results written.

The processor has 15 logical registers `%r01` through `%r15`, but these are implemented using 64 physical registers and register renaming. We call the physical registers `%x01` through `%x63`.

We will show instructions in a three-argument form like:
    
    add %r01, %r02 -> %r03

this indicates to add %r01 and %r02 and put the result into %r03.

## Part 1: register renaming

<!-- FIXME: automated different examples for each student??? -->

Assume initially that `%r01` is assigned to `%x01`, `%r02` to `%x02`, and so on.
Registers `%x16` through `%x63` are available for register renaming.

Rewrite the following instructions using the `%x01` taking into account how register renaming
might occur that would allow all of these instructions to be placed in the instruction queue
at once:

    add %r01, %r01 -> %r01
    add %r02, %r01 -> %r01
    add %r03, %r01 -> %r01
    add %r04, %r01 -> %r01
    mrmovq 0x1234(%r05) -> %r02
    imul %r02, %r03 -> %r03
    mrmovq 0x1234(%r06) -> %r03
    imul %r02, %r04 -> %r04

Record your answer at TBD.


## Part 2: instruction dispatch

Suppose the instruction queue for this processor contains the following instructions
after renaming:

    A. add %x05, %x06 -> %x16
    B. sub %x16, %x07 -> %x17
    C. mrmovq 0x100(%x05) -> %x18
    D. imul %x17, %x09 -> %x19
    E. add %x05, %x07 -> %x20
    F. sub %x18, %x07 -> %x21
    G. add %x20, %x19 -> %x22
    H. mrmovq 0x200(%x22) -> %x23

Initially the value of registers `%x01` through `%x15` is available.


Complete the timeline to show how all the instructions can be issued and executed:

                    cycle 0    1    2   3    4    5   6
    execution unit:       
    arithmetic 1          A
    arithmetic 2          E
    memory stage 1        C
    memory stage 2             C
    memory stage 3                  C
    
Record your answer at TBD.

## Part 3: branch misprediction delay

## Part 4: effect of fetch/decode/... width
