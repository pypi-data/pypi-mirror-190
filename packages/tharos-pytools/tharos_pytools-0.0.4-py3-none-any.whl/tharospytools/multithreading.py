"Tools to handle multithreading"
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count
from typing import Callable


def futures_collector(
    func: Callable,
        argslist: list[tuple],
        kwargslist: list[dict] | None = None,
        num_processes: int = cpu_count()
) -> list:
    """
    Spawns len(arglist) instances of func and executes them at num_processes instances at time.

    * func : a function
    * argslist (list): a list of tuples, arguments of each func
    * kwargslist (list[dict]) a list of dicts, kwargs for each func
    * num_processes (int) : max number of concurrent instances.
        Default : number of available logic cores
    """
    if kwargslist is None or len(kwargslist) == len(argslist):
        with ThreadPoolExecutor(max_workers=num_processes) as executor:
            futures = [
                executor.submit(
                    func,
                    *args
                ) if kwargslist is None else
                executor.submit(
                    func,
                    *args,
                    **kwargslist[i]
                ) for i, args in enumerate(argslist)
            ]
        return [f.result() for f in futures]
    else:
        raise ValueError(
            f"""Positionnal argument list length ({len(argslist)})
            does not match keywords argument list length ({len(kwargslist)}).""")
