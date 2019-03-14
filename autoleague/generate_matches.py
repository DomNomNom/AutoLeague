from rlbot.parsing.directory_scanner import scan_directory_for_bot_configs

from autoleague.paths import WorkingDir

def generate_matches(working_dir: WorkingDir, num_matches: int):
    """
    Looks at the working_dir's bots and their past results
    to decide which MatchConfigs to put into match_config_todo.
    """

    pass
