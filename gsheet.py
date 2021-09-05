from oauth2client.service_account import ServiceAccountCredentials
from riotwatcher import LolWatcher, ApiError
from typing import List, Optional
from pydantic import BaseModel
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QApplication
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon, QPainter, QColor, QPen
import urllib
import gspread
import time
import sys

scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("lolgsheet.json",scope)
client = gspread.authorize(creds)

topSheet = client.open("LoLGSheet").worksheet("Top")
jungleSheet = client.open("LoLGSheet").worksheet("Jungle")
midSheet = client.open("LoLGSheet").worksheet("Mid")
adcSheet = client.open("LoLGSheet").worksheet("Marksman")
supportSheet = client.open("LoLGSheet").worksheet("Support")
sheets = [topSheet,jungleSheet,midSheet,adcSheet,supportSheet]

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

        sendInfoButton = QPushButton('To GSheet',self)
        sendInfoButton.clicked.connect(self.sendMethod)
        sendInfoButton.resize(200,32)
        sendInfoButton.move(700, 40)
        sendInfoButton.setStyleSheet("background-color: white")

        self.blueTop = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/top.png")
        self.blueTop.setPixmap(self.pixmap)
        self.blueTop.resize(self.pixmap.width(), self.pixmap.height())
        self.blueTop.move(50,100)

        self.blueJungle = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/jungle.png")
        self.blueJungle.setPixmap(self.pixmap)
        self.blueJungle.resize(self.pixmap.width(), self.pixmap.height())
        self.blueJungle.move(50,240)

        self.blueMid = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/mid.png")
        self.blueMid.setPixmap(self.pixmap)
        self.blueMid.resize(self.pixmap.width(), self.pixmap.height())
        self.blueMid.move(50,380)

        self.blueAdc = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/bottom.png")
        self.blueAdc.setPixmap(self.pixmap)
        self.blueAdc.resize(self.pixmap.width(), self.pixmap.height())
        self.blueAdc.move(50,520)

        self.blueSupport = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/support.png")
        self.blueSupport.setPixmap(self.pixmap)
        self.blueSupport.resize(self.pixmap.width(), self.pixmap.height())
        self.blueSupport.move(50,660)

        self.redTop = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/top.png")
        self.redTop.setPixmap(self.pixmap)
        self.redTop.resize(self.pixmap.width(), self.pixmap.height())
        self.redTop.move(830,100)

        self.redJungle = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/jungle.png")
        self.redJungle.setPixmap(self.pixmap)
        self.redJungle.resize(self.pixmap.width(), self.pixmap.height())
        self.redJungle.move(830,240)

        self.redMid = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/mid.png")
        self.redMid.setPixmap(self.pixmap)
        self.redMid.resize(self.pixmap.width(), self.pixmap.height())
        self.redMid.move(830,380)

        self.redAdc = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/bottom.png")
        self.redAdc.setPixmap(self.pixmap)
        self.redAdc.resize(self.pixmap.width(), self.pixmap.height())
        self.redAdc.move(830,520)

        self.redSupport = QLabel(self)
        self.pixmap = QPixmap("Lane pngs/support.png")
        self.redSupport.setPixmap(self.pixmap)
        self.redSupport.resize(self.pixmap.width(), self.pixmap.height())
        self.redSupport.move(830,660)

        #######################################################################
        ##############             BLUE SIDE BUTTONS            ###############
        #######################################################################

        blueTopButton = QPushButton(self)
        blueTopButton.resize(60,60)
        blueTopButton.move(365, 130)
        blueTopButton.setIcon(QIcon('Lane pngs/down.png'))
        blueTopButton.setIconSize(QtCore.QSize(60,60))
        blueTopButton.setStyleSheet("background-color: white")

        blueJungleUpButton = QPushButton(self)
        blueJungleUpButton.resize(60,60)
        blueJungleUpButton.move(330, 270)
        blueJungleUpButton.setIcon(QIcon('Lane pngs/up.png'))
        blueJungleUpButton.setIconSize(QtCore.QSize(60,60))
        blueJungleUpButton.setStyleSheet("background-color: white")

        blueJungleDownButton = QPushButton(self)
        blueJungleDownButton.resize(60,60)
        blueJungleDownButton.move(400, 270)
        blueJungleDownButton.setIcon(QIcon('Lane pngs/down.png'))
        blueJungleDownButton.setIconSize(QtCore.QSize(60,60))
        blueJungleDownButton.setStyleSheet("background-color: white")

        blueMidUpButton = QPushButton(self)
        blueMidUpButton.resize(60,60)
        blueMidUpButton.move(330, 410)
        blueMidUpButton.setIcon(QIcon('Lane pngs/up.png'))
        blueMidUpButton.setIconSize(QtCore.QSize(60,60))
        blueMidUpButton.setStyleSheet("background-color: white")

        blueMidDownButton = QPushButton(self)
        blueMidDownButton.resize(60,60)
        blueMidDownButton.move(400, 410)
        blueMidDownButton.setIcon(QIcon('Lane pngs/down.png'))
        blueMidDownButton.setIconSize(QtCore.QSize(60,60))
        blueMidDownButton.setStyleSheet("background-color: white")

        blueBottomUpButton = QPushButton(self)
        blueBottomUpButton.resize(60,60)
        blueBottomUpButton.move(330, 550)
        blueBottomUpButton.setIcon(QIcon('Lane pngs/up.png'))
        blueBottomUpButton.setIconSize(QtCore.QSize(60,60))
        blueBottomUpButton.setStyleSheet("background-color: white")

        blueBottomDownButton = QPushButton(self)
        blueBottomDownButton.resize(60,60)
        blueBottomDownButton.move(400, 550)
        blueBottomDownButton.setIcon(QIcon('Lane pngs/down.png'))
        blueBottomDownButton.setIconSize(QtCore.QSize(60,60))
        blueBottomDownButton.setStyleSheet("background-color: white")

        blueSuportButton = QPushButton(self)
        blueSuportButton.resize(60,60)
        blueSuportButton.move(365, 690)
        blueSuportButton.setIcon(QIcon('Lane pngs/up.png'))
        blueSuportButton.setIconSize(QtCore.QSize(60,60))
        blueSuportButton.setStyleSheet("background-color: white")

        #######################################################################
        ###############             RED SIDE BUTTONS            ###############
        #######################################################################

        redTopButton = QPushButton(self)
        redTopButton.resize(60,60)
        redTopButton.move(595, 130)
        redTopButton.setIcon(QIcon('Lane pngs/down.png'))
        redTopButton.setIconSize(QtCore.QSize(60,60))
        redTopButton.setStyleSheet("background-color: white")

        redJungleUpButton = QPushButton(self)
        redJungleUpButton.resize(60,60)
        redJungleUpButton.move(560, 270)
        redJungleUpButton.setIcon(QIcon('Lane pngs/up.png'))
        redJungleUpButton.setIconSize(QtCore.QSize(60,60))
        redJungleUpButton.setStyleSheet("background-color: white")

        redJungleDownButton = QPushButton(self)
        redJungleDownButton.resize(60,60)
        redJungleDownButton.move(630, 270)
        redJungleDownButton.setIcon(QIcon('Lane pngs/down.png'))
        redJungleDownButton.setIconSize(QtCore.QSize(60,60))
        redJungleDownButton.setStyleSheet("background-color: white")

        redMidUpButton = QPushButton(self)
        redMidUpButton.resize(60,60)
        redMidUpButton.move(560, 410)
        redMidUpButton.setIcon(QIcon('Lane pngs/up.png'))
        redMidUpButton.setIconSize(QtCore.QSize(60,60))
        redMidUpButton.setStyleSheet("background-color: white")

        redMidDownButton = QPushButton(self)
        redMidDownButton.resize(60,60)
        redMidDownButton.move(630, 410)
        redMidDownButton.setIcon(QIcon('Lane pngs/down.png'))
        redMidDownButton.setIconSize(QtCore.QSize(60,60))
        redMidDownButton.setStyleSheet("background-color: white")

        redBottomUpButton = QPushButton(self)
        redBottomUpButton.resize(60,60)
        redBottomUpButton.move(560, 550)
        redBottomUpButton.setIcon(QIcon('Lane pngs/up.png'))
        redBottomUpButton.setIconSize(QtCore.QSize(60,60))
        redBottomUpButton.setStyleSheet("background-color: white")

        redBottomDownButton = QPushButton(self)
        redBottomDownButton.resize(60,60)
        redBottomDownButton.move(630, 550)
        redBottomDownButton.setIcon(QIcon('Lane pngs/down.png'))
        redBottomDownButton.setIconSize(QtCore.QSize(60,60))
        redBottomDownButton.setStyleSheet("background-color: white")

        redSuportButton = QPushButton(self)
        redSuportButton.resize(60,60)
        redSuportButton.move(595, 690)
        redSuportButton.setIcon(QIcon('Lane pngs/up.png'))
        redSuportButton.setIconSize(QtCore.QSize(60,60))
        redSuportButton.setStyleSheet("background-color: white")

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setPen(QPen(QColor(0, 0, 0), 3))
        painter.drawLine(510,120,510,750)

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
                    label.move(700, yPos - 500 + space * (i - 5))
                label.show()
                yPos+=100
                i+=1
    
    def sendMethod(self):
        teamSelected = 200

        currGame = get_game_data_id(LOLWATCHER,REGION,self.gameId.text())
        time.sleep(1)
        CHAMP_IDS, CHAMPS_IN_GAME = get_teams_data(self.gameId.text())
        
        totalKills = 0
        for summoner in currGame.participants:
            if summoner.teamId == teamSelected:
                totalKills += summoner.stats.kills

        blue = 0
        if teamSelected == 200:
            blue = 1

        whichSheet = 0
        for player in currGame.participants:
            if player.teamId == teamSelected:  
                playerData = player
                row = 6
                while sheets[whichSheet].cell(row,1).value != None:
                    row = row + 1
                    time.sleep(1)

                basicStats = [self.gameId.text(),currGame.gameCreation,playerData.teamId,CHAMP_IDS[str(playerData.championId)],currGame.gameDuration/60,
                currGame.teams[blue].win]
                kda = (playerData.stats.kills + playerData.stats.assists) / playerData.stats.deaths
                kp =  (playerData.stats.kills + playerData.stats.assists) / totalKills
                killStats = [playerData.stats.kills, playerData.stats.deaths, playerData.stats.assists, kda, kp, 
                playerData.stats.firstBloodKill , playerData.stats.firstBloodAssist]
                damageStats = [playerData.stats.totalDamageDealtToChampions,playerData.stats.damageDealtToTurrets, playerData.stats.damageDealtToObjectives]
                tankingStats = [playerData.stats.totalDamageTaken, playerData.stats.damageSelfMitigated, playerData.stats.totalHeal, 
                playerData.stats.totalUnitsHealed]
                ccStats = [playerData.stats.timeCCingOthers, playerData.stats.totalTimeCrowdControlDealt]
                visionScore = [playerData.stats.wardsPlaced, playerData.stats.visionScore, playerData.stats.visionWardsBoughtInGame,
                playerData.stats.wardsKilled]
                farmStats = [playerData.stats.totalMinionsKilled,playerData.stats.neutralMinionsKilled,playerData.stats.neutralMinionsKilledTeamJungle,playerData.stats.neutralMinionsKilledEnemyJungle]
                objectiveStats = [playerData.stats.turretKills,playerData.stats.inhibitorKills,playerData.stats.firstTowerKill,playerData.stats.firstTowerAssist]
                miscStats = [playerData.stats.goldEarned,playerData.stats.champLevel,(playerData.stats.goldEarned)/(currGame.gameDuration/60)]
                totalStats = [basicStats,killStats,damageStats,tankingStats,ccStats,visionScore,farmStats,objectiveStats,miscStats]
                
                column = 1
                for section in totalStats:
                    for stat in section:
                        sheets[whichSheet].update_cell(row,column,str(stat))
                        column += 1
                        time.sleep(1)
                whichSheet+=1

        


LOLWATCHER = LolWatcher('RGAPI-fa959162-2db2-40a2-883f-ff286ed48e18')
REGION = 'na1'
VERISION = LOLWATCHER.data_dragon.versions_for_region(REGION)
CHAMPION_VERSIONS = VERISION['n']['champion']
CURR_CHAMP_LIST = LOLWATCHER.data_dragon.champions(CHAMPION_VERSIONS)
game_id = 4030696925

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
