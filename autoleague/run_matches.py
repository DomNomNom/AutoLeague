from pathlib import Path
import json
import shutil

from rlbot.utils.logging_utils import get_logger
from rlbot.matchconfig.conversions import as_match_config
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team
from rlbottraining.training_exercise import Playlist
from rlbottraining.exercise_runner import run_playlist
from rlbottraining.history.exercise_result import log_result, store_result
from rlbottraining.history.website.server import set_additional_website_code

from autoleague.match_exercise import MatchExercise, MatchGrader
from autoleague.match_naming import get_match_name
from autoleague.paths import WorkingDir, PackageFiles
from autoleague.replays import ReplayPreference, ReplayMonitor

logger = get_logger('autoleague')

def run_matches(working_dir: WorkingDir, replay_preference: ReplayPreference):
    """
    Runs all matches as specified by working_dir/match_configs_todo
    """
    match_paths = list(working_dir.match_configs_todo.iterdir())
    if not len(match_paths):
        logger.warning(f'No matches found. Add some using `autoleague generate_matches`')
        return
    logger.info(f'Going to run {len(match_paths)} matches')
    match_configs = [ parse_match_config(p) for p in match_paths ]
    playlist = [
        MatchExercise(
            name=get_match_name(match_config),
            match_config_file_name=match_path.name,
            match_config=match_config,
            grader=MatchGrader(
                replay_monitor=ReplayMonitor(replay_preference=replay_preference),
            )
        )
        for match_config, match_path in zip(match_configs, match_paths)
    ]

    set_additional_website_code(PackageFiles.additional_website_code, working_dir.history_dir)

    for result in run_playlist(playlist):
        store_result(result, working_dir.history_dir)
        match_config_file_name = result.exercise.match_config_file_name
        shutil.move(
            working_dir.match_configs_todo / match_config_file_name,
            working_dir.match_configs_done / match_config_file_name,
        )
        log_result(result, logger)

def parse_match_config(filepath: Path) -> MatchConfig:
    with open(filepath) as f:
        try:
            return json.load(f, object_hook=as_match_config)
        except Exception as e:
            print("Error while parsing:", filepath)
            raise e

