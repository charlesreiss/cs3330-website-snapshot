---
title: "Lists in C"
...

# Your Task

1.  Go to the coding site for homework [here]({{site.submit_site}}c/lab2.php){:target="_top"}.
    You will be assigned two random types of lists A and B. The website will provide you with skeleton code
    in which you need to complete implementations of the following functions:

    -   A function to convert an A list into a B list called `convert`.
    -   A function to append a *copy* of one B list to another B list. To allow you to modify the destination list,
        a pointer to it will be passed called `append`
    -   A function to remove all instances of a specified value from B list. To allow you to modify
        the destination list, a pointer to it will be passed called `remove_if_equal`.

    Except for the list your function appends to for `append` and the list your function remove elements 
    from for `remove_if_equal`,
    your functions should not modify any of the lists passed to them as arguments.

    Your code may only use the library functions `malloc`, `realloc`, `calloc`, `free`, and `printf`, which will be
    declared in the supplied skeleton code. Other functions will not be available, and you may not include
    header files in the coding environment.

    Refer to the instructions on the right sidebar for more details and/or see the information below.

2.  Submit your implementation of these functions on the website. You can use the editor in a web browser
    or you can download and upload files and test them on your own machine.

    Whenever you submit a solution, the website will show you results from our test suite.

3.  Make sure your submission passes all the tests. Once you have submitted a solution that passes all tests,
    you have full credit for the assignment. There is no seperate submission.
    If you do not pass all tests, we will give partial credit for your best submission.
    (We will choose the submission that gives you the best grade, taking into account our late policy.)

# Additional Advice

## Testing on our Environment

If you submit a file that contains a function `int main(int argc, char *argv[])` then that function will be run and you'll see anything it `printf`s, along with a summary of how you used `malloc` and `free`.

You can also download the file and test on your own machine.

## The types of lists

The homework assignment choses between the following types of lists:

-   Singly-linked lists, of form `struct node_t { TYPE payload; struct node_t *next; }`. If you are creating these,
you must use a seperate malloc() call for each element of the list.

-   Sentinel-terminated array, of form `TYPE *list;` with a given `TYPE sentinel;` where `list[numberOfElements] == sentinel`.  If you are creating these, you should use a single malloc call like `malloc(sizeof(TYPE)*(numberOfElements+1))` to allocate memory for it.

-   The size-and-pointer pair made popular in recent languages as the preferred implementation of a *dynamic array* or *range*, being a `struct range { unsigned int length; TYPE *ptr; }` The `ptr` field should be created with a single `malloc` call. The `length` field should contain the number of elements.
 
## Skeleton code pieces

Some header info to define the types and values we need:

````c
/* this bit of code lets the grader change the type used in the lists. 
 * It will be provided.
 * Your code should work for any integer type and sentinel. */
#ifndef TYPE
#define TYPE short;
TYPE sentinel = -1234;
#else
extern TYPE sentinel;
#endif
````

The types we'll deal with

````c
typedef struct node_t { TYPE payload; struct node_t *next; } node;
typedef struct range_t { unsigned int length; TYPE *ptr; } range;
````

Potential signatures for the functions you must implement:

````c    
node *convert(range list); /* from range to linked list */
TYPE *convert(range list); /* from range to array */
node *convert(TYPE *list); /* from array to linked list */
TYPE *convert(node *list); /* from linked list to array */
range convert(TYPE *list); /* from array to range */
range convert(node *list); /* from linked list to range */

void append(range *dest, range source); /* append range to range */
void append(TYPE **dest, TYPE *source); /* append sentinel array to sentinel array */
void append(node **dest, node *source);  /* append linked list to linked list */

void remove_if_equal(range *dest, TYPE value);
void remove_if_equal(TYPE **dest, TYPE value);
void remove_if_equal(node **dest, TYPE value);
````

For the `append` function, if the `dest` argument is a pointer to the list "1, 2, 3, 4, 5, 6"
and the `source` argument is the list "7, 8, 9", then after `append` returns, the
`dest` list should be changed to "1, 2, 3, 4, 5, 6, 7, 8, 9". New space should be allocated as
necessary with `malloc` or `realloc`. Any memory no longer used should be deallocated.

For the `remove_if_equal` function, if the `dest` argument is a pointer to the list "1, 2, 3, 1, 2, 3"
and the `value` argument is "2", then after `remove_if_equal` returns, the `dest` list shouuld
be changed to "1, 3, 1, 3".

