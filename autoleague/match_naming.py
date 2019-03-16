from collections import defaultdict


def get_match_name(match_config) -> str:
    team_to_names = defaultdict(list)
    for player in match_config.player_configs:
        team_to_names[player.team].append(player.name)
    return f'{", ".join(team_to_names[0])} vs {", ".join(team_to_names[1])}'
