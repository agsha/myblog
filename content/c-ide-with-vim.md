Date: 2016-05-02 10:20 pm
Tags: misc
Authors: Sharath Gururaj
Title: C IDE with vim, cscope and grep (ag)
disqus_identifier: c_ide


# Setup Cscope

* First, Install cscope. 
* Next, you need a `cscope.files` with all the files that need to be indexed. In the source folder, you can do that with  

        find `pwd` -name "*.c" -o -name "*.cc" -o -name "*.h" > cscope.files

    the `pwd` is needed instead of `.` because you need `find` to print absolute pathnames.

* Now, build the cscope database.

        cscope -q -R -b -i cscope.files 

     This command will build `cscope.out`. `-q` to build an efficient database, `-b` to build just the database. 

* Start up vim and issue the command

        :cs add ~/code/ceph/cscope.out

    which will add the cscope database. Vim has built in support for cscope in the form of the `:cs` command. But it does *not* have useful keybindings setup. For that, you need `cscopes_map.vim` (which I've sourced in the `.vimrc`). You're all set now. Some basic comands:

    * `C-\ s` to find a symbol 
    * `C-\ c` to find all callers
    * `C-\ f` to find global definitions
    * `:help cscope` for more

# Setup ctags

* Install ctags.
* cd to the source folder and build the ctags index with `ctags -R .` (`-R` is for recursive).
* In vim, you need to do `:set tags=/path/to/tags`. Unfortunately, you need to do this everytime you start vim. (how to avoid it?)
* use `C-]` to show a list of tags under the cursor. `C-o` or `C-t` to go back.


# Some Vim shortcuts I would like to remember:

* `[[` moves to the previous curly brace on column 0 (1?) 
* `Ctrl-O` and `Ctrl-I` last location before jump
* `[{` jump to begining of current block! (Or you can search backward for `{`!
