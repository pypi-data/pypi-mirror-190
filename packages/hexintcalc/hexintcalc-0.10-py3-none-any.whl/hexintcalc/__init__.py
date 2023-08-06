from operatorlookup import doops
from typing import Union


def number_to_int(n):
    return (
        int((n.lower().replace("`", "").split("x")[-1]), base=16)
        if isinstance(n, str)
        else int(n)
    )


def number_to_hex(n):
    if isinstance(n, str):
        return n
    return hex(int(n))


def hexcalc(
    op: str,
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    nr1, nr2 = number_to_int(n1), number_to_int(n2)
    resa = doops(op, nr1, nr2, *args, **kwargs)
    hestr = hex(resa).lstrip("0x")
    if hestr == "":
        hestr = "0"
    if backtick:
        hestr = hestr.zfill(16)
        hestr = hestr[:8] + "`" + hestr[8:]
    hestr = hestr.zfill(zfill)
    if add0x:
        hestr = "0x" + hestr
    return hestr


def hadd(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "+", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hdivide(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "//", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hbitwiseand(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "&", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hxor(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "^", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hor_(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "|", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hpow(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "**", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hlshift(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "<<", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hmod(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "%", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hmul(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "*", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hrshift(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        ">>", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hsub(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "-", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hlt(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "<", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hle(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "<=", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def heq(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "==", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hne(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        "!=", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hge(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        ">=", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )


def hgt(
    n1: Union[str, int, float],
    n2: Union[str, int, float],
    zfill: int = 0,
    backtick: bool = False,
    add0x: bool = True,
    *args,
    **kwargs
) -> str:
    return hexcalc(
        ">", n1, n2, zfill=zfill, backtick=backtick, add0x=add0x, *args, **kwargs
    )



