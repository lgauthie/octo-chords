def read_csv(fname):
    """
    Reads a single csv file to a list
    """
    out = []
    with open(fname, 'r') as f:
        for line in f:
            out.append(map(lambda x: float(x.strip('\n')), line.split(',')[1:]))
    return out
