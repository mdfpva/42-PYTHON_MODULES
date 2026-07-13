<div align="center">

```
 ___       _          _          _    _     _    _
|   \ __ _| |_ __ _  /_\  _ _ __| |_ (_)_ _(_)__| |_
| |) / _` |  _/ _` |/ _ \| '_/ _| ' \| \ V / (_-<  _|
|___/\__,_|\__\__,_/_/ \_\_| \__|_||_|_|\_/|_/__/\__|
                                    💾 42 💾
```

### 🗄️ Digital Preservation in the Cyber Archives 🗄️

**A 42 School Project — Python Piscine, File I/O Module**

*Preserve digital knowledge by mastering file operations, managing data
streams, and building robust archival systems that protect information.*

`Version 3.0` · `Python 3.10+` · `flake8 compliant` · `mypy checked`

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Concepts Covered (Theory)](#-concepts-covered-theory)
  - [1. Files and `open()`](#1-files-and-open)
  - [2. File Objects and `typing.IO`](#2-file-objects-and-typingio)
  - [3. Open Modes: read vs write](#3-open-modes-read-vs-write)
  - [4. Reading: `read()` and `readline()`](#4-reading-read-and-readline)
  - [5. Writing: `write()`](#5-writing-write)
  - [6. Why `close()` Matters](#6-why-close-matters)
  - [7. File Errors: the `OSError` Family](#7-file-errors-the-oserror-family)
  - [8. The Three Standard Streams](#8-the-three-standard-streams)
  - [9. Writing to stderr](#9-writing-to-stderr)
  - [10. Reading stdin Without `input()`](#10-reading-stdin-without-input)
  - [11. Buffering and `flush()`](#11-buffering-and-flush)
  - [12. The `with` Statement (Context Managers)](#12-the-with-statement-context-managers)
  - [13. Designing a Safe API: `(bool, str)` Result Tuples](#13-designing-a-safe-api-bool-str-result-tuples)
  - [14. Optional Parameters and Default Values](#14-optional-parameters-and-default-values)
- [Project Structure](#-project-structure)
- [Exercises](#-exercises)
- [Usage](#-usage)
- [Testing & Linting](#-testing--linting)
- [Key Constraints](#-key-constraints)
- [Resources](#-resources)
- [Author](#-author)

---

## 🌍 About the Project

**Data Archivist** is the file I/O module of the 42 Python branch. Set in
the Cyber Archives of 2087 — where data is humanity's greatest treasure and
every byte saved is a victory against oblivion — it teaches the complete
lifecycle of file operations: **open**, **read**, **write**, **close**, the
three **standard streams**, and finally the `with` statement that makes
resource handling automatic.

A deliberate pedagogical constraint shapes the module: **the `with`
statement is forbidden until exercise 3.** You first manage files by hand
(`open`/`close` + exception handling), *feel* the fragility of that pattern,
and only then are handed the tool that solves it — so you understand
exactly what `with` automates.

---

## 🧠 Concepts Covered (Theory)

### 1. Files and `open()`

`open(path, mode)` asks the operating system for access to a file and
returns a **file object** — Python's handle on the underlying OS resource:

```python
file = open("ancient_fragment.txt", "r")   # may raise OSError!
content = file.read()
file.close()
```

`open()` is the moment of truth: the file may not exist, permissions may
forbid access, the path may be a directory. That's why file code and
exception handling are inseparable — this whole module is the exception
module applied to real resources.

### 2. File Objects and `typing.IO`

The answer to the subject's question — *what is the type of the data
returned by `open()`?* — is: a **file object** (for text mode, an
`io.TextIOWrapper`). For type hints, the `typing` module provides the
generic interface:

```python
from typing import IO   # (subject authorizes typing.IO)

def read_all(file: IO[str]) -> str:
    return file.read()
```

`IO[str]` means "a stream of `str`" (text mode); `IO[bytes]` would be a
binary stream. The file object bundles state (position in the file, open
or closed) with methods (`read`, `readline`, `write`, `flush`, `close`) —
it's a class instance like any other, which is why the streams of ex2 can
be used identically.

### 3. Open Modes: read vs write

The `mode` string tells `open()` your intent:

| Mode | Meaning | If file exists | If file missing |
|------|---------|----------------|-----------------|
| `"r"` | read (default) | reads it | `FileNotFoundError` |
| `"w"` | write | **truncated to empty** | created |
| `"a"` | append | writes at the end | created |

ex1's requirement — *create the file or replace it if it already exists* —
is exactly `"w"` semantics. The destructive side of `"w"` (instant
truncation on open) is worth respecting: opening for write is already a
modification.

### 4. Reading: `read()` and `readline()`

```python
content = file.read()       # the WHOLE file as one string ('\n' included)
line = file.readline()      # one line, keeping its trailing '\n'
```

- `read()` is the right tool here: small files, need everything —
  displaying it reproduces `cat`.
- `readline()` returns `""` (empty string) at end of file — that's the EOF
  signal.
- The file object keeps a **cursor**: successive reads continue where the
  previous one stopped.
- Line-by-line transformation (ex1's trailing `#`) works from `read()` +
  `str.split("\n")`, or by iterating — string methods are always allowed.

### 5. Writing: `write()`

```python
out = open("new_fragment.txt", "w")
out.write(transformed)      # writes EXACTLY what you pass — no newline added
out.close()
```

Unlike `print()`, `write()` appends **nothing**: newlines are your job.
`write()` returns the number of characters written (usually ignored). One
big string or several successive `write()` calls are equivalent — the
cursor advances after each.

### 6. Why `close()` Matters

`close()` releases the OS resource and **flushes** any buffered data to
disk. Skipping it risks:

- **data loss** — buffered writes that never reach the disk;
- **resource leaks** — file descriptors are finite; long-running programs
  that leak them eventually can't open anything;
- **locked files** on some systems.

The subtle bug this module makes you confront in ex0–ex2: with manual
handling, the `close()` must happen on **every** path — success *and*
failure. Done by hand, that means careful `try/except` structuring (and
noticing that a file that failed to *open* doesn't need closing — there's
nothing to close). This pain is deliberate: it's the setup for ex3.

### 7. File Errors: the `OSError` Family

File operations raise subclasses of **`OSError`**, each carrying an
`errno` and a clear message:

| Exception | errno | Typical cause |
|-----------|-------|---------------|
| `FileNotFoundError` | 2 | path doesn't exist |
| `PermissionError` | 13 | no read/write rights (`/etc/master.passwd`) |
| `IsADirectoryError` | 21 | path is a directory |

Catching `OSError` covers the whole family at once (hierarchy catching,
straight from the exceptions module). The expected outputs forward the
original message — `[Errno 2] No such file or directory: 'foo'` — which is
just `f"Error opening file '{name}': {e}"` with the caught exception.

### 8. The Three Standard Streams

Every process is born with three pre-opened channels — *older than the
Internet itself*, inherited from Unix:

| Stream | fd | Python | Purpose |
|--------|----|--------|---------|
| standard input | 0 | `sys.stdin` | data **in** (keyboard, pipes) |
| standard output | 1 | `sys.stdout` | normal results |
| standard error | 2 | `sys.stderr` | errors & diagnostics |

They are **file objects** (`IO[str]`) like any other — same `read`,
`readline`, `write` interface. `print()` writes to `sys.stdout`;
`input()` reads from `sys.stdin`. The module's point: those builtins are
*conveniences over streams you can drive directly*.

### 9. Writing to stderr

Separating errors from results is what makes programs **composable**:
redirect or pipe stdout (`> out.txt`, `| grep ...`) and error messages
still reach the terminal. Two equivalent idioms:

```python
print(f"[STDERR] Error opening file '{name}': {e}", file=sys.stderr)
sys.stderr.write(f"[STDERR] Error opening file '{name}': {e}\n")
```

`print(..., file=...)` shows that print *always* targeted a stream — the
default just happens to be stdout. Verify the separation with
`python3 ft_stream_management.py foo 2>/dev/null` (the `[STDERR]` line
disappears) — a likely defense demo.

### 10. Reading stdin Without `input()`

`input()` ≈ `sys.stdin.readline()` minus the trailing newline, plus a
prompt. Rebuilt from streams:

```python
sys.stdout.write("Enter new file name (or empty): ")
sys.stdout.flush()                      # prompt has no '\n' -> force it out
name = sys.stdin.readline().strip()    # readline keeps '\n'; strip it
```

Two details make this exercise: the **flush** (see below) and the
**trailing newline** that `readline()` keeps but `input()` strips —
forget the `.strip()` and every filename ends in `\n`.

### 11. Buffering and `flush()`

Streams **buffer**: written text sits in memory and reaches the terminal
or disk later (stdout is typically line-buffered on a terminal — it flushes
on `\n`). A prompt without a newline can therefore stay invisible while
the program already waits on stdin. `flush()` forces the buffer out
**now**:

```python
sys.stdout.write("Enter new file name (or empty): ")
sys.stdout.flush()    # without this, the user may stare at a blank line
```

Buffering exists for performance (syscalls are expensive; batching is
cheap); `flush()` is the manual override for the moments ordering matters.

### 12. The `with` Statement (Context Managers)

The payoff of the module. A **context manager** is an object that defines
setup and teardown; `with` guarantees the teardown runs:

```python
with open(filename, "r") as file:
    content = file.read()
# file is CLOSED here — success, exception, or early return
```

- On entering, `open(...)` runs and the file binds to `file`.
- On leaving the block **for any reason** — normal completion, an
  exception flying out, a `return` — Python calls the file's cleanup,
  which closes it.
- It's the `try/finally: close()` pattern from the exceptions module,
  packaged into syntax. What you wrote by hand in ex0–ex2 is what `with`
  does for you in ex3 — and *that* is why the subject banned it until now.
- Note `with` **replaces the close, not the error handling**: a failing
  `open()` raises *before* the block starts, so `try/except OSError`
  wraps the `with`.

```python
def secure_archive(filename: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as file:
                return (True, file.read())
        with open(filename, "w") as file:
            file.write(content)
            return (True, "Content successfully written to file")
    except OSError as e:
        return (False, str(e))
```

### 13. Designing a Safe API: `(bool, str)` Result Tuples

`secure_archive()` never raises — it **returns** the outcome as a tuple
`(success, payload)`:

- `(True, file_contents)` or `(True, confirmation_message)` on success;
- `(False, error_message)` on failure — the exception converted to data
  with `str(e)`.

This is the *result-value* style of error handling (the norm in Go, and in
Python at API boundaries): the caller can't forget to handle failure,
because the boolean must be inspected to use the payload. Compare with
raising: exceptions suit deep call stacks; result tuples suit simple
"try this, tell me how it went" utilities. Knowing **both** — and when to
use which — is the design lesson of the exercise.

### 14. Optional Parameters and Default Values

The `secure_archive()` signature relies on **default parameter values**:

```python
def secure_archive(filename: str, action: str = "read",
                   content: str = "") -> tuple[bool, str]:
```

- `filename` is mandatory; `action` and `content` are optional — callers
  provide only what they need: `secure_archive("f.txt")` reads,
  `secure_archive("f.txt", "write", data)` writes.
- Defaults are evaluated **once**, at definition time — safe with immutable
  defaults like `str`; a classic Python pitfall with mutable ones (never
  `def f(x=[])`).
- The subject leaves the `action` type to you (`int` or `str`); a `str`
  like `"read"`/`"write"` self-documents at every call site.

---

## 📂 Project Structure

```
data_archivist/
├── ex0/
│   └── ft_ancient_text.py        # open/read/close by hand, cat clone
├── ex1/
│   └── ft_archive_creation.py    # + transform lines, write mode
├── ex2/
│   └── ft_stream_management.py   # stderr for errors, stdin without input()
└── ex3/
    └── ft_vault_security.py      # with statement, (bool, str) API
```

---

## 🌾 Exercises

| Ex  | File | Authorized | Concepts |
|-----|------|------------|----------|
| 0 | `ft_ancient_text.py` | `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.close()`, `print()` | Manual open→read→close, usage line, `FileNotFoundError` / `PermissionError` |
| 1 | `ft_archive_creation.py` | + `io.write()`, `input()` | Write mode (`"w"` creates/replaces), `#` appended per line, optional save |
| 2 | `ft_stream_management.py` | + `sys.stdin`, `sys.stdout`, `sys.stderr`, `io.readline()`, `io.flush()` (− `input()`) | Errors → stderr with `[STDERR]` prefix, prompt via stdout+flush, read via `stdin.readline()` |
| 3 | `ft_vault_security.py` | `open()`, `read()`, `write()`, `print()` | `with` statement, `secure_archive() -> tuple[bool, str]`, defaults |

**Progression logic:** ex0 reads by hand, ex1 adds writing, ex2 reveals
that stdin/stdout/stderr are just three more file objects, and ex3 replaces
the whole manual close discipline with `with` — introduced *last, on
purpose*, so its value is earned rather than assumed.

---

## 🚀 Usage

```bash
# ex0 — a cat clone with archive framing
python3 ex0/ft_ancient_text.py ancient_fragment.txt

# ex2 — errors go to fd 2; prove it:
python3 ex2/ft_stream_management.py foo 2>/dev/null   # [STDERR] line vanishes

# ex3 — self-running demo of secure_archive()
python3 ex3/ft_vault_security.py
```

```
=== Cyber Archives Security ===

Using 'secure_archive' to read from a nonexistent file:
(False, "[Errno 2] No such file or directory: '/not/existing/file'")

Using 'secure_archive' to read from a regular file:
(True, '[FRAGMENT 001] Digital preservation protocols established 2087\n...')

Using 'secure_archive' to write previous content to a new file:
(True, 'Content successfully written to file')
```

---

## ✅ Testing & Linting

```bash
flake8 .
mypy ex0/ ex1/ ex2/ ex3/
```

---

## ⚠️ Key Constraints

- Python **3.10+**, flake8-clean, **type hints everywhere** (mypy-checked).
- Exceptions handled gracefully — no crashes, ever.
- **`with` is forbidden before ex3** — ex0–ex2 manage `close()` manually.
- Allowed baseline everywhere: `str`, `int`, `float`, `list`, `dict`,
  `set`, `tuple` and all their methods.
- Output messages may be customized as long as the essential information
  (structure, filenames, forwarded error text) is preserved.
- ex0: no argument → usage line; a file that failed to open must not be
  closed.
- ex1: saving is optional — empty filename means "Not saving data.";
  target file is created or replaced.
- ex2: every exception message goes to **stderr** with a clear prefix;
  user input read from `sys.stdin` (no `input()`), prompt flushed.
- ex3: `secure_archive()` returns `(True|False, str)`; mandatory filename,
  optional action (read/write), optional content — the code structure is
  reviewed against this signature at defense.
- Be ready to explain: the type returned by `open()`, what `"w"` does to
  an existing file, why stderr exists, what `with` replaces (and what it
  doesn't).

---

## 📚 Resources

- [Reading and Writing Files — official tutorial](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [`open()` built-in](https://docs.python.org/3/library/functions.html#open)
- [`io` module — streams](https://docs.python.org/3/library/io.html)
- [`sys.stdin` / `stdout` / `stderr`](https://docs.python.org/3/library/sys.html#sys.stdin)
- [The `with` statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
- [OS exceptions hierarchy](https://docs.python.org/3/library/exceptions.html#os-exceptions)

---

## 👤 Author

**mide-fre** — student at [42 Porto](https://www.42porto.com/)
GitHub: [@mdfpva](https://github.com/mdfpva)

### 🤖 AI Usage Disclosure

AI tools were used in accordance with the 42 AI guidelines: as a support for
understanding concepts, reviewing code, and producing documentation. All
submitted solutions are my own work, fully understood and defensible during
peer evaluation.

---

<div align="center">

*Made with 💾 at 42 Porto*

</div>
