---
title: "HW: Bit Fiddling"
...

{:.changelog}
Changelog:

{:.changelog}
*  7 Feb 2023: reference "is any bit set?" part of lecture for `evenbitparity`


# Your Task

0.  Work on the [corresponding lab](bitlab.html) first to get familiar with bit puzzles generally.

1.  Go to the custom [code environment]({{site.submit_site}}/bitlab/){:target="_top"}
    and solve the homework problems.

    Note that there is partial credit if you violate some of the restrictions of a puzzle
    (like the operator count limit) but otherwise solve it.

# Hints

## Specific advice for the puzzles

*   The puzzles ***are not*** arranged in order of difficulty. You should not feel obliged to
    do them in order.

### `allevenbits`

*  A mask and emulating the `==` operator with subtraction will help. 

*  Recall that in two's complement, negation is flipping all bits and adding 1.

<!--
### `byteSwap`

*   Isolate the bits that are moving into their own variables,
    clear their destinations in the original number,
    then put them back in into the number in their new locations.
-->

### `getbits`

*  Use bitshifting to create a mask of an appropriate size.

*  Using a solution to `bottom` (from the lab) may be helpful.

### `fiveeighths`

*  You may assume that integer overflow for `+` acts as in two's complement.

*   Arithmetic right shift is equivalent to dividing a signed integer by a power of two *but always rounding down*. Integer division in C always rounds towards zero.

*   Section 2.3.6 ("Multiplying by Constants") and 2.3.7 ("Dividing by Powers of Two") in the textbook
    describes the overall solution strategy, including how to compensate for arithmetic right shift rounding differently than normal integer division.

*   If your initial solution idea has problems with loosing information about the fractional part of something/8, think about what would happen to the bits "after the decimal" point if they were preserved by the division (like if the result did not have to be an integer) and still around for the later operations.

*   Similarly, if your initial solution idea has problems with loosing information due to overflow from something*5, think about what happen to the extra bits if they were preserved by the multiplication (like if the result was bigger than 32 bits) and around for later operations.

*   For both types of cases where there are extra bits you want to track, one idea is to divide the input number into two pieces, one of which will include those extra bits.

### `addok`
*   Overflow with `+` will always produce a result with the wrong sign.

*   (non-negative) + (negative) can never overflow.
    
### `evenbitparity`

*  `^` is almost all you need.

*  To reach the desired operation count, you will probably need to ensure that you were computing useful values for multiple bits at a time when you do most `^` operations. The strategy used for "is any bit set" discussed in lecture is helpful.

