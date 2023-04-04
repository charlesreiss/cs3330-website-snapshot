---
title: "Using SSH and SCP"
...

{:.changelog}
Changelog:

{:.changelog}
*  24 Aug 2022: add note about trying password reset for students who may already have an account


The most reliable single approach to using a POSIX system similar to the department machines is to use the department machines.  This can be done can be done remotely using a **s**ecure **sh**ell and a **s**ecure **c**o**p**y or by using remote desktop via the NoMachine software. (We believe remote desktop option is probably most convenient.)

Tools exist for using these on just about all operating systems.

> If you had a department account last semester, you should still have a department account this
> semester. If you aren't sure if you have an account, try the password reset advice below.
> For others students, accounts will be created by the second week of class; see your
> email for the initial password. (Look for an email sent from `cshelpdesk` and, for most students,
> the week before classes started.)

> To reset your password, use the password reset tool at [https://www.cs.virginia.edu/PasswordReset/](https://www.cs.virginia.edu/PasswordReset/). (This tool may not work unless your account was setup (at some point) to have its initial temporary password changed.)

About software on the department machines
==========================

The department machines use a "module" system to load software, like C compilers. See [this guide](files/UVA_linux_environment_modules.pdf) for using that
to load more recent versions of compilers, etc. when using them.

Remote Desktop on Windows, Mac, or Linux
============
You can use remote desktop to the UVa computer science department Linux environment
using the NoMachine client. See 
[this document](files/NX-Setup_v3A.pdf)
for instructions. 

*This will give you a persistent environment to work on the department machines, even if you disconnect.*

SSH on Windows
=======

1.	Download [PuTTY](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) (get the `putty.exe` file)

2.	Run the `putty.exe`

3.	In the "Host name" field type `portal.cs.virginia.edu`.

4.	When prompted, give your lab account username and password (you won't see the password as you type)

At the end of this you will have a terminal running on a lab machine. You won't be able to open windows (try `nano`, `emacs` or `vim` if you need an editor) but you can use `cd`, `gcc`, `./a.out`, `./driver.pl`, and so on.

Windows (without the Windows Subsystem for Linux) is pretty nerfed when it comes to open-source tools. You can try the `pscp.exe` or `psftp.exe` from the PuTTY site, but results vary.  See [Files to-and-from lab machines] for how to use p`scp`.


SSH in Chrome
======

I have had reports that [this chrome extension](https://chrome.google.com/webstore/detail/sshinatab/eooeadjobbbigamjlmofdhdjofjhahkd) works well for ssh, though I have not used it myself.


SSH on Mac, Linux, FreeBSD, OpenBSD, Haiku, etc.
=========================================

`ssh`, `scp`, `sftp`, `rsync`, and the like are installed by default.

## Working on lab machines remotely

1.	Open a terminal

2.	Type `ssh mst3k@portal.cs.virginia.edu` (where `mst3k` is your user ID)

3.	Type your lab account password (you won't see it as you type)

At the end of this you will have a terminal running on a lab machine.
You won't be able to open windows (try `nano`, `emacs` or `vim` if you need an editor) but you can use `cd`, `gcc`, `./a.out`, `./driver.pl`, and so on.

## Files to-and-from lab machines

1.	Open a terminal

2.	`cd` to the directory you want to share

3.	To send a single file (where `mst3k` is your computing ID):

		scp localFile.c mst3k@portal.cs.virginia.edu:~/remote/path/
	
	To retrieve a single file:
	
		scp mst3k@portal.cs.virginia.edu:~/remote/path/filename.c ./
	
	Note those are tildes `~` not hyphens `-`; the tilde stands for "my home directory on that machine".
	
For more complicated file moves, try `sftp` or `rsync`.  Learn more with `man sftp` or `man rsync`.


Cross-platform File Transfer with FileZilla
===========================================

If you have trouble with `scp`, you might try [FileZilla](https://filezilla-project.org).

1. Download and install the FileZilla Client
2. Run FileZilla
3. The top left icon is the "site manager"; click it
4. If you already set up a site, you can reuse it; otherwise create a New Site
	1. Host `portal.cs.virginia.edu`
	2. Protocol "SFTP"
	3. Logon Type "Ask for password"
	4. User `mst3k` --- your computing id
	5. Connect ()
5. In the FileZilla window you have your local directory in the left pane and the labunix directory in the right pane.  Navigate to the files you want to move, then drag and drop.




Hint on changing passwords
==========================

Remember, once you log in to a linux machine, in person or remotely, you can change your password by typing (where `mst3k` is your user ID)

    kpasswd mst3k

> Due to a current issue with the password management server, password changes may not take effect for several hours after running `kpasswd`.  This will be changed at some point, but probably not until after you've all set your passwords for the semester.
