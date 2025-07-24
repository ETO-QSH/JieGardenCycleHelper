def silk_cocoon_return(originium: int) -> int:
    """ 茧成绢返还规则 """
    return min(originium // 4, 99)


def recurse(x: int, t: int, p: float, f) -> int:
    if t > 0:
        x = x * (1 - p) + p * (x + f(x))
        return recurse(x, t - 1, p, f)
    else:
        return x


print(recurse(150, 6, 5 / 12, silk_cocoon_return))
