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