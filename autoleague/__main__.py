"""AutoLeague
Runs the training exercise playlist in the given python file.
The playlist has to be provided via a make_default_playlist() function.

Usage:
    autoleague download_bot_pack  [--working_dir=<working_dir>]
    autoleague generate_matches   [--working_dir=<working_dir>] [--num_matches=N]
    autoleague run_matches        [--working_dir=<working_dir>]
    autoleague (-h | --help)
    autoleague --version

Options:
    --working_dir=<working_dir>  Where to store inputs and outputs of the league.
    --num_matches=N              [default: 5].
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
        generate_matches(working_dir, arguments['--num_matches'])
    elif arguments['run_matches']:
        run_matches(working_dir)

    # REMOVE THIS CRAP BELOW
    return
    if arguments['download_bot_pack']:
        run_module(
            Path(arguments['<python_file>']),
            history_dir=arguments['--history_dir']
        )
    if arguments['history_render_static']:
        server = Server(history_dir=Path(arguments['<history_dir>']))
        server.render_static_website()
    elif arguments['history_dev_server']:
        restart_devserver_on_source_change(
            arguments['<history_dir>'],
            arguments['--host'],
            arguments['--port'],
        )

if __name__ == '__main__':
  main()
