from riotwatcher import LolWatcher, ApiError
from typing import List, Optional
from pydantic import BaseModel

class Timeline(BaseModel):
    lane: str
    role: str

class Stats(BaseModel):
    kills: int
    deaths: int
    assists: int
    firstBloodKill: bool
    firstBloodAssist: bool
    totalDamageDealtToChampions: int
    damageDealtToTurrets: int
    damageDealtToObjectives: int
    totalDamageTaken: int
    damageSelfMitigated: int
    totalHeal: int
    totalUnitsHealed: int
    timeCCingOthers: int
    totalTimeCrowdControlDealt: int
    wardsPlaced: int
    visionScore: int
    visionWardsBoughtInGame: int
    wardsKilled: int
    totalMinionsKilled: int
    neutralMinionsKilled: int
    neutralMinionsKilledTeamJungle: int
    neutralMinionsKilledEnemyJungle: int
    turretKills: int
    inhibitorKills: int
    firstTowerKill: bool
    firstTowerAssist: bool
    goldEarned: int
    champLevel: int

class Participant(BaseModel):
    teamId: int
    championId: int
    stats: Stats
    timeline: Timeline

class Team(BaseModel):
    teamId: int
    win: str
    firstBlood: bool
    firstTower: bool
    firstInhibitor: bool
    firstBaron: bool
    firstDragon: bool
    firstRiftHerald: bool
    towerKills: int
    inhibitorKills: int
    baronKills: int
    dragonKills: int
    riftHeraldKills: int


class Match(BaseModel):
    gameId: int
    gameCreation: int
    gameDuration: int
    gameVersion: str
    teams: List[Team] = []
    participants: List[Participant] = []

LOLWATCHER = LolWatcher('RGAPI-bc836c0e-e2cd-4468-b513-fd5800205fd3')
REGION = 'na1'

def get_game_data_id(lol_watcher, region, game_id):
    try:
        match = lol_watcher.match.by_id(region, game_id)
        match = Match(**match)
        return match
    except ApiError as err:
        print(err)
    return None


curr = get_game_data_id(LOLWATCHER,REGION,4006452981)
for i in curr:
    print(i)
