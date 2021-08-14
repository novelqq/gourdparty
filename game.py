import json
import random
from copy import deepcopy


class Player:
    easyquestpool = []
    medquestpool = []
    hardquestpool = []
    sabotagepool = {}
    activequests = {}
    sabotages = {}
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
    

    def assignnewquests(self):

        
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
            print(player)
            print(gourddata['sabotages'])
            self.players[player].easyquestpool.extend(gourddata['easyquests'])
            self.players[player].medquestpool.extend(gourddata['medquests'])
            self.players[player].hardquestpool.extend(gourddata['hardquests'])
            self.players[player].sabotagepool = deepcopy(gourddata['sabotages'])
            self.players[player].activequests['easy'] = self.players[player].easyquestpool.pop(random.randint(0, len(self.players[player].easyquestpool)-1))
            self.players[player].activequests['med'] = self.players[player].medquestpool.pop(random.randint(0, len(self.players[player].medquestpool)-1))
            self.players[player].activequests['hard'] = self.players[player].hardquestpool.pop(random.randint(0, len(self.players[player].hardquestpool)-1))
            print(self.players[player].activequests)
            print(self.players[player].sabotagepool)
            #self.players[player].assignnewquests()
        #self.startRound()
        return f'game has started with {len(self.players)} players playing. Check your quests now!'

    def nextRound(self):
        pass

