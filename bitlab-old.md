---
title: "Lab: Bit Fiddling"
...

# Your Task

1.  Go to the custom [code environment]({{site.submit_site}}/bithw/bitlab.php){:target="_top"}.

2.  Solve as many of the puzzles as you can during the lab time (or in a roughly equivalent amount of time
    outside of lab) using a restricted subset of C (described below).
    We expect everyone to complete the first two puzzles, and most to *complete* the first three.
    We expect very few students to attempt all six puzzles within the lab time.

    (For the lab, you do not need to complete all the puzzles;
    we intend to give full credit as long as your submissions to the coding environment are consistent
    with spending an appropriate amount of effort on the puzzles. You can also spend additional
    time on the puzzles, but we do not intend to require this as long as your submissions show
    (by completing enough puzzles, or through attempts on puzzles you did not complete) you likely
    spent something similar to the required amount of time.)

3.  These puzzles should help you understand the following [homework](bithw.html), which, unlike
    the lab, must be completed individually and its entirety.

# The C Subset

1.  You are restricted to a subset of C

    - Constants cannot exceed a single byte (between 0 and 255, or 0x00 and 0xff)
    - You cannot have any control constructs (no `if`, `for`, etc)
    - You can only use `int`-type values. **You can use temporary variables and multiple statements**, and we encourage you to do this.
    - All temporary variables must be initialized on declaration (e.g. `int temporary = 0;`)
    - All `>>` operators are arithmetic shifts
    - Each puzzle has a limited set of operators you are allowed to use
    - Each puzzle has a limit on the number of operators you are allowed to use. Assignments to variables do not count towards this limit.

2.  Solutions violating any of the above rules *except* the number of operators will result in 0 points.
    A partial score is awarded if you have the correct functionality following
    all of the rules except the operator count. 

# Hints

## Testing outside the Coding environment

*   You can copy-and-paste code from the coding environment to your own computer for testing. 
    This can let you get useful compiler error messages and add `printf()` statements, etc.

## Specific advice for the puzzles

*   The puzzles are arranged in approximate order of difficulty and build on each other.

### `thirdBits`

*   Use shifts to make the large constant from smaller parts.

### `bang`

*   In C, `!x` is equivalent to `x != 0` (since `0` is the only false value in C). (It is not a bitwise operator.)

*   You need to distinguish between `0` and non-zero values.

*   `0` is the only value where `x` and `-x` is non-negative.

*   It may help to remember how to negate numbers in two's complement.

*   The complement (`~x` = `x` with all bits flipped) operator can be helpful.

### `isEqual`

*   The `^` (xor) operator is very helpful. In particular, consider what the value of `x^x` is.

### `bitMask`

*   Consider creating two masks of the form `0..01..1` with different numbers of `0`s, then combine them.

### `isLessOrEqual`

*   The sign of `x - y` is a good starting point.

*   You may need special cases for overflow/underflow.

### `bitCount`

*  Use masks to select parts of the number and add those parts together.

*  Performing multiple operations in parallel like the "any bit set" example in lecture will help stay under the operation limit.  Note that you can perform two additions in parallel in a similar matter to how we demonstrated performing multiple `|`s in parallel. For example, you can add `x=0x4+0x7` and `y=0x3+0x1` at the same time by performing the one addition `z=0x40003 + 0x70001`, then extracting `x` from the upper bits of `z` and `y` from the lower bits.

*  See also [this semester's slides for 9 September](slides/20210909-slides.pdf) or [Prof. Khan's slides from Spring 2017](https://www.cs.virginia.edu/~cr4bd/3330/S2017/notes/20170131am-slides-1up.pdf) (slide 43) for an approach.
    Or see the Fall 2016's lecture notes from [Sep-01 12:30 lecture](https://www.cs.virginia.edu/luther/3330/F2016/notes.php?date=20160901) (near the end)
    and [Sep-06 3:30 lecture](https://www.cs.virginia.edu/luther/3330/F2016/notes.php?date=20160906) (near the beginning)
    for Prof Tychonievich's effort to explain the approach.
