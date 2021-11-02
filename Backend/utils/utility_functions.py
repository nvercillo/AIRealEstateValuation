def split_str_into_n_sized_parts(string: str, n: int):

    arr = []
    start = 0
    end = n
    while end <= len(string):
        arr.append(string[start:end])
        start = end
        end += n

    remainder = string[start:end]
    if len(remainder) != 0:
        arr.append(string[start:end])

    return arr
