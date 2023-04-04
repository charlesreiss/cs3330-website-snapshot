---
title: "Tip on safe removal"
...

Once you `rm`{.bash} something, it is gone;
recovery is spotty in practice and not something we'll be able to use.

An extra buffer, similar to most desktop OS's recycling bin, can be created by changing `rm`{.bash}
to an **alias** that doesn't actually delete but moves to a trashcan directory instead.

Create an alias.  We'll put this in a file called `.bashrc`, which is run each time you log into a bash terminal either in person or via `ssh`.

1.  Edit `$HOME/.bashrc` in your favorite editor.
    It likely already exists and contains code; we'll add our code after it.
    
2.  Create a trashing function in `.bashrc`:
    
    ````bash
    function trash_put() {
        while [ "$#" -gt 0 ]
        do
            if [ -e "$1" ]
            then
                to_delete="$(readlink -f "$1")"
                del_path="$(dirname "$to_delete")"
                del_name="$(basename "$to_delete")"
                now=$(date +%Y%m%d$H%M%s)
                mkdir -p $HOME/.trash/$now"$del_path"
                mv "$to_delete" $HOME/.trash/$now"$del_path"
            else
                echo "Cannot trash \`$1' (not a file or directory)"
            fi
            shift
        done
    }
    ````
        
    That is written in a language called Bash.
    Very useful to learn, but not within the scope of this course.
    
3.  Create an alias in `.bashrc`
    
    ````bash
    alias rm='trash_put'
    ````

Once you have done this, any bash terminal will move files instead of removing them when you type `rm`.
You can find the "deleted" files in `$HOME/.trash/date-of-deletion/original/absolute/path/to/file`.