Note that `malloc` (and `realloc`) may not initialize the memory they return. In particular, the
`malloc` in our testing environment deliberately ensures the memory is not zeroed.

## Intepreting AddressSanitizer errors

Our testing environment runs your code under AddressSanitizer to reliably catch memory errors.
This includes memory errors triggered by your code directly, and memory errors caused when our
testing code tries to traverse an malformed list.
We will show you a filtered version of the AddressSanitizer output, along with the name of
the test case that triggered it. 

For example, you might see some output like:

    =================================================================
    ==7816==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000ef90 at pc 0x4013e0 bp 0x7ffe30f15360 sp 0x7ffe30f15358
    WRITE of size 2 at 0x60200000ef90 thread T0
        #0 0x4013df in convert <your code>:93
        #1 0x403bd8 in rawCheckOneConvert <our testing code>:422
        #2 0x403367 in runForked <our testing code>:380
        #3 0x40438c in checkOneConvert <our testing code>:453
        #4 0x4043d7 in checkConvert <our testing code>:460
        #5 0x4056f7 in main <our testing code>:560
        #6 0x7f89b7b38f44 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21f44)
        #7 0x401148 (/var/www/html/cs3330/c/code/listsA2R/cr4bd-2018-01-26-105358-test.exe+0x401148)

    0x60200000ef91 is located 0 bytes to the right of 1-byte region [0x60200000ef90,0x60200000ef91)
    allocated by thread T0 here:
        #0 0x7f89b7f34862 in __interceptor_malloc (/usr/lib/x86_64-linux-gnu/libasan.so.1+0x54862)
        #1 0x40596c in malloc <library code>:21
        #2 0x40132a in convert <your code>:91
        #3 0x403bd8 in rawCheckOneConvert <our testing code>:422
        #4 0x403367 in runForked <our testing code>:380
        #5 0x40438c in checkOneConvert <our testing code>:453
        #6 0x4043d7 in checkConvert <our testing code>:460
        #7 0x4056f7 in main <our testing code>:560
        #8 0x7f89b7b38f44 in __libc_start_main (/lib/x86_64-linux-gnu/libc.so.6+0x21f44)

    SUMMARY: AddressSanitizer: heap-buffer-overflow <your code>:93 convert
    ==7816==ABORTING
    convert: empty list: crashed or returned malformed list (look for messages above)

This most likely means that a test called "convert: empty list" wrote out-of-bounds of an array at
line 93. The array which was accessed out-of-bounds was allocated at line 91.

Our autograder tests are divided into pieces, with each piece
run seperately, so we can give you partial credit if your code only crashes on some tests.

## Interpreting "wrong number of mallocs"

We count the number of times you call `malloc` and `free` and make sure it corresponds to what we
expect for the list you are producing. If you get this test failure message,
it probably means you are leaking memory. This could include leaking memory by not freeing up
memory allocated for an old list before replacing it with a new one. The message could
also mean you are allocating memory in way which doesn't make sense for the kind of list you are
creating &mdash; for example, allocating all nodes of a linked list in one `malloc` call (preventing
them from being `free`d individually).

## Basic hints and common problems

1.  To get the the length of the input list (for the `malloc` call):

    ````c
    int lengthOf(node *list) {
        int i=0; while(list) { list = (*list).next; i+=1; } return i;
    }
    int lengthOf(TYPE *list) {
        int i=0; while(list[i] != sentinel) i+=1; return i;
    }
    int lengthOf(range list) {
        return list.length;
    }
    ````

2.  To access the values from a list:

    ````c
        /* range */
        int i;
        for(i = 0; i < list.length; i += 1)
            doSomethingWith(list.ptr[i]);
        
        /* array */
        int i;
        for(i = 0; list[i] != sentinel; i += 1) 
            doSomethingWith(list[i]);

        /* linked-list */
        node *here;
        for(here = list; here; here = (*here).next) 
            doSomethingWith((*here).payload);
    ````

3.  `malloc()` might not initialize the memory it returns, so pointers in that memory may not start out as NULL.

4.  `*foo[1]` is the same as `*(foo[1])`, not `(*foo)[1]`

5.  If the function you are assigned to implement accepts a `TYPE **dest`, then your function should modify 
    the `TYPE*` at `*dest` rather than changing what `TYPE*` `dest` points to.

6.  It is possible for an error in the list you return (such as an allocation of the wrong size or a pointer
    to deallocated memory) to cause a crash in our testing code.
