def bit_to_int(sequence, group_len):
    grouped = list(zip(*[iter(sequence)] * group_len))
    return [sum(v<<i for i, v in enumerate(p[::-1])) for p in grouped]