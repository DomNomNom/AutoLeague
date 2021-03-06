# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package

__version__ = '0.2.0'

release_notes = {
    '0.1.0': '''
        - Visualize match results by adding an rlbottraining website extension - DomNomNom
    ''',

    '0.1.0': '''
        - Run full matches using RLBotTraining - DomNomNom
    ''',
}


def get_current_release_notes():
    if __version__ in release_notes:
        return release_notes[__version__]
    return ''


def get_help_text():
    return 'Trouble? Ask on Discord at https://discord.gg/5cNbXgG ' \
           'or report an issue at https://github.com/RLBot/RLBotTraining/issues'


def print_current_release_notes():
    print(f'Version {__version__}')
    print(get_current_release_notes())
    print(get_help_text())
    print('')
