from typing import Mapping, List, Tuple
import json
from dataclasses import dataclass, field
import random

import numpy as np
from trueskill import Rating, TrueSkill

from autoleague.paths import WorkingDir
from autoleague.bot_id import BotID

@dataclass
class SkillPool:
    ratings: Mapping[BotID, Rating] = field(default_factory=dict)
    env: TrueSkill = field(default_factory=TrueSkill)


def load_skill_pool(working_dir: WorkingDir) -> SkillPool:
    if not working_dir.skill_pool.exists():
        return SkillPool()
    with open(working_dir.skill_pool) as f:
        return json.load(f, object_hook=as_skill_pool)

def save_skill_pool(working_dir: WorkingDir, skill_pool: SkillPool):
    with open(working_dir.skill_pool, 'w') as f:
        json.dump(f, skill_pool, cls=SkillEncoder, sort_keys=True)


def match_making(skill_pool: SkillPool, num_matches: int) -> List[Tuple[BotID, BotID]]:
    # A naive way of doing matchmaing:
    # weighted random choice, weighted by 1v1 match quality.
    ratings = skill_pool.ratings
    ids = sorted(list(ratings.keys()))
    assert len(ids) > 1
    population = []
    weights = []
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            rating_i = ratings[ids[i]]
            rating_j = ratings[ids[j]]
            population.append((ids[i], ids[j]))
            weights.append(skill_pool.env.quality([(rating_i,), (rating_j,)]))

    weights = np.array(weights)
    weights /= weights.sum()
    indecies = np.random.choice(np.arange(len(population)), p=weights, size=num_matches, replace=False)
    return [ population[i] for i in sorted(indecies) ]


# ====== SkillPool -> JSON ======

known_types = {
    TrueSkill: '__TrueSkill__',
    Rating: '__Rating__',
    SkillPool: '__SkillPool__',
}
class SkillEncoder(json.JSONEncoder):
    def default(self, obj):
        for cls, tag in known_types.items():
            if not isinstance(obj, cls):
                continue
            json_obj = obj.__dict__.copy()
            if isinstance(obj, TrueSkill):
                del json_obj['cdf']
                del json_obj['pdf']
                del json_obj['ppf']
            json_obj[tag] = True
            return json_obj
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# ====== JSON -> SkillPool ======

def as_skill_pool(json_obj) -> SkillPool:
    for cls, tag in known_types.items():
        if not json_obj.get(tag, False):
            continue
        obj = cls()
        del json_obj[tag]
        obj.__dict__ = json_obj
        return obj
    return json_obj

if __name__ == '__main__':
    # Quick and dirty unit test
    pool = SkillPool()
    pool.ratings['foo'] = pool.env.create_rating()
    s = json.dumps(pool, cls=SkillEncoder, sort_keys=True)
    pool2 = json.loads(s, object_hook=as_skill_pool)
    assert str(pool) == str(pool2)
