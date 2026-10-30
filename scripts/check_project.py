"""
Project health check. Run from anywhere inside the project:

    python scripts/check_project.py

It prints OK / WARN / FAIL for each check. It never changes any file.
FAIL = something is wrong and should be fixed before pushing.
WARN = worth a look, but not necessarily a problem.

When a phase is finished, update the EXPECTED numbers below.
"""
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import json
import re
import subprocess
import sys

# ---------------- EXPECTED VALUES (update after each phase) ----------------
EXPECTED_ROWS = 66475
EXPECTED_TAG_CANDIDATES = 13933
EXPECTED_APPS = {"PhonePe", "Google Pay", "Paytm", "CRED", "BHIM"}
EXPECTED_LOG_ENTRIES = 21
REQUIRED_FILES = [
    "README.md", "requirements.txt", "environment.yml", ".gitignore",
    "notebooks/01_collect.ipynb", "notebooks/02_clean_and_mask.ipynb",
    "docs/decision-log.md", "docs/data-quality-log.md",
    "data/raw/collection_note.md", "data/processed/reviews_clean.csv",
]
# ---------------------------------------------------------------------------

results = []

def record(status, message):
    results.append(status)
    # A failing check that only states what SHOULD be true gets a clear prefix, so it cannot be misread as a pass
    if status != "OK" and ":" not in message and "(" not in message and "skipped" not in message and "Could not" not in message:
        message = "NOT TRUE - " + message
    print(f"{status:<5} {message}")

def find_root():
    here = Path.cwd().resolve()
    for folder in [here, *here.parents]:
        if (folder / "requirements.txt").exists():
            return folder
    print("FAIL  Could not find requirements.txt. Run this from inside the project folder.")
    sys.exit(1)

def git(*args):
    try:
        out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
        return out.returncode, out.stdout.strip()
    except FileNotFoundError:
        return None, ""

ROOT = find_root()
print(f"Checking project: {ROOT.name}\n")

