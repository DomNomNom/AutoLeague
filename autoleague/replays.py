from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any
import requests
import time

from pywinauto import Desktop, Application, keyboard
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from rlbottraining.history.metric import Metric


class ReplayPreference(Enum):
    SAVE = 'save'  # save to the default replays directory
    CALCULATED_GG = 'calculated_gg'  # save locally and upload to http://calculated.gg/


def upload_to_calculated_gg(replay_path: Path):
    with open(replay_path, 'rb') as f:
        response = requests.post('http://calculated.gg/api/upload', files={replay_path.name: f})

def parse_replay_id(replay_path: Path) -> str:
    replay_id, extension = replay_path.name.split('.')
    assert extension == 'replay'
    return replay_id

@dataclass
class ReplayMonitor(Metric):

    replay_preference: ReplayPreference

    replay_id: str = None
    observer: Observer = None

    def to_json(self) -> Dict[str, Any]:
        return {
            'replay_id': self.replay_id,
        }

    def ensure_monitoring(self):
        if self.observer is not None:
            return
        replay_monitor = self
        class SetReplayId(LoggingEventHandler):
            def on_modified(set_replay_id_self, event):
                if event.is_directory: return
                assert event.src_path.endswith('.replay')
                nonlocal replay_monitor
                replay_path = Path(event.src_path)
                if replay_monitor.replay_preference == ReplayPreference.CALCULATED_GG:
                    upload_to_calculated_gg(replay_path)
                replay_monitor.replay_id = parse_replay_id(replay_path)

            def on_created(self, event):
                pass
            def on_deleted(self, event):
                pass
            def on_moved(self, event):
                pass

        self.observer = Observer()
        self.observer.daemon = True
        self.observer.schedule(SetReplayId(), str(get_replay_dir()), recursive=True)
        self.observer.start()

    def stop_monitoring(self):
        self.observer.stop()
        self.observer.join(1)

def get_replay_dir() -> Path:
    replay_dir = Path.home() / 'My Documents' / 'My Games' / 'Rocket League' / 'TAGame' / 'Demos'
    assert replay_dir.exists()
    return replay_dir
