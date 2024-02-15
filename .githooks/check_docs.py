import json
import os
from subprocess import (
    DEVNULL,
    PIPE,
    CalledProcessError,
    Popen,
    check_call,
    check_output,
)

print("===== Malevich Git Pre-commit Hook =======")

ps = Popen(("git", "status", "-uno", "-s"), stdout=PIPE)

ps.wait()

files = check_output(
    ["cut", "-d", " ", "-f3"],
    stdin=ps.stdout
    ).decode().strip("\n ").split('\n')

procs = []

for file in files:
    if file.endswith(".py"):
        d = os.path.dirname(os.path.join("./", file))
        procs.extend(
            json.loads(
                check_output(
                    ["malevich", "dev", "list-procs", d]
                ).decode()
            )
        )
if len(procs) == 0:
    print("No modified procs to check. Exiting...")
    print("==========================================\n")
    exit(0)

errors = []

for proc in procs:
    doc = check_output(
        ["malevich", "dev" ,"get-doc", proc['name'], proc["path"]]
    ).decode().strip()
    try:
        check_call(
            ["malevich", "dev" ,"parse-doc", f"\"{doc}\""],
            stderr=DEVNULL,
        )
    except CalledProcessError:
        errors.append(proc['name'])

if len(errors) != 0:
    print("Following apps' docs should be rewritten:\n\t", end="")
    print("\n\t".join(errors))
    print("\nPlease, rewrite docs and try again")
    print("==========================================\n")
    exit(1)

print("Everything is passed. Commiting...")
print("==========================================\n")
