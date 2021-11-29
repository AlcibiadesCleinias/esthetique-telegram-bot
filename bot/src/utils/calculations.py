from schemas import LikeStats


LIKE_WEIGHT = {
    'like_2': -2,
    'like_1': -1,
    'like0': 0,
    'like1': 1,
    'like2': 2,
}


def calculate_weight(like_stats: LikeStats) -> float:
    like_numbers = like_stats.dict()
    return sum([like_numbers[key] * LIKE_WEIGHT[key] for key in LIKE_WEIGHT.keys()])
