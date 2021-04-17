def assertEqual(a, b):
    assert type(a) == type(b)
    if(isinstance(a, list)):
        for (x, y) in zip(a, b):
            assertEqual(x, y)
    if(isinstance(a, dict)):
        for k, v in a.items():
            assert k in b
            assertEqual(v, b[k])
        for k, v in b.items():
            assert k in a
            assertEqual(v, a[k])
    assert a == b, "\nexpected:\n{}\ngot:\n{}".format(a, b)
