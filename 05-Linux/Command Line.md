
## About Shell
 
 A shell is a program that accepts commands you type, asks the operating system to run them, and then prints the result back to your terminal

Shell is not the same Terminal, it is two different components do different thing

## Terminal 

The **Terminal** (Terminal Emulator) is simply the application you interact with.


Examples include:

- GNOME Terminal
- Konsole 
- Kitty 
- Alacritty 
- WezTerm 


The Terminal is responsible for:
- Displaying a window. 
- Receiving keyboard input. 
- Displaying output on the screen. 
 
 
The Terminal **does not understand Linux commands**.
 When you type:
  ```bash ls ```
the Terminal simply sends the text to another program called the **Shell**.
      
> Think of the Terminal as a communication interface between you and the Shell.


so what's SHELL ??

## What's Shell

When learning Linux, one of the first concepts you'll encounter is the **Shell**.

Most beginners think that when they type a command like: ```bash ls ``` the operating system understands it directly.

That's **not** what actually happens.
There are several components working together to execute your command.

### How process done

you type a command, the execution flow looks like this: 

```text 
Keyboard
 │
 ▼ 
Terminal 
 │
 ▼
Shell 
 │ 
 ▼ 
Kernel 
 │ 
 ▼
Hardware 
```

---

After execution, the output travels back through the same path:

```text
Hardware
    │
    ▼
Kernel
    │
    ▼
Shell
    │
    ▼
Terminal
    │
    ▼
Screen
```

***Each component has a different responsibility.***
So also we can say that ***Terminal is the descriptor between user and shell***.

---

The **Shell** is a command interpreter.

Its job is to:

- Read the command.
- Parse it.
- Decide how it should be executed.
- Ask the Kernel to execute programs.
- Return the output to the Terminal.

The Shell is essentially the bridge between the **user** and the **operating system**.

---

## Why is it called a Shell?

The Kernel is the core of the operating system.

Users cannot interact with the Kernel directly.

Instead, they communicate through another program that surrounds the Kernel.

That program is called the **Shell**.

```text
+---------------------------+
|           User            |
+---------------------------+
              │
              ▼
+---------------------------+
|          Shell            |
+---------------------------+
              │
              ▼
+---------------------------+
|         Kernel            |
+---------------------------+
              │
              ▼
+---------------------------+
|        Hardware           |
+---------------------------+
```

The Shell hides the complexity of the Kernel and provides a user-friendly interface.

---

## Bash

Shell is not one, it's many type one of the most widely spread is ***Bash***.

It is the default shell on many Linux distributions and the most widely used shell in tutorials and scripts.

Learning Bash gives you a solid foundation before exploring other shells like Zsh or Fish.

---

### Shell Prompt

When you open a Terminal, you'll usually see something like this:

```bash
mostafa@arch:~$
```

Let's break it down.

```
mostafa
```

Current username.

```
@
```

Means "on".

```
arch
```

Hostname (computer name).

```
~
```

Current working directory.

`~` is a shortcut for your home directory.

Example:

```text
/home/mostafa
```

Finally:

```
$
```

This is called the **Prompt**.

It indicates that the Shell is waiting for your next command.

> Never type `$`; it is only a prompt symbol.

If you see:

```text
#
```

you are usually logged in as the **root** user.

---

### Command Structure

Most Linux commands follow this format:

```text
command [options] [arguments]
```

Example:

```bash
ls -l Downloads
```

Where:

- `ls` → Command
- `-l` → Option
- `Downloads` → Argument

---


## Commands 
### pwd (print working directory)

it's print the current directory that's shell is working on it (Full path from / to the current dir) 

#### Directory Tree in linux
The location of any file or directory is described by its path. A path is a sequence of directories that leads from a starting point to a specific destination.
```text
/
|-- bin
|   |-- file1
|   |-- file2
|-- etc
|   |-- file3
|   `-- directory1
|       |-- file4
|       `-- file5
|-- home
|-- var
```

---
### cd (change directory)

- Used to change current directory to another

#### Two different type of pathes

