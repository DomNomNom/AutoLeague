from pathlib import Path
from typing import Optional
from enum import Enum
import time
import requests

from pywinauto import Desktop, Application, keyboard
from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer


class ReplayPreference(Enum):
    DISCARD = 'discard'  # Does not Save the replay
    SAVE = 'save'  # save to the default replays directory
    CALCULATED_GG = 'calculated_gg'  # save locally and upload to http://calculated.gg/

def handle_replay_saving_while_on_endscreen(action: ReplayPreference) -> Optional[str]:
    if action == ReplayPreference.DISCARD:
        return None

    replay_path = save_replay_while_on_endscreen()
    if replay_path is None:
        return None
    replay_id = parse_replay_id(replay_path)

    if action == ReplayPreference.CALCULATED_GG:
        upload_to_calculated_gg(replay_path)

    return replay_id

def upload_to_calculated_gg(replay_path: Path):
    with open(replay_path, 'rb') as f:
        response = requests.post('http://calculated.gg/api/upload', files={replay_path.name: f})
        print('upload_to_calculated_gg: ', response, response.body)

def parse_replay_id(replay_path: Path) -> str:
    replay_id, extension = replay_path.name.split('.')
    assert extension == 'replay'
    return replay_id


def save_replay_while_on_endscreen() -> Path:
    """
    Ensures that the replay is written to disk after the
    """

    replay_path = None
    observer = Observer()
    class StopOnReplaySaved(LoggingEventHandler):
        def on_modified(self, event):
            if event.is_directory: return
            assert event.src_path.endswith('.replay')
            nonlocal replay_path
            nonlocal observer
            replay_path = Path(event.src_path)
            print('replay_path', replay_path)
            observer.stop()

        def on_created(self, event):
            pass
        def on_deleted(self, event):
            pass
        def on_moved(self, event):
            pass

    observer.schedule(StopOnReplaySaved(), str(get_replay_dir()), recursive=True)
    observer.start()
    send_save_replay_keystrokes()
    observer.join(5)  # observer.stop() should get called when the replay file is written
    if replay_path is None:
        print('omg no replay')

    return replay_path

def get_replay_dir() -> Path:
    replay_dir = Path.home() / 'My Documents' / 'My Games' / 'Rocket League' / 'TAGame' / 'Demos'
    assert replay_dir.exists()
    return replay_dir

def send_save_replay_keystrokes():
    # Note: make sure the script is running as Administrator!
    app = Application(backend="uia").connect(path="RocketLeague.exe", title="Rocket League")
    window = app.Window_()
    window.type_keys(
        # For some reason this only puts the first character of "autoleague"
        # into the text box. I've tried a bunch of things to get this to work.
        # Good luck debugging this.
        '{DOWN}{DOWN}{ENTER}AutoLeague{ENTER}',
        pause=0.2,
        set_foreground=True,
    )
    time.sleep(2) # replay saving can take a little bit of time
    window.type_keys(
        '{ENTER}',
        set_foreground=True,
    )
