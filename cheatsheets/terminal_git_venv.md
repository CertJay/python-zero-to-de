# Terminal, Git and virtual environment cheat sheet

## Virtual environment
```bash
py -m venv .venv            # Windows (Mac/Linux: python3 -m venv .venv)
.venv\Scripts\activate      # Windows (Mac/Linux: source .venv/bin/activate)
deactivate
pip install -r requirements.txt
pip freeze > requirements.txt
```

## Course
```bash
python check.py             # all progress
python check.py 05          # one module
python check.py 05 -x       # stop at first failure
python data/generate_data.py
```

## Git: the daily loop
```bash
git status                  # what changed?
git add .                   # stage everything
git commit -m "Complete module 05: regex log parser"
git push
git log --oneline -10       # recent history
git diff                    # unstaged changes
git restore file.py         # throw away changes to a file
```

## Git: branches (for bigger changes)
```bash
git switch -c feature/serve-tables
# ...work, commit...
git switch main
git merge feature/serve-tables
```

## Good commit messages
- `Add outlet normalization with mapping table`
- `Quarantine charges with unknown guest_id`
- `Fix day-first date parsing for 12/10/2026`

Not: `update`, `fix`, `asdf`.

## Terminal
```bash
pwd   ls   cd folder   cd ..   mkdir output   cls / clear   Ctrl+C (stop)   Tab (autocomplete)   ↑ (previous command)
```
