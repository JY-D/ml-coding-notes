import pdb
from collections import Counter, defaultdict

# Count frequencies
cnt = Counter(["car", "bus", "car", "van"])
cnt["car"]  # 2
cnt.most_common(2)  # [("car", 2), ("bus", 1)]

# Grouping with defaultdict
by_tag: dict[str, list[int]] = defaultdict(list)  # tag -> list of scores
by_tag["night"].append(1)
by_tag["night"].append(0)

# Nested defaultdict for stats (e.g., TP/FP/FN)
stats = defaultdict(lambda: {"tp": 0, "fp": 0, "fn": 0})  # dont need to assign key
stats["rain"]["tp"] += 1
# stats["rain"]
# {'tp': 1, 'fp': 0, 'fn': 0}

# usage caution:
# stats.get("rain") will return None
# "rain" in stats will err, wont create new key
# for k in stats: wont create new key
pdb.set_trace()
