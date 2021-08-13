from riotwatcher import LolWatcher, ApiError
from typing import List, Optional
from pydantic import BaseModel
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QIcon
import urllib

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

CHAMP_IDS = None
CHAMPS_IN_GAME = None

class MainWindow(QMainWindow):

    

    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1020, 800))    
        self.setWindowTitle("LolGsheets") 
        self.setStyleSheet("background-color: #889bbf")

        self.gameIdText = QLabel(self)
        self.gameIdText.setText('GAME ID:')
        self.gameId = QLineEdit(self)

        self.gameId.move(200, 20)
        self.gameId.resize(425, 32)
        self.gameIdText.move(100, 20)

        enterButton = QPushButton('ENTER', self)
        enterButton.clicked.connect(self.clickMethod)
        enterButton.resize(200,32)
        enterButton.move(300, 60)
        enterButton.setStyleSheet("background-color: white")

        self.blueTop = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/top.png")
        self.blueTop.setPixmap(self.pixmap)
        self.blueTop.resize(self.pixmap.width(), self.pixmap.height())
        self.blueTop.move(50,100)

        self.blueJungle = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/jungle.png")
        self.blueJungle.setPixmap(self.pixmap)
        self.blueJungle.resize(self.pixmap.width(), self.pixmap.height())
        self.blueJungle.move(50,200)

        self.blueMid = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/mid.png")
        self.blueMid.setPixmap(self.pixmap)
        self.blueMid.resize(self.pixmap.width(), self.pixmap.height())
        self.blueMid.move(50,300)

        self.blueAdc = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/bottom.png")
        self.blueAdc.setPixmap(self.pixmap)
        self.blueAdc.resize(self.pixmap.width(), self.pixmap.height())
        self.blueAdc.move(50,400)

        self.blueSupport = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/support.png")
        self.blueSupport.setPixmap(self.pixmap)
        self.blueSupport.resize(self.pixmap.width(), self.pixmap.height())
        self.blueSupport.move(50,500)

        self.redTop = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/top.png")
        self.redTop.setPixmap(self.pixmap)
        self.redTop.resize(self.pixmap.width(), self.pixmap.height())
        self.redTop.move(706,100)

        self.redJungle = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/jungle.png")
        self.redJungle.setPixmap(self.pixmap)
        self.redJungle.resize(self.pixmap.width(), self.pixmap.height())
        self.redJungle.move(706,200)

        self.redMid = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/mid.png")
        self.redMid.setPixmap(self.pixmap)
        self.redMid.resize(self.pixmap.width(), self.pixmap.height())
        self.redMid.move(706,300)

        self.redAdc = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/bottom.png")
        self.redAdc.setPixmap(self.pixmap)
        self.redAdc.resize(self.pixmap.width(), self.pixmap.height())
        self.redAdc.move(706,400)

        self.redSupport = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/support.png")
        self.redSupport.setPixmap(self.pixmap)
        self.redSupport.resize(self.pixmap.width(), self.pixmap.height())
        self.redSupport.move(706,500)

    def clickMethod(self):
        print('Entered Game ID: ' + self.gameId.text())
        CHAMP_IDS, CHAMPS_IN_GAME = get_teams_data(self.gameId.text())

        yPos = 100
        i = 0
        space = 40
        for teams in CHAMPS_IN_GAME.values():
            for champId in teams:
                url = "http://ddragon.leagueoflegends.com/cdn/" + CHAMPION_VERSIONS + "/img/champion/" + CHAMP_IDS[champId] + ".png"
                data = urllib.request.urlopen(url).read()
                self.pixMap = QPixmap()
                self.pixMap.loadFromData(data)
                label = QtWidgets.QLabel(self)
                label.setPixmap(self.pixMap)
                label.resize(120,120)
                if(i < 5):
                    label.move(200,yPos + space * i)
                else:
                    label.move(600, yPos - 500 + space * (i - 5))
                label.show()
                yPos+=100
                i+=1

        # url = "http://ddragon.leagueoflegends.com/cdn/" + CHAMPION_VERSIONS + "/img/champion/" + str(CHAMP_IDS["131"]) + ".png"
        # data = urllib.request.urlopen(url).read()
        # self.pixMap = QPixmap()
        # self.pixMap.loadFromData(data)
        # label = QtWidgets.QLabel(self)
        # label.setPixmap(self.pixMap)
        # label.move(100,100)
        # label.resize(120,120)
        # label.show()


LOLWATCHER = LolWatcher('RGAPI-01def34c-ba3e-4734-ae9a-8720145eee9f')
REGION = 'na1'
VERISION = LOLWATCHER.data_dragon.versions_for_region(REGION)
CHAMPION_VERSIONS = VERISION['n']['champion']
CURR_CHAMP_LIST = LOLWATCHER.data_dragon.champions(CHAMPION_VERSIONS)
game_id = 4008089613

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
    return champ_to_id, champs_in_game

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit( app.exec_() )