- **Absolute path**: The full path starting from the root directory (`/`). For example: `/home/pete/Desktop`.
```bash
cd /home/pete/Desktop
```

- **Relative path**: A path based on your current location. If you are in `/home/pete/Documents` and want to access a subdirectory named `taxes`, you can use `taxes/`.

```bash
cd taxes
```

---
#### Navigation Shortcuts

- `.` (current directory): Represents the directory you are currently in.

- `..` (parent directory): Moves you one level up to the directory containing your current one.

- `~` (home directory): A shortcut to your personal home directory, like `/home/pete`.

- `-` (previous directory): Takes you back to the last directory you were in.

```bash
cd .
cd ..
cd ~
cd -
```


### ls (list directories)

even it's shortcut for *list directories*, but it can used to list every thing in specified directory like files, dirs, text files and hidden files

```shell
ls -> list files of current dir
ls [abs path (/home/mostafa/Downloads) or relative path (mostafa/Downloads)] -> list files of specified dir
```


#### Options

- `ls -a` 
	Not all files in a directory are visible by default. In Linux, filenames that start with a dot(`.`) are hidden. You can view them with the `-a`option, which stands for all.
	```bash
	$ ls -a
	 . .. .bashrc Documents Pictures
	```

---

- `ls -l`
		***Getting Detailed Information*** ( file permissions, number of links, owner, group, size, modification time, and name)
	```
	pete@icebox:~$ ls -l
		total 80
		drwxr-x--- 7 pete penguingroup   4096 Nov 20 16:37 Desktop
		drwxr-x--- 2 pete penguingroup   4096 Oct 19 10:46  Documents
		drwxr-x--- 4 pete penguingroup   4096 Nov 20 09:30 Downloads
		drwxr-x--- 2 pete penguingroup   4096 Oct  7 13:13   Music
		drwxr-x--- 2 pete penguingroup   4096 Sep 21 14:02 Pictures
		drwxr-x--- 2 pete penguingroup   4096 Jul 27 12:41   Public
		drwxr-x--- 2 pete penguingroup   4096 Jul 27 12:41   Templates
		drwxr-x--- 2 pete penguingroup   4096 Jul 27 12:41   Videos
	```

***Other common options***

- `-h`: Show human-readable sizes with `-l`.
- `-r`: Reverse the sort order.
- `-t`: Sort by modification time.
- `-S`: Sort by file size.
- `-d`: List the directory itself instead of its contents.

### Touch 
The `touch` command is primarily used to **update a file's timestamps**. If the specified file does not exist, `touch` creates a new **empty file**.

#### Syntax

```bash
touch [OPTIONS] FILE...
```

#### Create Empty Files

```bash
touch notes.txt
```

Create multiple files at once:

```bash
touch file1.txt file2.txt README.md
```


#### Update Timestamps

If the file already exists, `touch` **does not modify its contents**. It only updates its timestamps (by default, to the current time).

```bash
touch notes.txt
```

#### Common Options

| Option      | Description                                |
| ----------- | ------------------------------------------ |
| `-a`        | Update access time (`atime`) only          |
| `-m`        | Update modification time (`mtime`) only    |
| `-c`        | Do not create the file if it doesn't exist |
| `-d "DATE"` | Set a specific date and time               |
| `-r FILE`   | Copy timestamps from another file          |

##### Examples

```bash
touch -c notes.txt
```

```bash
touch -d "2026-06-23 12:30:00" notes.txt
```

```bash
touch -r file1.txt file2.txt
```

#### Notes

- `touch` **does not write data** into a file.
- `touch` **does not overwrite** an existing file.
- Its primary purpose is updating timestamps; creating empty files is a common side effect.

> **Remember:**  
> If the file **doesn't exist**, `touch` creates it.  
> If the file **already exists**, `touch` only updates its timestamps.


### file

The `file` command is used to determine a file's **actual type** by inspecting its **contents**, not just its filename or extension.

#### Why is it Needed?

Unlike Windows, Linux does **not** rely on file extensions.

For example:

```text
image.jpg
notes
backup
funny.gif
```

A file named `funny.gif` doesn't have to be a GIF image, and `README` can be a plain text file without any extension.

