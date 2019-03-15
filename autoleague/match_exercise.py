from dataclasses import dataclass, field
from typing import Iterable, Any, Mapping, Optional

from rlbot.matchconfig.match_config import MatchConfig
from rlbot.utils.game_state_util import GameState
from rlbot.utils.rendering.rendering_manager import RenderingManager
from rlbot.training.training import Grade, Pass
from rlbottraining.grading.grader import Grader
from rlbottraining.match_configs import make_default_match_config
from rlbottraining.rng import SeededRandomNumberGenerator
from rlbottraining.history.metric import Metric
from rlbottraining.grading.training_tick_packet import TrainingTickPacket
from rlbottraining.training_exercise import TrainingExercise

from autoleague.replays import ReplayPreference


@dataclass
class MatchGrader(Grader):

    replay_preference: ReplayPreference

    last_match_time: float = 0
    replay_id: Optional[str] = None


    def on_tick(self, tick: TrainingTickPacket) -> Optional[Grade]:
        game_info = tick.game_tick_packet.game_info
        if game_info.is_match_ended:
            seconds_since_game_end = game_info.seconds_elapsed - self.last_match_time
            print('enduuuu', seconds_since_game_end)
            if seconds_since_game_end > 30:
                handle_replay_saving_while_on_endscreen(self.replay_preference)
                self.final_game_tick_packet = tick.game_tick_packet
                return Pass()
        else:
            self.last_match_time = game_info.seconds_elapsed
        pass  # Continue by default

from autoleague.replays import handle_replay_saving_while_on_endscreen
@dataclass
class MatchExercise(TrainingExercise):

    grader: Grader = field(default_factory=MatchGrader)

    def make_game_state(self, rng: SeededRandomNumberGenerator) -> GameState:
        return GameState()  # don't need to change anything

