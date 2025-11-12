
#!/usr/bin/env python3
import sys, os, textwrap

if len(sys.argv) < 3:
    print("Usage: scripts/new_problem.py <id> <kebab-title>")
    sys.exit(1)

pid = sys.argv[1]
title = sys.argv[2]
folder = f"problems/{pid}-{title}"
os.makedirs(folder, exist_ok=True)

with open(os.path.join(folder, "solution.py"), "w") as f:
    f.write(textwrap.dedent(f'''\
        # {pid} - {title.replace("-", " ").title()}
        from typing import List

        class Solution:
            pass
        '''))

with open(os.path.join(folder, "NOTES.md"), "w") as f:
    f.write(textwrap.dedent(f'''\
        # {pid}. {title.replace("-", " ").title()}
        (copy template from templates/PROBLEM_NOTE_TEMPLATE.md)
        '''))
print(f"Scaffolded {folder}")
