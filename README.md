# temmies-cli
Command Line tool using the [temmies library](https://github.com/Code-For-Groningen/temmies)

## Installation
> [!NOTE]
> I am currently working on an arch linux package for this tool (AUR). Open an issue if I forget and/or you want me to package it for another distro. A bash script is also in the works.

```bash
pipx install temmies-cli
```

## Usage

## `temmies init <year>/<course>(/<assignment>) <path>`

### Initialize a new assignment
```bash
temmies init <year>/<course>/<assignment> <path>
```
> `temmies init 2024-2025/advalgo/labs-wk2 .`

### Initializing an entire course
```bash
temmies init <year>/<course>
```
### Optional args
- `-s` : Search for an assignment instead of providing the link i.e. `temmies init -s "Advanced Algorithms" `.
- `-t <path>`: Specify where you want your tests to be (relative to the parent of each assignment folder). Default is `.`.

### File hierarchy example
Once the command is ran:
```
 .
├── practical_1
│   ├── pizza
|   |   | .temmies <-- This is the temmies file which lets you do `temmies submit`
│   │   ├── tcs
│   │   │   ├── 1.in
│   │   │   ├── 1.out
│   │   │   ├── 6.in
│   │   │   ├── 6.out
│   └── tunnel
|   |   | .temmies <-- there's one of these in each assignment folder
│   │   ├── tcs
│   │   │   ├── 1.in
│   │   │   ├── 1.out
│   │   │   ├── 2.in
│   │   │   ├── 2.out
│   │   │   ├── 3.in
│   │   │   ├── 3.out
```

## `temmies submit <file>`
> `temmies submit main.c`
Submits a file to the relevant assignment. You can pass multiple files as well.

### Optional args
- `-q` : Quiet submission, don't wait for output

## `temmies status`

Shows an overview of the current assignment's status.

### Optional args
- `-d` : Adds some more detail (i.e. the leading submission)

