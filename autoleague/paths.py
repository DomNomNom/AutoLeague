"""
This module contains file system paths that are used by autoleague.
"""

from pathlib import Path

class WorkingDir:
    """
    An object to make is convenient and safe to access file system paths.
    """

    def __init__(self, working_dir: Path):
        self._working_dir = working_dir
        self.bots = working_dir / 'bots'
        self.bot_pack = self.bots / 'bot_pack'
        self.match_configs_todo = working_dir / 'match_configs_todo'
        self.match_configs_done = working_dir / 'match_configs_done'
        self.history_dir = working_dir / 'match_history_dir'
        self.skill_pool = working_dir / 'skill_pool.json'
        self._ensure_directory_structure()

    def _ensure_directory_structure(self):
        self._working_dir.mkdir(exist_ok=True)
        self.bots.mkdir(exist_ok=True)
        self.bot_pack.mkdir(exist_ok=True)
        self.match_configs_todo.mkdir(exist_ok=True)
        self.match_configs_done.mkdir(exist_ok=True)
        self.history_dir.mkdir(exist_ok=True)