To identify the real file type, use:

```bash
file <filename>
```

Example:

```bash
file banana.jpg
```

Output:

```text
banana.jpg: JPEG image data
```

---

#### Check Multiple Files

```bash
file notes.txt image.png archive.tar.gz
```

You can also use wildcards:

```bash
file *
```

---

#### Common Options

| Option | Description                             |
| ------ | --------------------------------------- |
| `-i`   | Show the file's MIME type               |
| `-b`   | Show only the file type (omit filename) |
| `-L`   | Follow symbolic links                   |
| `-z`   | Inspect compressed files                |

#### Examples

Show MIME type:

```bash
file -i index.html
```

Output:

```text
text/html; charset=us-ascii
```

Brief output:

```bash
file -b notes.txt
```

Output:

```text
ASCII text
```

---

#### Notes

- `file` examines the **contents** of a file, not just its extension.
- A file's extension can be misleading, but `file` usually identifies its real type.
- If the type cannot be determined, the output may simply be:

```text
data
```

meaning the file doesn't match any recognized format.

### cat

The `cat` (**concatenate**) command is used to **display**, **combine**, and **create** text files.

#### Syntax

```bash
cat [OPTIONS] FILE...
```

---

#### Display File Contents

Print the contents of a file to the terminal.

```bash
cat notes.txt
```

Display multiple files:

```bash
cat file1.txt file2.txt
```

---

#### Concatenate Files

Combine multiple files and display their contents sequentially.

```bash
cat dog.txt bird.txt
```

Save the combined output into a new file:

```bash
cat dog.txt bird.txt > animals.txt
```

---

#### Create a File

Create a new file and write text directly from the terminal.

```bash
cat > notes.txt
```

After typing the content, press **Ctrl + D** to save and exit.

Append text instead of overwriting:

```bash
cat >> notes.txt
```

---

#### Output Redirection

| Operator | Description                   |
| -------- | ----------------------------- |
| `>`      | Overwrite the file            |
| `>>`     | Append to the end of the file |

---

#### Common Options

| Option | Description                           |
| ------ | ------------------------------------- |
| `-n`   | Number all output lines               |
| `-b`   | Number only non-empty lines           |
| `-s`   | Squeeze multiple blank lines into one |
| `-A`   | Show non-printing characters          |

Examples:

```bash
cat -n script.sh
```

```bash
cat -b notes.txt
```

```bash
cat -s messy.txt
```

---

#### When Not to Use `cat`

`cat` is great for **small files**.

For large files, use:

```bash
less large-file.log
```

which allows scrolling, searching, and quitting without flooding the terminal.

---

#### Notes

- `cat` stands for **concatenate**.
- It prints file contents to **stdout**.
- `cat > file` creates or **overwrites** a file.
- `cat >> file` appends content to the end of a file.
- Press **Ctrl + D** to finish input when creating a file with `cat`.

### less

The `less` command is used to **view large text files** one page at a time without printing the entire file to the terminal.

Unlike `cat`, `less` allows you to **scroll**, **search**, and **navigate** through a file interactively.

#### Syntax

```bash
less [OPTIONS] FILE
```

Example:

```bash
less notes.txt
```

---

#### Navigation

| Key                     | Action                   |
| ----------------------- | ------------------------ |
| `↑` / `↓`               | Move one line up or down |
| `Page Up` / `Page Down` | Move one page            |
| `g`                     | Jump to the beginning    |
| `G`                     | Jump to the end          |
| `u`                     | Move half a page up      |
| `d`                     | Move half a page down    |
| `q`                     | Quit `less`              |
| `h`                     | Show help                |

---

#### Searching

Search forward:

```text
/search_term
```

Search backward:

```text
?search_term
```

After searching:

| Key | Action         |
| --- | -------------- |
| `n` | Next match     |
| `N` | Previous match |

---

#### Common Options

| Option | Description                               |
| ------ | ----------------------------------------- |
| `-N`   | Show line numbers                         |
| `+G`   | Open at the end of the file               |
| `+F`   | Follow new content (similar to `tail -f`) |

