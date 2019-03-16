from dataclasses import dataclass, field
from typing import Iterable, Any, Mapping, Optional

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.training.training import Grade, Pass, Fail
from rlbot.utils.game_state_util import GameState
from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbottraining.grading.grader import Grader
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.match_configs import make_default_match_config
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.training_exercise import TrainingExercise

from autoleague.replays import ReplayPreference, ReplayMonitor


class FailDueToNoReplay(Fail):
    def __repr__(self):
        return 'FAIL: Match finished but no replay was written to disk.'

@dataclass
class MatchGrader(Grader):

    replay_monitor: ReplayMonitor = field(default_factory=ReplayMonitor)

    last_match_time: float = 0
    last_game_tick_packet: GameTickPacket = None

    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        self.replay_monitor.ensure_monitoring()
        self.last_game_tick_packet = tick.game_tick_packet
        game_info = tick.game_tick_packet.game_info
        if game_info.is_match_ended:
            if self.replay_monitor.replay_id:
                self.replay_monitor.stop_monitoring()
                return Pass()
            seconds_since_game_end = game_info.seconds_elapsed - self.last_match_time
            if seconds_since_game_end > 15:
                self.replay_monitor.stop_monitoring()
                return FailDueToNoReplay()
        else:
            self.last_match_time = game_info.seconds_elapsed


@dataclass
class MatchExercise(TrainingExercise):

    grader: Grader = field(default_factory=MatchGrader)
    match_config_file_name: str = None

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState()  # don't need to change anything

