from pathlib import Path

from rlbot.parsing.bot_config_bundle import BotConfigBundle

from autoleague.paths import WorkingDir


BotID = str  # type alias

def make_bot_id(working_dir: WorkingDir, bot_config: BotConfigBundle) -> BotID:
    path = Path(bot_config.config_directory) / bot_config.config_file_name
    return str(path.relative_to(working_dir.bots))
