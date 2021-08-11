from riotwatcher import LolWatcher, ApiError
from typing import List, Optional
from pydantic import BaseModel
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize

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

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(320, 140))    
        self.setWindowTitle("LolGsheets") 

        self.gameIdText = QLabel(self)
        self.gameIdText.setText('GAME ID:')
        self.gameId = QLineEdit(self)

        self.gameId.move(80, 20)
        self.gameId.resize(200, 32)
        self.gameIdText.move(20, 20)

        enterButton = QPushButton('ENTER', self)
        enterButton.clicked.connect(self.clickMethod)
        enterButton.resize(200,32)
        enterButton.move(80, 60)        

    def clickMethod(self):
        print('Entered Game ID: ' + self.gameId.text())

LOLWATCHER = LolWatcher('RGAPI-bc836c0e-e2cd-4468-b513-fd5800205fd3')
REGION = 'na1'
VERISION = LOLWATCHER.data_dragon.versions_for_region(REGION)
CHAMPION_VERSIONS = VERISION['n']['champion']
CURR_CHAMP_LIST = LOLWATCHER.data_dragon.champions(CHAMPION_VERSIONS)


def get_game_data_id(lol_watcher, region, game_id):
    try:
        match = lol_watcher.match.by_id(region, game_id)
        match = Match(**match)
        return match
    except ApiError as err:
        print(err)
    return None

def get_teams_data(game_id):
    curr = get_game_data_id(LOLWATCHER,REGION,game_id)
    champs_in_game = {100:[],200:[]}
    champ_to_id = {}

    for player in curr.participants:
        champs_in_game[player.teamId].append(str(player.championId))

    counted = 0

    for i in CURR_CHAMP_LIST['data'].keys():
        if CURR_CHAMP_LIST['data'][i]['key'] in champs_in_game[100] or CURR_CHAMP_LIST['data'][i]['key'] in champs_in_game[200]:
            champ_to_id[CURR_CHAMP_LIST['data'][i]['key']] = CURR_CHAMP_LIST['data'][i]['id']
            counted+=1
        if counted == 10:
            break
        #print(i + " " + CURR_CHAMP_LIST['data'][i]['key'])

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