# ---- 1. Environment ----
print("[1] Environment")
py = sys.version_info
record("OK" if (py.major, py.minor) == (3, 11) else "WARN", f"Python {py.major}.{py.minor}.{py.micro} (project uses 3.11)")
mismatches, missing = [], []
for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^\s*([A-Za-z0-9_.\-]+)\s*==\s*([^\s#]+)", line)
    if not m:
        continue
    pkg, wanted = m.groups()
    try:
        have = version(pkg)
        if have != wanted:
            mismatches.append(f"{pkg} {have} (wanted {wanted})")
    except PackageNotFoundError:
        missing.append(pkg)
record("FAIL" if missing else "OK", "All libraries in requirements.txt are installed" if not missing else f"Not installed: {', '.join(missing)}")
record("WARN" if mismatches else "OK", "Library versions match requirements.txt" if not mismatches else "Version differences: " + "; ".join(mismatches))

# ---- 2. Required files ----
print("\n[2] Files")
absent = [f for f in REQUIRED_FILES if not (ROOT / f).exists()]
record("FAIL" if absent else "OK", "All expected files are present" if not absent else f"Missing: {', '.join(absent)}")

# ---- 3. Privacy and safety ----
print("\n[3] Privacy and safety")
gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
record("OK" if "data/raw/reviews_raw.csv" in gitignore else "FAIL", ".gitignore blocks the raw reviews file")
code, tracked = git("ls-files")
if code is None or code != 0:
    record("WARN", "Git not available here, so tracked-file checks were skipped")
    tracked_files = []
else:
    tracked_files = tracked.splitlines()
    bad = [f for f in tracked_files if "reviews_raw" in f or f.endswith(".env") or "/.env" in f]
    record("FAIL" if bad else "OK", "Raw data and secret files are not tracked by Git" if not bad else f"Tracked but should not be: {bad}")
private = [p.name for p in ROOT.rglob("*") if ".git" not in p.parts and p.is_file() and "interview" in p.name.lower()]
record("FAIL" if private else "OK", "No private interview notes inside the project folder" if not private else f"Private file inside project: {private}")
dupes = [p.name for p in ROOT.rglob("*") if ".git" not in p.parts and p.is_file()
         and re.search(r"(__old_|\(\d+\)|_\d+|_copy| copy)\.(md|ipynb|csv|txt|yml)$", p.name)]
record("WARN" if dupes else "OK", "No duplicate-looking files (like README_1.md)" if not dupes else f"Check these names: {dupes}")
leaks = []
for nb in (ROOT / "notebooks").glob("*.ipynb"):
    text = nb.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"C:\\\\Users|/home/|/mnt/", text):
        leaks.append(nb.name)
record("WARN" if leaks else "OK", "Notebooks contain no personal file paths" if not leaks else f"Personal paths found in: {leaks}")

# ---- 4. Data ----
print("\n[4] Processed data")
try:
    import pandas as pd
    df = pd.read_csv(ROOT / "data" / "processed" / "reviews_clean.csv")
    record("OK" if len(df) == EXPECTED_ROWS else "FAIL", f"Row count is {len(df):,} (expected {EXPECTED_ROWS:,})")
    record("OK" if set(df["app"].unique()) == EXPECTED_APPS else "FAIL", "All five apps are present")
    record("OK" if df["review_id"].is_unique else "FAIL", "review_id is unique")
    record("OK" if "text" not in df.columns else "FAIL", "No raw 'text' column in the processed file")
    cand = int(df["tag_candidate"].sum())
    record("OK" if cand == EXPECTED_TAG_CANDIDATES else "FAIL", f"Tagging candidates: {cand:,} (expected {EXPECTED_TAG_CANDIDATES:,})")
    stored_ok = df.loc[~df["tag_candidate"], "text_masked"].isin(["[not stored]", "[REDACTED]"]).all()
    record("OK" if stored_ok else "FAIL", "Review text is stored only for tagging candidates")
    record("OK" if not ((df["text_masked"] == "[REDACTED]") & df["tag_candidate"]).any() else "FAIL", "No redacted review is marked for tagging")
    record("OK" if df["rating"].between(1, 5).all() else "FAIL", "All ratings are between 1 and 5")
except Exception as e:
    record("FAIL", f"Could not check the processed file: {type(e).__name__}: {e}")

# ---- 5. Documents agree with each other ----
print("\n[5] Documents")
def read(rel):
    p = ROOT / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""
readme, dq, dec, note = read("README.md"), read("docs/data-quality-log.md"), read("docs/decision-log.md"), read("data/raw/collection_note.md")
entries = len(re.findall(r"^\| \d+ \|", dq, flags=re.M))
record("OK" if entries == EXPECTED_LOG_ENTRIES else "FAIL", f"Data-quality log has {entries} entries (expected {EXPECTED_LOG_ENTRIES})")
record("OK" if f"{EXPECTED_ROWS:,}" in readme and f"{EXPECTED_ROWS:,}" in note and f"{EXPECTED_ROWS:,}" in dq else "FAIL",
       f"README, collection note and data-quality log all mention {EXPECTED_ROWS:,} reviews")
record("OK" if "12 months" not in note else "FAIL", "Collection note has no stale '12 months' wording")
record("OK" if "[confirm]" not in dec and "_fill in" not in dec else "WARN", "Decision log has no unresolved [confirm] or 'fill in' marks")
bad_nb = []
for nb in (ROOT / "notebooks").glob("*.ipynb"):
    try:
        json.loads(nb.read_text(encoding="utf-8"))
    except Exception:
        bad_nb.append(nb.name)
record("OK" if not bad_nb else "FAIL", "Notebooks are valid files" if not bad_nb else f"Broken notebook files: {bad_nb}")

# ---- 6. Git state ----
print("\n[6] Git")
if code is None or code != 0:
    record("WARN", "Git not available, skipped")
else:
    c, status = git("status", "--porcelain")
    if status:
        lines = status.splitlines()
        record("WARN", f"{len(lines)} uncommitted or untracked change(s): " + "; ".join(l.strip() for l in lines[:6]))
    else:
        record("OK", "Everything is committed")
    c, ahead = git("rev-list", "--count", "origin/main..HEAD")
    if c == 0 and ahead.isdigit():
        record("OK" if ahead == "0" else "WARN", "Everything committed is also pushed to GitHub" if ahead == "0" else f"{ahead} commit(s) not pushed yet")
    else:
        record("WARN", "Could not compare with GitHub (no origin/main found)")

# ---- Summary ----
print()
fails, warns = results.count("FAIL"), results.count("WARN")
print(f"Summary: {results.count('OK')} OK, {warns} WARN, {fails} FAIL")
if fails:
    print("Something needs fixing. Copy this whole output and send it to Claude.")
elif warns:
    print("No failures. Read the WARN lines. Many are expected (for example, a file you have not committed yet).")
else:
    print("All clear.")
sys.exit(1 if fails else 0)
