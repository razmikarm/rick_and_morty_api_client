from typing import Callable

def ep_aired_between(start_year: int, end_year: int) -> Callable:
    def inner(ep) -> bool:
        air_year = int(ep["air_date"].split(',')[1].strip())
        return start_year <= air_year <= end_year
    return inner
