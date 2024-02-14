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
                    ["malevich", "dev", "list", d]
                ).decode()
            )
        )
if len(procs) == 0:
    print("No modified procs to check. Exiting...")
    exit(0)

errors = []

for proc in procs:
    doc = check_output(
        ["malevich", "dev" ,"get-doc", proc['name'], proc["path"]]
    ).decode().strip()
    try:
        check_call(
            ["malevich", "dev" ,"parse-doc", f"\"{doc}\""],
            stdout=DEVNULL,
        )
    except CalledProcessError:
        errors.append(proc['name'])

if len(errors) != 0:
    print("Following apps' docs should be rewritten:")
    print("\n\t".join(errors))
    print("Please, rewrite docs and try again")
    exit(1)