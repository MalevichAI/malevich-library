import json
import os
from subprocess import (
    PIPE,
    Popen,
    check_output,
)

from malevich._cli.dev import (
    get_processor_docstring,
    list_procs,
    parse_docstring,
)

print("===== Malevich Git Pre-commit Hook =======")

ps = Popen(("git", "status", "-uno", "-s"), stdout=PIPE)

ps.wait()

files = check_output(
    ["cut", "-d", " ", "-f3"],
    stdin=ps.stdout
    ).decode().strip("\n ").split('\n')

procs = []
results = []

for file in files:
    if file.endswith(".py"):
        d = os.path.dirname(os.path.join("./", file))
        results.append(
                list_procs(path=d, out=None)
        )
if len(results) == 0:
    print("No modified procs to check. Exiting...")
    print("==========================================\n")
    exit(0)

results = list(set(results))

for result in results:
    procs.extend(
        json.loads(
            result
        )
    )

errors = []

for proc in procs:
    print(f"Checking {proc['name']}...")
    doc = get_processor_docstring(proc['name'], proc['path'])
    try:
        parse_docstring(doc)
    except Exception:
        errors.append(proc['name'])

if len(errors) != 0:
    print("Following apps' docs should be rewritten:\n\t", end="")
    print("\n\t".join(errors))
    print("\nPlease, rewrite docs and try again")
    print("==========================================\n")
    exit(1)

print("Everything is passed. Commiting...")
print("==========================================\n")
