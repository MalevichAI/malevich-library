import argparse
import json
from subprocess import DEVNULL, CalledProcessError, check_call, check_output

parser = argparse.ArgumentParser()
parser.add_argument('--procs')

args = parser.parse_args()

data = json.loads(args.procs)

errors = []
for d in data:
    doc = check_output(
        ["malevich", "dev", "get-doc", d['name'], d['path']]
    ).decode().strip()

    try:
        check_call(
            ["malevich", "dev", "parse-doc", doc],
            stderr=DEVNULL
        )
    except CalledProcessError:
        errors.append(d['name'])

if len(errors) != 0:
    print("The following processors have invalid documentation:\n\t" +
          "\n\t".join(errors) +
          "\nPlease rewrite the docs and try again"
    )
    exit(1)
