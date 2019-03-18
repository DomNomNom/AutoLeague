import json
from typing import List
from dataclasses import dataclass, field
from pathlib import Path

from rlbottraining.history.exercise_result import ExerciseResultJson
from rlbottraining.history.website.view import Aggregator, Renderer
from rlbottraining.paths import HistoryPaths
from rlbottraining.history.website.json_utils import serialize_with_line_per_item, get_nested

@dataclass
class MatchListRenderer(Renderer):
    """
    Returns contents for static files which can be served.
    Usually for data from an Aggregator.
    """
    matches: List[ExerciseResultJson]

    def render(self) -> str:
        return serialize_with_line_per_item(self.matches)

@dataclass
class MatchListAggregator(Aggregator):
    path: Path = field(default_factory=lambda: HistoryPaths.Website.data_dir/'matches.json')

    def add_exercise_result(self, result_json: ExerciseResultJson):
        if self.path not in self.shared_url_map:  # ensure we're rendering the path
            self.shared_url_map[self.path] = MatchListRenderer(matches=[])
        renderer = self.shared_url_map[self.path]
        if get_nested(result_json, 'exercise.__class__') == 'autoleague.match_exercise.MatchExercise':
            renderer.matches.append(result_json)
