from pathlib import Path
from typing import Mapping, List, Tuple
import json
import random
import time

from rlbot.parsing.bot_config_bundle import BotConfigBundle
from rlbot.parsing.directory_scanner import scan_directory_for_bot_configs
from rlbot.matchconfig.conversions import read_match_config_from_file, ConfigJsonEncoder
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team

from autoleague.paths import WorkingDir, PackageFiles
from autoleague.bot_id import BotID, make_bot_id
from autoleague.skill_pool import load_skill_pool, save_skill_pool, match_making
from autoleague.match_naming import get_match_name


def generate_matches(working_dir: WorkingDir, num_matches: int):
    """
    Looks at the working_dir's bots and their past results
    to decide which MatchConfigs to put into match_config_todo.
    """
    active_bots = get_bots(working_dir)
    skill_pool = load_skill_pool(working_dir)

    # Align the keys of skill_pool and active_bots
    skill_pool.ratings = { k:v for k,v in skill_pool.ratings if k in active_bots }
    for bot_id in active_bots:
        if bot_id not in skill_pool.ratings:
            skill_pool.ratings[bot_id] = skill_pool.env.create_rating()

    bot_id_pairs = match_making(skill_pool, num_matches)
    match_configs = [ make_match_config(working_dir, pair) for pair in bot_id_pairs ]
    start_number = int(time.time()*6283185399)  # lol
    for i, match_config in enumerate(match_configs):
        print(f'Generated match: {get_match_name(match_config)}')
        match_config_path = working_dir.match_configs_todo / f'{start_number}_{i}.json'
        assert not match_config_path.exists()
        with open(match_config_path, 'w') as f:
            json.dump(match_config, f, cls=ConfigJsonEncoder)
    num_todos = len(list(working_dir.match_configs_todo.iterdir()))
    more_info = '' if num_todos == len(bot_id_pairs) else f'(A total of {num_todos} matches waiting to be played)'
    print(f'Added {len(bot_id_pairs)} match configs. {more_info}')


def make_match_config(working_dir: WorkingDir, bot_id_pair: Tuple[BotID, BotID]) -> MatchConfig:
    match_config = read_match_config_from_file(PackageFiles.default_match_config)
    match_config.game_map = random.choice([
        'ChampionsField',
        'Farmstead',
        'StarbaseArc',
        'DFHStadium',
        'SaltyShores',
        'Wasteland',
    ])
    if random.random() < .5:
        bot_id_pair = bot_id_pair[::-1]  # mix up the colors a bit.
    match_config.player_configs = [
        PlayerConfig.bot_config(working_dir.bots / bot_id_pair[0], Team.BLUE),
        PlayerConfig.bot_config(working_dir.bots / bot_id_pair[1], Team.ORANGE),
    ]
    return match_config

def get_bots(working_dir: WorkingDir) -> Mapping[BotID, BotConfigBundle]:
    return {
        make_bot_id(working_dir, bot_config): bot_config
        for bot_config in scan_directory_for_bot_configs(working_dir.bots)
    }
