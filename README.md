Overview
========

This program renames files to sequential number on a command line.

There are so many similar scripts out there, but the notable feature of this script is that it can undo the previous renaming.

I wanted this because I manage large number of photo images, which are not easy to backup with copy before invoking renaming.



Undoing
-------

After this program run, the working directory should contain a file `restore.py`, which will simply revert the renaming to restore previous state.

Be careful that doing the rename 2 or more times in the same directory will disable `restore.py` to restore original state. The restore script can only revert one invocation of the program.
