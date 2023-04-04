---
title: "Lab: Bit Fiddling"
...

# Your Task

1.  Go to the custom [code environment]({{site.submit_site}}/bitlab){:target="_top"}.

2.  Solve as many of the "lab" puzzles as you can during the lab time (or in a roughly equivalent amount of time
    outside of lab).

    For each puzzle, you can write a series of C-like statements using only 32-bit `int`s,
    following the restrictions in the puzzle.

    We expect everyone to complete first two puzzles, and almost all to *complete* the first three.
    We expect very few students to attempt all six puzzles within the lab time.

    (For the lab, you do not need to complete all the puzzles;
    we intend to give full credit as long as your submissions to the coding environment are consistent
    with spending an appropriate amount of effort on the puzzles.)

3.  These puzzles should help you understand the following [homework](bithw.html), which, unlike
    the lab, must be completed individually and its entirety.

# Notes on the C-like environment

1.  You can create new variables by assigning to them like `int y = x + 1;` or just `y = x + 1;`.
    (Since all variables are `int`s, you don't need to specify types.)

2.  Integers use two's complement.

2.  Since all values are `int`s, all shifts are arithmetic.

3.  You cannot use control flow constructs like `if` or `while`.

2.  You can generally omit semicolons if you want.

# Hints

## Specific advice for the puzzles

*   The puzzles are arranged in approximate order of difficulty and build on each other.

### `thirdbits`

*   Use shifts to make the large constant from smaller parts.

### `bang`

*   In C, `!x` is equivalent to `x != 0` (since `0` is the only false value in C). (It is not a bitwise operator.)

*   You need to distinguish between `0` and non-zero values.

*   `0` is the only value where `x` and `-x` is non-negative.

*   It may help to remember how to negate numbers in two's complement.

*   The complement (`~x` = `x` with all bits flipped) operator can be helpful.

### `isequal`

*   The `^` (xor) operator is very helpful. In particular, consider what the value of `x^x` is.

*  Note that `!` is a permitted operator.

### `bottom`

*   Bitshifting a value with all 1s could be a good strategy.

*   Bitshifting a 32-bit value by 32 or more bits is undefined behavior. To deal with this restriction, one option would be doing what would otherwise be a 32-bit shift in two smaller shifts. For example, you could divide the shift amount into two pieces by dividing it by 2 and adding the remainder to one of the parts.

### `islessorequal`

*   The sign of `x - y` is a good starting point.

*   You may need special cases for overflow/underflow.

### `bitcount`

*  Use masks to select parts of the number and add those parts together.

*  Performing multiple operations in parallel like the "any bit set" example in the lecture slides (to be covered Thursday) will help stay under the operation limit.  Note that you can perform two additions in parallel in a similar matter to how we demonstrated performing multiple `|`s in parallel. For example, you can add `x=0x4+0x7` and `y=0x3+0x1` at the same time by performing the one addition `z=0x40003 + 0x70001`, then extracting `x` from the upper bits of `z` and `y` from the lower bits.

*  See also this end of this year's bitwise slides (which we probably won't get to until Thursday) or [last year's slides for 9 September](https://www.cs.virginia.edu/~cr4bd/3330/F2021/slides/20210909-slides.pdf) for an approach.
    Or see the Fall 2016's lecture notes from [Sep-01 12:30 lecture](https://www.cs.virginia.edu/luther/3330/F2016/notes.php?date=20160901) (near the end)
    and [Sep-06 3:30 lecture](https://www.cs.virginia.edu/luther/3330/F2016/notes.php?date=20160906) (near the beginning)
    for Prof Tychonievich's effort to explain the approach.
