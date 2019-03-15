from pathlib import Path
from collections import defaultdict
import json

from rlbot.utils.logging_utils import get_logger
from rlbot.matchconfig.conversions import as_match_config
from rlbot.matchconfig.match_config import MatchConfig, PlayerConfig, Team
from rlbottraining.training_exercise import Playlist
from rlbottraining.exercise_runner import run_playlist
from rlbottraining.history.exercise_result import log_result, store_result

from autoleague.paths import WorkingDir
from autoleague.replays import ReplayPreference
from autoleague.match_exercise import MatchExercise, MatchGrader

def run_matches(working_dir: WorkingDir, replay_preference: ReplayPreference):
    """
    Runs all matches as specified by working_dir/match_configs_todo
    """
    match_configs = [ parse_match_config(p) for p in working_dir.match_configs_todo.iterdir() ]
    playlist = [ make_exercise(match_config, replay_preference) for match_config in match_configs]
    logger = get_logger('autoleague')

    for result in run_playlist(playlist):
        store_result(result, working_dir.history_dir)
        log_result(result, logger)
        # TODO: Move match_config from TODO into DONE

def parse_match_config(filepath: Path) -> MatchConfig:
    with open(filepath) as f:
        try:
            return json.load(f, object_hook=as_match_config)
        except Exception as e:
            print("Error while parsing:", filepath)
            raise e


def make_exercise(match_config: MatchConfig, replay_preference: ReplayPreference) -> MatchExercise:
    team_to_names = defaultdict(list)
    for player in match_config.player_configs:
        team_to_names[player.team].append(player.name)
    return MatchExercise(
        name=f'{", ".join(team_to_names[0])} vs {", ".join(team_to_names[1])}',
        match_config=match_config,
        grader=MatchGrader(
            replay_preference=replay_preference,
        )
    )
