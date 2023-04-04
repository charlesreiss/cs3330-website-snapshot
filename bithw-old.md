---
title: "HW: Bit Fiddling"
...

{:.changelog}
Changelog:

{:.changelog}
*  8 September 2021: correct name of last puzzle to match coding environment
*  13 September 2021: refer to availability of lab solutions

# Your Task

0.  Work on the [corresponding lab](bitlab.html) first to get familiar with bit puzzles generally.
    *[added 13 September:]* Solutions to the lab are available on Collab under resources (posted after
    the lab was due) for you to reference.

1.  Go to the custom [code environment]({{site.submit_site}}/bithw/bithw.php){:target="_top"}.
    This is like the code environment for the lab, but with different problems.

2.  Solve ***all*** of the puzzles below using restricted subset of C (described below).

# The C Subset

1.  You are restricted to a subset of C

    - Constants cannot exceed a single byte (between 0 and 255, or 0x00 and 0xff)
    - You cannot have any control constructs (no `if`, `for`, etc)
    - You can only use `int`-type values. **You can use temporary variables and multiple statements**, and we encourage you to do this.
    - All temporary variables must be initialized on declaration (e.g. `int temporary = 0;`)
    - All `>>` operators are arithmetic shifts (regardless of the types involved)
    - Each puzzle has a limited set of operators you are allowed to use
    - Each puzzle has a limit on the number of operators you are allowed to use

2.  Violating any of the above rules *except* the number of operators will result in 0 points.
    Partial credit is awarded if you have the correct functionality following all of the rules except the operator count.

# Hints

## Testing outside the Coding environment

*   You can copy-and-paste code from the coding environment to your own computer for testing. 
    This can let you get useful compiler error messages and add `printf()` statements, etc.

## Specific advice for the puzzles

*   The puzzles ***are not*** arranged in order of difficulty. You should not feel obliged to
    do them in order.

### `allEvenBits`

*  A mask and emulating the `==` operator with subtraction will help. 

*  Recall that in two's complement, negation is flipping all bits and adding 1.

### `byteSwap`

*   Isolate the bits that are moving into their own variables,
    clear their destinations in the original number,
    then put them back in into the number in their new locations.

### `multFiveEighths`
*   Section 2.3.6 ("Multiplying by Constants") and 2.3.7 ("Dividing by Powers of Two") in the textbook
    have most of the solution described, if not explicitly given.

*   Arithmetic right shift is equivalent to dividing a signed integer by a power of two *but always rounding down*. Integer division in C always rounds towards zero.

### `addOK`
*   Overflow with `+` will always produce a result with the wrong sign.

*   (non-negative) + (negative) can never overflow.
    
### `evenBitParity`
*  `^` is almost all you need.

# Evaluation

Correctness points.
:   Each puzzle you must solve has been given a difficulty rating between 1 and 4 and is worth that many points.
    This is awarded all-or-nothing per puzzle: you either obeyed the coding rules and got all inputs correct or you did not.

Performance points.
:   There are an additional 2 points per puzzle that are awarded if you use a small number of operators.
    Again, this is all-or-nothing: you either met the limit or you did not.

Opt-in Competition
:   You may elect to provide a publicly visible name and have the operation counts of your working code
    logged on a competition scoreboard.

