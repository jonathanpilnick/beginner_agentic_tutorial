"""
check_project.py - checks the parts of the project that a program can check. Run it before peer review.

  python project/check_project.py      (from the week12_web folder)

It checks: your PROJECT_README.md, that your secrets stay out of the code and out of git,
and that the tests pass (with at least 2 tests of your own). It makes no Claude calls.
It can't check if your idea is good or your app is pleasant to use: that's what peer review is for.
"""

import io
import os
import re
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(KIT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SECTIONS = ["What it does", "Course idea", "How to run", "Tests", "One failure"]
TEXT_FILES = (".py", ".html", ".js", ".css", ".md", ".txt", ".toml", ".json")
results = []


def check(ok, text, fix=""):
    results.append(ok)
    print("[ OK ]" if ok else "[TODO]", text + ("" if ok or not fix else f"\n       -> {fix}"))


# 1. The write-up
readme = HERE / "PROJECT_README.md"
if not readme.exists():
    check(False, "PROJECT_README.md", "Create project/PROJECT_README.md from the template in PROJECT_BRIEF.md")
else:
    text = readme.read_text(encoding="utf-8").lower()
    missing = [s for s in SECTIONS if s.lower() not in text]
    check(not missing, "PROJECT_README.md has every section", f"Add: {', '.join(missing)}")

# 2. Configuration: an example file to share, the real file ignored by git
check((KIT / ".env.example").exists(), ".env.example exists (shareable, no real secrets)",
      "Keep .env.example in week12_web and list every setting your app reads")
ignored = (KIT / ".gitignore").read_text(encoding="utf-8").splitlines() if (KIT / ".gitignore").exists() else []
check(".env" in [line.strip() for line in ignored], ".env is in .gitignore", "Add a line: .env")

# 3. Secret scan: no real secret written into any file you would share
token = ""
if (KIT / ".env").exists():
    for line in (KIT / ".env").read_text(encoding="utf-8").splitlines():
        if line.startswith("ADMIN_TOKEN="):
            token = line.split("=", 1)[1].strip()
patterns = [re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}"),                           # an Anthropic API key
            re.compile(r"""(TOKEN|SECRET|PASSWORD|API_KEY)\s*=\s*["'][^"']{12,}["']""", re.I)]  # a hard-coded secret
leaks = []
for path in sorted(HERE.rglob("*")) + [KIT / ".env.example"]:
    if not path.exists() or (path.name != ".env.example" and path.suffix not in TEXT_FILES) \
            or "__pycache__" in path.parts or path.name == "check_project.py":
        continue
    content = path.read_text(encoding="utf-8", errors="replace")
    if path.name == "test_project.py":       # its made-up test token is allowed
        content = content.replace("test-token-1234567890", "")
    if (len(token) >= 16 and token in content) or any(p.search(content) for p in patterns):
        leaks.append(path.name)
check(not leaks, "No secrets written in your files",
      f"Found a secret in {', '.join(leaks)}: move it to .env and read it with os.environ")

# 4. Tests: everything passes, and at least 2 tests of your own ran
os.chdir(HERE)
suite = unittest.defaultTestLoader.loadTestsFromName("test_project")
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
problems = result.failures + result.errors
check(not problems, f"Tests pass ({result.testsRun - len(result.skipped)} ran, {len(problems)} failed)",
      "Run  python project/test_project.py  and read the first failure: " +
      (problems[0][0].id().split(".")[-1] if problems else ""))
skipped = {test.id() for test, _ in result.skipped}
mine = [t for t in unittest.defaultTestLoader.loadTestsFromName("test_project.MyTests")
        if t.id() not in skipped]
check(len(mine) >= 2, f"At least 2 tests of your own ({len(mine)} so far)",
      "Write them in the MyTests class of test_project.py")

print(f"\n{sum(results)}/{len(results)} checks pass." +
      (" Ready for peer review!" if all(results) else " Fix the [TODO] lines, then run this again."))
