import json

from malevich._cli.dev import get_processor_docstring, list_procs, parse_docstring

data = json.loads(list_procs('lib/src/'))

errors = []
for d in data:
    print(f"Checking {d['name']} ...")
    doc = get_processor_docstring(d['name'], d['path'])
    try:
        parse_docstring(doc)
    except Exception:
        errors.append(d['name'])

if len(errors) != 0:
    print("The following processors have invalid documentation:\n\t" +
          "\n\t".join(errors) +
          "\nPlease rewrite the docs and try again"
    )
    exit(1)
