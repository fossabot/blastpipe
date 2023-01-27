import asyncio
from typing import Set

from .tailcall import async_tail_call

async def _chr_union(*args) -> Set[str]:
    """Makes a sequence of int ranges or ints into a set of str
    Returns a set of chr() from:
        1. range(start=args[0], stop=args[1])
            OR
        2. chr(arg[n] if type(arg[n])==int) | chr_union(arg[:2])
    Raises:
        ValueError if not a sequence of start,stop pairs and ints, an int, or a start, stop pair
        """
    chars = set()
    if len(args) == 2 and all(map(isinstance, args, (int,)*len(args))):
        start, stop = args
        chars |= {chr(i) for i in range(start, stop)}
    else:
        for i in args:
            if isinstance(i, int):
                chars |= {chr(i)}
            elif len(i) == 2 and all(map(isinstance, i, (int,)*len(i))):
                return i # type: TAILCALL
            else:
                raise ValueError(f"Expected Sequence or int, got {type(i)}")
    return chars

def chr_union(*args):
    return asyncio.run(async_tail_call()(_chr_union)(*args))