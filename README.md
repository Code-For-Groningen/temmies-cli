# temmies-cli
Command Line tool using the [temmies library](https://github.com/Code-For-Groningen/temmies)

## Installation
> [!NOTE]
> I am currently working on an arch linux package for this tool (AUR). Open an issue if I forget and/or you want me to package it for another distro. A bash script is also in the works.

```bash
pipx install temmies-cli
```

## Usage

### Initialize a new assignment
```bash
temmies init {year}/{course}/{assignment} {path}
```
> `temmies init 2024-2025/advalgo/labs-wk2 .`

### Optional args
- `-s` : Search for an assignment instead of providing the link i.e. `temmies init -s "Advanced Algorithms" `.

### File hierarchy example
Once the command is run.
```
 .
├── practical_1
│   │   .temmies <-- This file holds all relevant information
│   ├── pizza
│   │   ├── tcs
│   │   │   ├── 1.in
│   │   │   ├── 1.out
│   │   │   ├── 6.in
│   │   │   ├── 6.out
│   └── tunnel
│   │   ├── tcs
│   │   │   ├── 1.in
│   │   │   ├── 1.out
│   │   │   ├── 2.in
│   │   │   ├── 2.out
│   │   │   ├── 3.in
│   │   │   ├── 3.out
```

## `temmies submit {file}`
> `temmies submit main.c`
Submits a file to the relevant assignment. You can pass multiple files as well.

### Optional args
- `-q` : Quiet submission, don't wait for output

## `temmies status`

Shows an overview of the current assignment's status.

### Optional args
- `-d` : Adds some more detail

