"""
This module contains file system paths that are used by autoleague.
"""

from pathlib import Path

from rlbottraining.paths import HistoryPaths

class WorkingDir:
    """
    An object to make is convenient and safe to access file system paths.
    """

    def __init__(self, working_dir: Path):
        working_dir = working_dir.absolute()
        self._working_dir = working_dir
        self.bots = working_dir / 'bots'
        self.bot_pack = self.bots / 'bot_pack'
        self.match_configs_todo = working_dir / 'match_configs_todo'
        self.match_configs_done = working_dir / 'match_configs_done'
        self.history_dir = working_dir / 'history_dir'
        self.skill_pool = working_dir / 'skill_pool.json'
        self._ensure_directory_structure()

    def _ensure_directory_structure(self):
        self._working_dir.mkdir(exist_ok=True)
        self.bots.mkdir(exist_ok=True)
        self.bot_pack.mkdir(exist_ok=True)
        self.match_configs_todo.mkdir(exist_ok=True)
        self.match_configs_done.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)


class PackageFiles:
    """
    An object to keep track of static paths that are part of this package
    """
    _package_dir = Path(__file__).absolute().parent
    default_match_config = _package_dir / 'default_match_config.cfg'

    _website_dir = _package_dir / 'website'
    additional_website_code = _website_dir / 'additional_website_code'
    additional_website_static = _website_dir / 'static'
