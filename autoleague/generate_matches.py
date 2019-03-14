from typing import Mapping
from pathlib import Path

from rlbot.parsing.bot_config_bundle import BotConfigBundle
from rlbot.parsing.directory_scanner import scan_directory_for_bot_configs

from autoleague.paths import WorkingDir
from autoleague.bot_id import BotID, make_bot_id
from autoleague.skill_pool import load_skill_pool, save_skill_pool, match_making

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

    # Pick some good matches
    bot_id_pairs = match_making(skill_pool, num_matches)
    for p in bot_id_pairs:
        print (p)
    # print (bot_id_pairs)

    # TODO: Write to working_dir

def get_bots(working_dir: WorkingDir) -> Mapping[BotID, BotConfigBundle]:
    return {
        make_bot_id(working_dir, bot_config): bot_config
        for bot_config in scan_directory_for_bot_configs(working_dir.bots)
    }
