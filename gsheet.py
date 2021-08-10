from riotwatcher import LolWatcher, ApiError

lol_watcher = LolWatcher('RGAPI-0fd83fbb-314d-421a-9baf-c73ff5379e1a')

my_region = 'na1'

me = lol_watcher.summoner.by_name(my_region, 'Swoh')
print(me)

def get_game_data_id(lol_watcher, region, game_id):
    try:
        match = lol_watcher.match.by_id(region, game_id)
        match = Match(**match)
        return match
    except ApiError as err:
        print(err)
    return None