Examples:

```bash
less -N notes.txt
```

```bash
less +G logfile.log
```

```bash
less +F /var/log/syslog
```

---

#### Pipe Output to `less`

`less` can display the output of another command.

```bash
dmesg | less
```

This is useful when a command produces a large amount of output.

---

#### Notes

- Use `cat` for **small files**.
- Use `less` for **large files** or when you need to search and navigate.
- `less` opens files in **read-only mode**; it does not modify the file.
- Press `q` to exit and return to the shell.

### history

The `history` command displays a list of previously executed commands, allowing you to quickly review and reuse them.

#### Syntax

```bash
history
```

Example:

```text
101  pwd
102  ls -la
103  cat notes.txt
```

Each entry contains a **history number** and the executed command.

---

#### Re-run Previous Commands

| Shortcut | Description |
|----------|-------------|
| `↑` | Browse previous commands |
| `↓` | Browse newer commands |
| `!!` | Execute the last command |
| `!number` | Execute a command by its history number |
| `!prefix` | Execute the most recent command starting with `prefix` |

Examples:

```bash
!!
```

```bash
!102
```

```bash
!cat
```

---

#### Search History

Press:

```text
Ctrl + R
```

Start typing part of a command to search backward through your history.

- `Ctrl + R` → Next older match
- `Enter` → Execute the matched command
- `→` (Right Arrow) → Edit the command before running it

---

#### Manage History

Clear the current history list:

```bash
history -c
```

Delete a specific entry:

```bash
history -d 101
```

Write the current history to the history file:

```bash
history -w
```

History is usually stored in:

```text
~/.bash_history
```

---

#### Related Commands

Clear the terminal screen:

```bash
clear
```

> `clear` only clears the terminal display. It **does not** delete command history.

Use **Tab Completion** to autocomplete commands, filenames, and directories.

---

#### Notes

- `history` helps you reuse previously executed commands.
- `Ctrl + R` is one of the fastest ways to find old commands.
- Avoid typing passwords or secrets directly into commands, as they may be saved in your history.

### cp (Copy)
#### one file
```bash
cp [OPTIONS] SOURCE DESTINATION
```

#### more than one file
```bash
cp [OPTIONS] SOURCE1 SOURCE2 SOURCE3 DESTINATION
```
note : Destination must be only path with no file name

