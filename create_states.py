from itertools import product


def create_states(str1, rno):
    chars = list(str1)
    results = []
    for c in product(chars, repeat=rno):
        results.append(c)
    return results


def join_tuple_string(strings_tuple) -> str:
    return ''.join(strings_tuple)


def reformat(str1, rno):
    all_comb = create_states(str1, rno)
    results = map(join_tuple_string, all_comb)
    return list(results)
