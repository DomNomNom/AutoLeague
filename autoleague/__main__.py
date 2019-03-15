"""AutoLeague
Runs the training exercise playlist in the given python file.
The playlist has to be provided via a make_default_playlist() function.

Usage:
    autoleague download_bot_pack  [--working_dir=<working_dir>]
    autoleague generate_matches   [--working_dir=<working_dir>] [--num_matches=N]
    autoleague run_matches        [--working_dir=<working_dir>] [--replays=R]
    autoleague (-h | --help)
    autoleague --version

Options:
    --working_dir=<working_dir>  Where to store inputs and outputs of the league.
    --num_matches=N              [default: 5].
    --replays=R                  What to do with the replays of the match. Valid values are 'discard', 'save', and 'calculated_gg'. [default: calculated_gg]
    -h --help                    Show this screen.
    --version                    Show version.
"""

from pathlib import Path
import os
import sys

from docopt import docopt

from autoleague.download_bot_pack import download_bot_pack
from autoleague.generate_matches import generate_matches
from autoleague.paths import WorkingDir
from autoleague.run_matches import run_matches
from autoleague.version import __version__
from autoleague.replays import ReplayPreference

working_dir_env_var = 'AUTOLEAGUE_WORKING_DIR'
working_dir_flag = '--working_dir'

def main():
    arguments = docopt(__doc__, version=__version__)

    working_dir = arguments[working_dir_flag]
    if working_dir is None:
        working_dir = os.environ.get(working_dir_env_var, None)
    if working_dir is None:
        print('The working directory must be specified. You can specify it in one of these ways:')
        print(f'  Use the {working_dir_flag} flag')
        print(f'  Use the {working_dir_env_var} environment variable')
        sys.exit(1)
    working_dir = WorkingDir(Path(working_dir))

    if arguments['download_bot_pack']:
        download_bot_pack(working_dir)
    elif arguments['generate_matches']:
        generate_matches(working_dir, int(arguments['--num_matches']))
    elif arguments['run_matches']:
        replay_preference = ReplayPreference(arguements['--replays'])
        run_matches(working_dir, replay_preference)
    else:
        raise NotImplementedError()

if __name__ == '__main__':
  main()
