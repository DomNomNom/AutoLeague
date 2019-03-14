"""
This module contains file system paths that are used by autoleague.
"""

from pathlib import Path

class WorkingDir:

    def __init__(self, working_dir: Path):
        self.bots = working_dir / 'bots'
        # self.bot_repos = self.bots / 'git_repos'
        self.bot_pack = self.bots / 'bot_pack'
        self.match_configs_todo = working_dir / 'match_configs_todo'
        self.match_configs_done = working_dir / 'match_configs_done'
        self.history_dir = working_dir / 'match_history_dir'
        self._ensure_directory_structure()

    def _ensure_directory_structure(self):
        for directory in vars(self).values():
            if not isinstance(directory, Path):
                continue
            directory.mkdir(parents=True, exist_ok=True)
