# Module 00: Set up your workshop

**Time:** 2–3 hours · **Goal:** Python runs on your computer, this course runs, and your first test passes.

## Bakit ko 'to kailangan?

Every data engineering job starts the same way: clone a repo, create an environment, install packages, run tests. If this part scares you, everything after it will feel harder than it is. Do it once properly and you'll never think about it again.

**At work:** the developers on your projects do exactly this every day. Knowing it means you can run their code yourself instead of waiting for a demo.

---

## 1. Install the tools

### Python 3.12 (or newer)
1. Go to <https://www.python.org/downloads/> and download the latest Python 3.
2. **Windows:** on the first screen of the installer, tick **"Add python.exe to PATH"**. This is the step most people miss.
3. Open a new terminal and check:

```bash
# Windows (PowerShell)
py --version
# Mac / Linux
python3 --version
```

You should see `Python 3.12.x` or newer.

### VS Code
1. Install from <https://code.visualstudio.com/>.
2. Open VS Code → Extensions (Ctrl+Shift+X) → install **Python** (by Microsoft). It also installs Pylance.

### Git
1. Install from <https://git-scm.com/downloads>.
2. Tell Git who you are (once):

```bash
git config --global user.name "Miguel Jay Faustino"
git config --global user.email "migueljayfaustino@gmail.com"
```

---

## 2. The terminal, in 8 commands

The terminal is where you run Python scripts, install packages and use Git. You only need these to start:

| What you want | Windows (PowerShell) | Mac / Linux |
|---|---|---|
| Where am I? | `pwd` | `pwd` |
| List files | `ls` | `ls` |
| Go into a folder | `cd modules` | `cd modules` |
| Go up one folder | `cd ..` | `cd ..` |
| Make a folder | `mkdir output` | `mkdir output` |
| Run a Python file | `py script.py` | `python3 script.py` |
| Clear the screen | `cls` | `clear` |
| Stop a running program | `Ctrl+C` | `Ctrl+C` |

Tip: press **Tab** to auto-complete folder and file names.

---

## 3. Open the course and create a virtual environment

A **virtual environment** (venv) is a private box of packages for one project.

**Bakit:** different projects need different package versions. At work, one pipeline may need pandas 1.5 and another pandas 2.2. A venv stops them from breaking each other. Every DE project you join will use one.

In VS Code: **File → Open Folder** → choose `python-zero-to-de`. Then open the terminal (**Ctrl+`**) and run:

```bash
# Windows
py -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Your prompt now starts with `(.venv)`. That means it's active. **Activate it every time you open the course.**

If Windows says *"running scripts is disabled on this system"*, run this once, then try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Now install the course packages:

```bash
pip install -r requirements.txt
python data/generate_data.py
```

In VS Code, press **Ctrl+Shift+P → "Python: Select Interpreter"** and pick the one inside `.venv`.

---

## 4. How this course works

Every module folder has three files:

| File | What it is | Do you edit it? |
|---|---|---|
| `lesson.md` | Explanations, examples, the "bakit" | No, read it |
| `exercises.py` | Functions with `raise NotImplementedError` | **Yes, this is where you write code** |
| `test_exercises.py` | Automatic checks for your functions | No |

The loop for every exercise:

1. Read the function's docstring (the text in `"""triple quotes"""`). It has examples.
2. Delete `raise NotImplementedError` and write your code.
3. Run the checker:

```bash
python check.py 00      # check one module
python check.py         # see progress for the whole course
python check.py 03 -x   # stop at the first failure (useful when stuck)
```

4. Read the failure message, fix, repeat.

**Rule:** don't open the `solutions/` folder until you've passed a module or been stuck on one exercise for more than 45 minutes. Struggling for a while is the learning. Copying skips it.

---

## 5. The Python REPL: your scratchpad

Type `python` (Mac/Linux: `python3`) in the terminal and you get `>>>`. Try things here before putting them in a file:

```python
>>> 2 + 3
5
>>> "bar".upper()
'BAR'
>>> type(25.5)
<class 'float'>
>>> exit()
```

**Bakit:** professionals test small ideas in the REPL constantly. It's faster than running a whole script.

---

## 6. Reading an error message (the most important skill in this module)

```
Traceback (most recent call last):
  File "exercises.py", line 12, in greet
    return "Hello, " + nme
NameError: name 'nme' is not defined
```

Read from the **bottom up**:
1. Last line = **what** went wrong (`NameError`: a name Python doesn't know).
2. Line above = **where** (`exercises.py`, line 12).
3. Fix that line (a typo: `nme` should be `name`).

Most beginner errors are one of these: `NameError` (typo), `SyntaxError` (missing `:` or bracket), `IndentationError` (spaces wrong), `TypeError` (wrong type, like `"5" + 5`).

---

## 7. Git: save your progress

Make this course your public learning repo. Recruiters can see you practiced every week.

```bash
git init
git add .
git commit -m "Start Python for DE course"
```

Then create an empty repo on GitHub named `python-zero-to-de`, and follow the "push an existing repository" commands GitHub shows you.

After each module:

```bash
git add .
git commit -m "Complete module 03: data structures"
git push
```

**Bakit:** a green contribution graph and clear commit messages are evidence of consistency. Hiring managers for junior roles look for exactly that.

---

## Exercises (`exercises.py`)

1. `greet(name)` – your first function.
2. `minutes_to_hours(minutes)` – arithmetic and rounding.
3. `describe_me()` – return a dictionary about you. (You'll learn dictionaries properly in Module 03. Just follow the pattern.)

Run `python check.py 00`. When all three pass, you're set up.

## Done when
- [ ] `python --version` (or `py --version`) shows 3.12+
- [ ] `.venv` exists and you know how to activate it
- [ ] `python check.py 00` shows 3/3 passing
- [ ] The course is pushed to your GitHub
