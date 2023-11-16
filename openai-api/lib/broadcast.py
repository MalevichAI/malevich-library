def broadcast(x: dict):
    s = {}
    for key in x:
        if not isinstance(x[key], list):
            s[key] = [x[key]]

    assert all(
        len(s[key]) == len(s['index']) or len(s[key]) == 1
        for key in s
    )

    for key in s:
        if len(s[key]) == 1:
            s[key] = s[key] * len(s['index'])

    return x
