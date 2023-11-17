def broadcast(x: dict):
    s = {}
    ln = 0
    for key in x:
        if not isinstance(x[key], list):
            s[key] = [x[key]]
        else:
            s[key] = x[key]
        ln = len(s[key])

    assert all(
        len(s[key]) == ln or len(s[key]) == 1
        for key in s
    )

    for key in s:
        if len(s[key]) == 1:
            s[key] = s[key] * ln

    return s