---
#### Options 
-  ```cp -r ``` copy recursively : to copy whole folder into another path (copy folder and it's content recursively)
- -i & -f & -n : **-i** when coping file to dst that has file with same name it **ask u would u like to replace** old with new , **-f force coping** with asking u and **-n prevent replacing file if exists**
- -p : preserve original metadata of file (nice at backups)
- -a : combination of -p -r (most used in backups) 
- -u : if file newer than that in dst or not exists 
- -v : show what is coping while coping process

---

#### mv Move File
#### one file
```bash
cp [OPTIONS] SOURCE DESTINATION
```

#### more than one file
```bash
cp [OPTIONS] SOURCE1 SOURCE2 SOURCE3 DESTINATION
```
note : Destination must be only path with no file name

---

#### Options 
-   -r move recursively : to copy whole folder into another path (copy folder and it's content recursively)
- -i & -f & -n : **-i** when moving file to dst that has file with same name it **ask u would u like to replace** old with new and **-n prevent replacing file if exists** 
- -v : show what is coping while coping process

### mkdir

The `mkdir` (**Make Directory**) command is used to create one or more directories.

#### Syntax

```bash
mkdir [OPTIONS] DIRECTORY...
```

---

#### Create a Directory

```bash
mkdir documents
```

---

#### Create Multiple Directories

```bash
mkdir books paintings projects
```

---

#### Create Nested Directories

Use `-p` to create parent directories if they don't exist.

```bash
mkdir -p projects/app/src
```

---

#### Set Permissions

Use `-m` to specify directory permissions.

```bash
mkdir -m 755 public
```

---

#### Common Options

| Option | Description |
|--------|-------------|
| `-p` | Create parent directories as needed |
| `-m MODE` | Set directory permissions |
| `-v` | Show each created directory |

Example:

```bash
mkdir -pv projects/app/src
```

---

#### Notes

- `mkdir` creates **directories**, not files.
- Use `touch` to create empty files.
- Without `-p`, creating a nested path whose parent doesn't exist will fail.
### rm

The `rm` (**Remove**) command is used to delete files and directories.

> **Warning:** `rm` permanently deletes files. They are **not** moved to the Trash.

#### Syntax

```bash
rm [OPTIONS] FILE...
```

---

#### Remove Files

Delete a single file:

```bash
rm file.txt
```

Delete multiple files:

```bash
rm file1.txt file2.txt
```

Delete files using wildcards:

```bash
rm *.tmp
```

> Preview wildcard matches first:

```bash
ls *.tmp
```

---

#### Remove Directories

Use `-r` (recursive) to remove a directory and everything inside it.

```bash
rm -r project/
```

To remove an **empty** directory only:

```bash
rmdir empty-directory
```

---

#### Common Options

| Option | Description |
|--------|-------------|
| `-r` / `-R` | Remove directories recursively |
| `-i` | Ask before deleting |
| `-f` | Force deletion without prompts |
| `-v` | Show removed files/directories |

Example:

```bash
rm -rv project/
```

---

#### Notes

- `rm` permanently deletes files.
- `rm -r` removes directories and their contents.
- `rm -rf` is very powerful and should be used with caution.
- Use `pwd` and `ls` to verify the target before deleting.
- Prefer `rmdir` when deleting empty directories.


### find

The `find` command is used to search for files and directories based on criteria such as **name**, **type**, **size**, and **modification time**.

#### Syntax

```bash
find [PATH] [EXPRESSION]
```

Example:

```bash
find /home -name "notes.txt"
```

---

#### Search by Name

```bash
find . -name "*.txt"
```

Case-insensitive search:

```bash
find . -iname "*.jpg"
```

---

#### Search by Type

Find regular files:

```bash
find . -type f
```

Find directories:

```bash
find . -type d
```

---

#### Search by Size

Files larger than 10 MB:

```bash
find . -type f -size +10M
```

Files smaller than 1 KB:

```bash
find . -type f -size -1k
```

---

#### Search by Modification Time

Modified within the last 7 days:

```bash
find . -type f -mtime -7
```

Modified more than 30 days ago:

```bash
find . -type f -mtime +30
```

---

#### Execute an Action

List details for each match:

```bash
find . -name "*.log" -exec ls -l {} \;
```

Delete matching files:

```bash
find . -name "*.log" -delete
```

> Always verify matches **before** using `-delete`.

---

#### Common Options

| Option | Description |
|--------|-------------|
| `-name` | Search by filename |
| `-iname` | Case-insensitive filename search |
| `-type f` | Search for regular files |
| `-type d` | Search for directories |
| `-size` | Search by file size |
| `-mtime` | Search by modification time |
| `-maxdepth` | Limit search depth |

---

#### Notes

- `find` searches **recursively** by default.
- Quote wildcard patterns (e.g., `"*.txt"`) to prevent shell expansion.
- `-exec` runs a command on each matching result.
- Be cautious when using `-delete`, as it permanently removes files.
### help

The `help` command displays help information for **Bash built-in commands**.

#### Syntax

```bash
help COMMAND
```

Example:

```bash
help cd
```

---

#### Bash Built-in Commands

`help` works only with commands built into the Bash shell, such as:

- `cd`
- `echo`
- `pwd`
- `history`

Example:

```bash
help history
```

---

#### External Commands

For external programs, use the `--help` option instead.

```bash
ls --help
```

Examples:

```bash
cp --help
```

```bash
find --help
```

---

#### Check Command Type

Use `type` to determine whether a command is a Bash built-in or an external program.

```bash
type cd
```

Output:

```text
cd is a shell builtin
```

```bash
type ls
```

Output:

```text
ls is /usr/bin/ls
```

---

#### Other Help Tools

| Command | Purpose |
|---------|---------|
| `help` | Help for Bash built-in commands |
| `COMMAND --help` | Quick usage summary |
| `man COMMAND` | Full manual page |
| `whatis COMMAND` | One-line command description |

---

#### Notes

- `help` works **only** for Bash built-in commands.
- Use `type` if you're unsure whether a command is built-in or external.
- For most external commands, `--help` is the quickest way to view available options.

### man

The `man` (**Manual**) command displays the official documentation (manual pages) for Linux commands and utilities.

#### Syntax

```bash
man COMMAND
```

Example:

```bash
man ls
```

---

#### Navigate Inside a Man Page

| Key                     | Action                 |
| ----------------------- | ---------------------- |
| `↑` / `↓`               | Scroll line by line    |
| `Page Up` / `Page Down` | Scroll by page         |
| `/text`                 | Search forward         |
| `n`                     | Next search result     |
| `N`                     | Previous search result |
| `q`                     | Quit                   |

---

#### Manual Sections

| Section | Description                    |
| ------- | ------------------------------ |
| `1`     | User commands                  |
| `2`     | System calls                   |
| `3`     | Library functions              |
| `5`     | File formats                   |
| `8`     | System administration commands |

Example:

```bash
man 1 passwd
```

```bash
man 5 passwd
```

---

#### Related Help Commands

| Command | Purpose |
|---------|---------|
| `help` | Help for Bash built-ins |
| `COMMAND --help` | Quick usage summary |
| `man` | Complete manual page |
| `whatis` | One-line command description |

---

#### Notes

- `man` provides detailed documentation for Linux commands.
- Use `/` to search inside a man page.
- Press `q` to exit.
- If no man page exists, try `COMMAND --help` or `help COMMAND`.

### whatis

The `whatis` command displays a **one-line description** of a command from its manual page.

#### Syntax

```bash
whatis COMMAND
```

Example:

```bash
whatis ls
```

Output:

```text
ls (1) - list directory contents
```

---

#### Related Commands

| Command | Purpose |
|---------|---------|
| `whatis` | One-line command description |
| `man` | Full manual page |
| `COMMAND --help` | Quick usage summary |
| `help` | Help for Bash built-ins |
| `apropos` | Search commands by keyword |

---

#### Notes

- `whatis` displays only a **brief description** of a command.
- The description comes from the **NAME** section of the command's man page.
- The number in parentheses (e.g., `(1)`) indicates the **manual section**.
- Use `man` if you need detailed documentation or command options.

### alias

The `alias` command creates **shortcuts** for commands or command sequences.

#### Syntax

```bash
alias NAME='COMMAND'
```

Example:

```bash
alias ll='ls -la'
```

Now:

```bash
ll
```

is equivalent to:

```bash
ls -la
```

---

#### Common Examples

```bash
alias ..='cd ..'
```

```bash
alias cls='clear'
```

```bash
alias grep='grep --color=auto'
```

---

#### Make an Alias Permanent

Add it to:

```text
~/.bashrc
```

Then reload the file:

```bash
source ~/.bashrc
```

---

#### Remove an Alias

```bash
unalias ll
```

---

#### List Aliases

```bash
alias
```

Check whether a command is an alias:

```bash
type ll
```

---

#### Notes

- Aliases are **temporary** unless saved in `~/.bashrc`.
- `unalias` removes an alias from the current session.
- Use `type` to check whether a command is an alias.
- Aliases are mainly for **interactive shell** usage, not scripts.
### exit

The `exit` command terminates the current shell session.

#### Syntax

```bash
exit
```

Exit with a specific status code:

```bash
exit 0
```

```bash
exit 1
```

---

#### Other Ways to Exit

Exit a login shell:

```bash
logout
```

Exit using the keyboard:

```text
Ctrl + D
```

---

#### Exit Status

| Status | Meaning |
|--------|---------|
| `0` | Success |
| Non-zero | Error or special condition |

---

#### Notes

- `exit` closes the current shell session.
- When using SSH, `exit` disconnects the remote session.
- `Ctrl + D` sends an **EOF (End Of File)** signal and usually exits the shell.
- `exit 0` and `exit 1` are commonly used in shell scripts.