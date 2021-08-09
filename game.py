import json
import random
from copy import deepcopy

class Player:
    easyquestpool = []
    medquestpool = []
    hardquestpool = []
    activequests = {}
    sabotages = []
    isGhost = False
    def __init__(self, name):
        self.name = name
        self.points = 0
    
    def prettyprintquests(self):
        result = "Your active quests:\n\n"
        for quest in self.activequests:
            print(quest)
            print(self.activequests[quest])
            result = result + quest + ": " + self.activequests[quest]['name'] + " - " + self.activequests[quest]['desc'] + str(self.activequests[quest]['points']) + " points.\n\n"
        
        return result
    
    def eliminate(self):
        self.isGhost = True
        self.quests = []
        self.sabotages = []
    
    def assignnewquests(self):
        random.shuffle(self.easyquestpool)
        random.shuffle(self.medquestpool)
        random.shuffle(self.hardquestpool)
        self.activequests['easy'] = self.easyquestpool.pop()
        self.activequests['med'] = self.medquestpool.pop()
        self.activequests['hard'] = self.hardquestpool.pop()
        print("hehehehe", self.activequests)

    def completequest(self, questindex, success):
        if(len(self.activequests[questindex]) == 0):
            return "No active quest for that difficulty!"
        if(success):
            self.points += self.activequests[questindex]['points']
            self.activequests[questindex] = {}
            return "Quest successfully completed. Points awarded."
        else:
            if(questindex == 'easy'):
                self.easyquestpool.append(self.activequests[questindex])
            elif(questindex == 'med'):
                self.medquestpool.append(self.activequests[questindex])
            elif(questindex=='hard'):
                self.hardquestpool.append(self.activequests[questindex])
            else:
                return "invalid quest difficulty"
            self.activequests[questindex] = {}
            return "Quest turned in incomplete. Returned to pool."
        

class Quest:
    completed = False
    def __init__(self, name, desc, points):
        self.name = name
        self.desc = desc
        points = points

class Game:
    #
    players = {}
    sabotagepool = []
    roundcount = 0
    isJoinable = False
    roundtheme = ''
    def __init__(self):
        self.isJoinable = True

    
    def addPlayer(self, discordid, nick):
        if discordid in self.players:
            #player already added
            return 'You are already in the game!'
        self.players[discordid] = Player(nick)
        return 'You are now in the game!'
    
    def sabotagetarget(self, origin, target):
        random.shuffle(self.players[target].sabotagepool)
        sabotage_item = self.players[target].sabotagepool.pop()
        self.players[target].sabotages.append(sabotage_item)
        self.players[origin].points -= sabotage_item.points

    def sabotagerandom(self, origin):
        pass
    
    def startGame(self):
        self.isJoinable = False
        f = open('gourddata.json',)
        gourddata = json.load(f)

        
        for player in self.players:
            self.players[player].easyquestpool = deepcopy(gourddata['easyquests'])
            self.players[player].medquestpool = deepcopy(gourddata['medquests'])
            self.players[player].hardquestpool = deepcopy(gourddata['hardquests'])
        
        self.startRound()
        return f'game has started with {len(self.players)} players playing. Check your quests now!'

    def startRound(self):
        for player in self.players:
            self.players[player].assignnewquests()
    def endRound(self):
        pass

