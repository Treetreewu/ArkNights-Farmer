import itertools
import random
from collections import Counter, defaultdict
from farmer.data import TAGS, RARITY


over_5 = False


def random_tags():
    result = random.sample(list(TAGS.keys()), k=5)
    print(result)
    return dict.fromkeys(result)


def count_stars(_tags):
    """Counting starts (o゜▽゜)o☆
    :return : List of tags to select.
              None if skip this recruit.
    """
    stars = {}
    employs = {}
    # 计算选1, 2, 3个标签的情况
    for count in range(1, 4):
        for comb in itertools.combinations(_tags.keys(), count):
            # 交集
            emp = TAGS[comb[0]].intersection(*(TAGS[t] for t in comb[1:]))
            emp = frozenset(e for e in emp if RARITY[e] > 2)
            if not emp:
                continue
            # 排除小于等于二星（指某些有高星标签的支援机械），计算保底
            employs[comb] = emp
            stars[comb] = min(RARITY[e] for e in employs[comb])
    # 保底最高星的组合
    result = max(stars, key=stars.get)
    if stars[result] <= 3:
        # 如果最高保底3星，就不选标签了，没必要。
        return []
    combs = [k for k in stars if stars[k] == stars[result]]
    if len(combs) == 1:
        return combs[0]
    if stars[result] == 4:
        # 4星组合有多种，取并集后按照标签出现次数最多的规则缩减为3个标签。
        counter = Counter(itertools.chain(*combs))
        return [t[0] for t in counter.most_common(3)]
    else:
        # 大于等于5星，首先排除干员池相同的标签组
        reverted_employs = defaultdict(list)
        for k, v in employs.items():
            if k in combs:
                reverted_employs[v].append(k)

        if len(reverted_employs) == 1:
            return max(reverted_employs.popitem()[1], key=len)
        elif over_5:
            # 大杂烩随便选选。
            vs = itertools.chain(*itertools.chain(*reverted_employs.values()))
            counter = Counter(vs)
            return tuple(t[0] for t in counter.most_common(3))
        else:
            return None


if __name__ == '__main__':
    print(count_stars(random_tags()))
