---
title: Pipeline Simulation Exercise
...

# Your task

1.  Download the supplied program traces (<a href="files/pipesim/traces.tar.xz">link<a/> (last updated 27 October 2021); extract with `tar --xz -xvf traces.tar.xz`) and trace analysis tool (<a href="files/pipesim/time_trace.py">link</a>).

    The supplied trace analysis tool takes a *trace*, which is a record of all the instructions a program
    executes and counts how many cycles a pipelined processor similar to the one you produced for pipehw2
    would take to execute it, except it does not simulate stalling for `ret`.

    The supplied traces in a format described below. Rather than being a list of instructions, they are a list
    of attributes of instructions, like their source and destination registers, whether they are branches, etc.

2.  For the below questions, record your answers in the answer sheet [answer sheet]({{site.submit_site}}quizzes/quiz.php?qid=pipesim-hw).

    To save you time computing performance numbers, we'll only ask for statistics from the lapack-segsv and queens-8 traces, though we supply some additional ones. (Notably, the asumr trace is much smaller than the others.) For some problems, we'll supply expected results on simple traces to aid your debugging.

    When you are done, also upload all modifications you made to the trace analysis tool to the [submission site](https://kytos02.cs.virginia.edu/cs3330-spring2023/task.php?task=pipesim). Please make sure you include code for all
    the modifications needed throughout this assignment, though most of that code should be disabled by default.

3.  Using the supplied trace analysis tool identify
    how many times slower the programs is predicted to be when increasing the branch misprediction
    penalty (number of cycles wasted on branch misprediction, also known as the branch delay) from 2 to 3 cycles.
    You can do this with the command-line options in the tool.

    (Throughout this assignment, measure the performance by counting the number of cycles (since
    we don't give you enough information to make any other type of performance measurement).)

    Record your answers in the answer sheet.

4.  Modify the trace analysis tool to determine what the performance would be if conditional branches were
    not predicted at all and the processor instead stalled for 2 cycles (compared to the original version).

    When you do this, you should see the `jump-sample` trace increase from a total branch misprediction penalty
    of 2 cycles to 6 cycles.

    Record the differences in performance (between this and the original version of the processor)
    in the answer sheet.

5.  Suppose we had a processor that had a longer pipeline by splitting the execute stage into
    multiple stages. In this case, an instruction sequence like

        addq %rax, %rbx
        addq %rbx, %rcx

    would require stalling for one cycle in order to forward `%rbx`.

    Modify the trace tool to simulate this effect by assuming that a
    cycle of stalling (in addition to any cycles for load/use hazards)
    is required to read a value written by the previous instruction.
    <small>(In a real processor, probably not every operation would require both
    execute stages to retrieve a value, but to keep this simpler, please
    do not try to determine how "complicated" an instruction that writes
    a register is.)</small>

    When you do this, you should see the `data-dep-sample` trace require 2 stalls (instead of 0).

    Record the differences in performance (between this and the original version of the processor) from this change in the answer sheet.

6.  Suppose we had a processor that made branch predictions for conditional branches
    based on historical information. Your implementation should identify particular branch instructions
    by their `orig_pc` field. Then, rather than predicting branches to always be taken:
    *  if a particular branch instruction was executed earlier in the trace (there was
       a prior line of the trace which was a conditional branch with the same orig_pc field),
       predict the branch to be taken if it was taken the previous time it was executed
       and predict to be not taken if it was not taken the previous time.
    *  if the branch instruction was not executed before, predicts the branch to be taken

    Suppose that when the processor predicts a branch in this way, it can fetch the
    predicted instruction in the next cycle (like the processor we implemented for pipehw2).
    When the processor does not predict correctly,
    it results in two cycles being wasted fetching predicted instructions
    that will not be allowed to complete.
       
    (Your prediction
    should only be based on the actual outcome of the previous execution and should
    not take into account the prediction for the previous execution. So, for example,
    if the second time a branch instruction was executed it was not taken, you should predict
    the branch instruction to be not taken the third time regardless of what you predicted
    the second time the branch insturciton was executed.)

    When you do this, you should see `jump-sample2` change from having 350 cycles of branch delay to
    304 cycles of branch delay.

    Modify the trace tool to simulate this effect and record the differences in performance
    from this change (starting from the original version of the processor) in the answer sheet.

7.  In addition to your answers, remember to submit your modified trace analysis tool.

# Program trace format

The program trace files we supply are CSV (comma-separated value) files with one row for each
instruction executed and the following fields:

*  is_conditional_branch, is_constant_jump, is_computed_jump: `Y` if the program is that type of jump; `N` otherwise. In the trace, a Y86-like `call function_name` instruction is a constant jump and a Y86-like `ret` instruction is a computed jump.

*  srcA, srcB, dst: source and destination register numbers. If an instruction has no sources (e.g. load of a constant into a register), `srcA` and `srcB` will be left blank. If an instruction has no destination register (e.g.register-to-memory move), then `dst` will be left blank. If an instruction only has one source register, then one of `srcA` or `srcB` will be left blank.

*  is_memory_read, is_memory_write: `Y` if the instruction performs a data memory read/write; `N` otherwise.

*  mem_addr: address accessed by the data memory (blank if none).

*  branch_taken: `Y` if the instruction was a taken conditional branch; `N` if the instruction was a not-taken conditional branch; blank otherwise

*  orig_pc: the program counter of the instruction that produced this entry in the trace. In some case, one instruction in the original program was transformed into multiple instructions in the trace, so there may be multiple entries for one instruction execution.

There may also be fields other starting with `orig_` which give information
(that you are not expected to interpret) about the instructions from which the trace was generated. Depending on the trace, these are either Y86 instructions or RISC V instructions.
Note that this means that there may be some combinations of the fields above that would not be possible on Y86. (For example, RISC V's equivalent of the `call` instruction writes the return address to a register rather than memory.)

The supplied Python code extracts these instructions into dictionaries, so you can access the individual fields using code like `instruction['orig_pc']`.

For traces derived from Y86 instructions,
instructions that would write multiple registers (like `popq %rax`)
have been transformed into multiple instructions rather than adding a second `dst` field.

# Trace analysis tool

We supply `time_trace.py`. If you run `python3 time_trace.py --help`, you can see the options it takes.

On department machines, you should run `module load python` first to ensure that Python 3 is available.

The functions inside `time_trace.py` have comments that should help explain what they do and the limitations
of the simulation. The bulk of the work is done in the `count_time_in` function and this is where you
should expect to make any changes.

## Making modification conditional

I would suggest making modifications by adding new command-line arguments and then checking them
in `count_time_in`. You can look at how the existing code checks args.branch_delay
(the `--branch-delay` option) or args.load_use_hazard (the `--load-use-hazard` option) in `count_time_in`
and how the corresponding options are defined in `main()`.

Alternately, you could have changes controlled by a global flag or similar. Regardless, I would
strongly recommend making your changes in a way where it is easy to turn your changes on
and off without commenting or uncommenting code.
