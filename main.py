import os
import random
import json
from copy import deepcopy
from pymongo import message

from pymongo.message import _randint
from werkzeug.datastructures import ContentRange
import env
import game
import enum
from flask import Flask
from flask_discord_interactions import *
from pymongo import MongoClient
from pymongo import ReturnDocument

from discord_webhook import DiscordWebhook
client = MongoClient("PRIVATE_KEY")
db = client.gourdparty

judgeid = '874559171759071263'
contestantid = '874558995233394708'
mucus = '874558761119936563'

class QuestDifficulty(enum.Enum):
    easy = "easy"
    med = "med"
    hard = "hard"

class playerName(enum.Enum):
    Ryan = "209111087537192961"
    Lache = "189329174002008064"
    Max = "447594892458328082"
    Blake = "185627412321533953"
    Alex = "811965046849536043"

class sabotageenum(enum.Enum):
    sab1 = "sab1"
    sab2 ='sab2'
    sab3 ='sab3'
    sab4 ='sab4'
    sab5 ='sab5'
    sab6 ='sab6'
    sab7 ='sab7'
    sab8 ='sab8'
    sab9 ='sab9'
    sab10 ='sab10'
    sab11 ='sab11'
    sab12 ='sab12'
    sab13 ='sab13'
    sab14 ='sab14'
    sab15 ='sab15'
    sab16= 'sab16'
    sab17 = 'sab17'
    sab18 = 'sab18'
    sab19 = 'sab19'
    sab20 = 'sab20'
    sab21 = 'sab21'
    sab22 = 'sab22'
    sab23 = 'sab23'
    sab24 = 'sab24'
    sab25 = 'sab25'
    sab26 = 'sab26'
    sab27 = 'sab27'
    sab28 = 'sab28'
    sab29 = 'sab29'
    sab30 = 'sab30'

app = Flask(__name__)
discord = DiscordInteractions(app)

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_CLIENT_ID"]
app.config["DISCORD_PUBLIC_KEY"] = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_CLIENT_SECRET"]


@discord.command()
def ping(ctx):
    "Respond with a friendly 'pong'!"
    return "Pong!"

@discord.command()
def leaderboard(ctx):
    "Current GourdParty point totals"
    players = 'Leaderboard:\n'
    for player in db.users.find({}).sort("points", -1):
        if(player['discordid'] != '534509337457065984'):
            players = players + player['name'] + ': ' + str(player['points']) + ' points. ' + str(len(player['sabotages'])) + ' sabotages currently applied.\n'
    
    return Response(players, ephemeral=True)

@discord.command()
def refreshquestpool(ctx):
    "Adds back all removed quests into the possible quest pool and removes all active quests."
    if(contestantid in ctx.author.roles):
        f = open('gourddata.json',)
        gourddata = json.load(f)
        db.users.find_one_and_update({"discordid": ctx.author.id}, {'$set': {
            "easyquestpool": gourddata['easyquests'],
            "medquestpool": gourddata['medquests'],
            "hardquestpool":gourddata['hardquests'],
            "activequests": {'easy': {}, 'med': {}, 'hard': {}}
            }}
        )
        return Response("Quest pool refreshed.")
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command()
def refreshsabotagepool(ctx):
    "Adds back all removed sabotages into the possible sabotage pool and removes all active sabotages."
    if(contestantid in ctx.author.roles):
        f = open('gourddata.json',)
        gourddata = json.load(f)
        db.users.find_one_and_update({"discordid": ctx.author.id}, {'$set': {
            "sabotagepool": gourddata['sabotages'],
            "sabotages": {}
            }}
        )
        return Response("Sabotage pool refreshed.")
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command()
def removesabotages(ctx):
    if(contestantid in ctx.author.roles):
        db.users.find_one_and_update({"discordid": ctx.author.id}, {'$set': {
            "sabotages": {}
            }}
        )
        return Response("Sabotages removed.", ephemeral=True)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)
@discord.command()
def getquests(ctx):
    "Assign new quests for yourself."
    if(contestantid in ctx.author.roles):
        myUser = db.users.find_one({"discordid": ctx.author.id})
        easyquest = myUser.get('easyquestpool').pop(random.randint(0,len(myUser.get('easyquestpool'))-1))
        medquest = myUser.get('medquestpool').pop(random.randint(0,len(myUser.get('medquestpool'))-1))
        hardquest = myUser.get('hardquestpool').pop(random.randint(0, len(myUser.get('hardquestpool'))-1))
        myUser["activequests"]['easy'] = easyquest
        myUser["activequests"]['med'] = medquest
        myUser["activequests"]['hard'] = hardquest
        db.users.find_one_and_update({"discordid": ctx.author.id}, {'$set': {
            "easyquestpool": myUser['easyquestpool'],
            "medquestpool": myUser['medquestpool'],
            "hardquest":myUser['hardquestpool'],
            "activequests": {"easy": easyquest, "med": medquest, "hard": hardquest}}})
        
        quests = f"{easyquest['name']}: \n *{easyquest['desc']}*. {str(easyquest['points'])} points. \n {medquest['name']}: \n *{medquest['desc']}*. {str(medquest['points'])} points. \n {hardquest['name']}: \n *{hardquest['desc']}*. {str(hardquest['points'])} points."
        announcement = myUser['name'] +" was assigned the following quests: \n" + quests
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/874776728214577212/4r1Z01zr3-tj0SyMpSLsRnkoVUvCLC8jhFaZYfoGYq9NQblnweHJ5DMPKzNI4A4zeY47', content=announcement)
        response = webhook.execute()
        print(response)
        return Response("Quests assigned. Check them with /myquests")
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command()
def myquests(ctx):
    "List your current quests."
    if contestantid in ctx.author.roles:
        return Response(str(db.users.find_one({'discordid': ctx.author.id})["activequests"]), ephemeral=True)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command(annotations = {"choice": "Quest Difficulty", "completed": "True or False"})
def handinquest(ctx, choice: QuestDifficulty, completed: bool):
    if contestantid in ctx.author.roles:
        result = ''
        myuser = db.users.find_one({"discordid": ctx.author.id})
        quest = myuser['activequests'][choice]
        if(len(quest) == 0):
            return Response("No active quest for that difficulty!", ephemeral=True)
        if completed:
            result += str(quest['points']) + " awarded."
            myuser['points'] += quest['points']
        else:
            result += "Returned quest to pool."
            if(choice == 'easy'):
                myuser['easyquestpool'].append(quest)
            elif(choice == 'med'):
                myuser['medquestpool'].append(quest)
            elif(choice =='hard'):
                myuser['hardquestpool'].append(quest)
            else:
                return Response("invalid quest difficulty", ephemeral=True)
        myuser['activequests'][choice] = {}
        db.users.find_one_and_update({"discordid": ctx.author.id}, {'$set': {
            "points": myuser['points'],
            "activequests": myuser['activequests'],
            "easyquestpool": myuser['easyquestpool'],
            "medquestpool": myuser['medquestpool'],
            "hardquest":myuser['hardquestpool']
        }})
        announcement = myuser['name'] + " has handed in the following quest: \n" + str(quest) + '\n Completed: ' + str(completed)
        webhook = DiscordWebhook(url='https://discord.com/api/webhooks/874776728214577212/4r1Z01zr3-tj0SyMpSLsRnkoVUvCLC8jhFaZYfoGYq9NQblnweHJ5DMPKzNI4A4zeY47', content=announcement)
        response = webhook.execute()
        print(response)
        return Response('Quest handed in. ' + result)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command()
def mypoints(ctx):
    "Lists your total points available."
    if contestantid in ctx.author.roles or mucus in ctx.author.roles:
        return Response(str(db.users.find_one({"discordid": ctx.author.id})['points']) + ' points available.', ephemeral=True)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command()
def kingshitpoints(ctx):
    "Lists the amount of points available to Mucus."
    return Response(str(db.users.find_one({"discordid": '534509337457065984'})['points']) + ' points available.', ephemeral=True)

@discord.command()
def mysabotages(ctx):
    "Lists sabotages against you."
    if contestantid in ctx.author.roles:
        return Response(str(db.users.find_one({"discordid": ctx.author.id})['sabotages']), ephemeral=True)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command(annotations={"target": "Target to recieve points", "amount": "number of points to be given"})
def givepoints(ctx, target: playerName, amount: int):
    if judgeid in ctx.author.roles:
        myuser = db.users.find_one({"discordid": target})
        myuser['points'] += amount
        db.users.find_one_and_update({"discordid": ctx.author.id}, {'$set': {
        "points": myuser['points']}})
        return Response(f"{myuser['name']} was awarded {amount} points by Judge Ari.")
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.custom_handler()
def handle_sabotage(ctx, interaction_id, origin_id, target_id, sabotage):
    if ctx.author.id == origin_id:
        origin_user = db.users.find_one({"discordid": origin_id})
        target_user = db.users.find_one({"discordid": target_id})
        if(origin_user['points'] >= target_user['sabotagepool'][sabotage]['cost']):
            origin_user['points'] -= target_user['sabotagepool'][sabotage]['cost']
            target_user['sabotages'][sabotage] = (target_user['sabotagepool'].pop(sabotage, None))
            db.users.find_one_and_update({"discordid": origin_id}, {"$set": {'points': origin_user['points']}})
            db.users.find_one_and_update({"discordid": target_id}, { "$set": {
                'sabotagepool': target_user['sabotagepool'],
                'sabotages': target_user['sabotages']
            }})
            announcement = f"{origin_user['name']} just sabotaged {target_user['name']} with the following sabotage: \n {str(target_user['sabotages'][sabotage])}"
            webhook = DiscordWebhook(url='https://discord.com/api/webhooks/874776728214577212/4r1Z01zr3-tj0SyMpSLsRnkoVUvCLC8jhFaZYfoGYq9NQblnweHJ5DMPKzNI4A4zeY47', content=announcement)
            response = webhook.execute()
            print(response)
            return Response(f"Sabotage sent successfully.", update=False, ephemeral=True)
        else:
            return Response("Insufficient points to send sabotage", update=False, ephemeral=True)
@discord.command()
def directsabotage(ctx, target: playerName, sabnumber: str):
    "Sabotage a specific player"
    if(contestantid in ctx.author.roles or mucus in ctx.author.roles):
        origin_user = db.users.find_one({"discordid": ctx.author.id})
        target_user = db.users.find_one({"discordid": target})
        if(sabnumber in target_user['sabotagepool']):
            if(origin_user['points'] >= target_user['sabotagepool'][sabnumber]['cost'] *2):
                origin_user['points'] -= target_user['sabotagepool'][sabnumber]['cost']*2
                newsab = target_user['sabotagepool'].pop(sabnumber, None)
                if newsab == None:
                    return Response("Something went wrong. Report to Ryan", ephemeral=True)
                else:
                    target_user['sabotages'][sabnumber] = newsab
                    db.users.find_one_and_update({"discordid": ctx.author.id}, {"$set": {'points': origin_user['points']}})
                    db.users.find_one_and_update({"discordid": target}, { "$set": {
                        'sabotagepool': target_user['sabotagepool'],
                        'sabotages': target_user['sabotages']
                    }})
                    result = '*' + target_user['sabotages'][sabnumber]['name'] + '*\n\n' + target_user['sabotages'][sabnumber]['desc']
                    announcement = f"{origin_user['name']} just directly sabotaged {target_user['name']} with the following sabotage: \n\n" + result
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/874776728214577212/4r1Z01zr3-tj0SyMpSLsRnkoVUvCLC8jhFaZYfoGYq9NQblnweHJ5DMPKzNI4A4zeY47', content=announcement)
                    response = webhook.execute()
                    print(response)
                    return Response("Sabotage sent successfully.", ephemeral=True)
            else:
                return Response("Insufficient points to send sabotage", ephemeral=True)
        else:
            return Response("Chosen sabotage not available. Was likely applied already. (or wrongly typed)", ephemeral=True)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

@discord.command()
def randomsabotage(ctx, sabnumber: str):
    "Sabotage a random player"
    if(contestantid in ctx.author.roles or mucus in ctx.author.roles):
        target = random.choice(list(playerName)).value
        origin_user = db.users.find_one({"discordid": ctx.author.id})
        target_user = db.users.find_one({"discordid": target})
        if(sabnumber in target_user['sabotagepool']):
            if(origin_user['points'] >= target_user['sabotagepool'][sabnumber]['cost']):
                origin_user['points'] -= target_user['sabotagepool'][sabnumber]['cost']
                newsab = target_user['sabotagepool'].pop(sabnumber, None)
                if newsab == None:
                    return Response("Something went wrong. Report to Ryan", ephemeral=True)
                else:
                    target_user['sabotages'][sabnumber] = newsab
                    db.users.find_one_and_update({"discordid": ctx.author.id}, {"$set": {'points': origin_user['points']}})
                    db.users.find_one_and_update({"discordid": target}, { "$set": {
                        'sabotagepool': target_user['sabotagepool'],
                        'sabotages': target_user['sabotages']
                    }})
                    result = '*' + target_user['sabotages'][sabnumber]['name'] + '*\n\n' + target_user['sabotages'][sabnumber]['desc']
                    announcement = f"{origin_user['name']} just randomly sabotaged {target_user['name']} with the following sabotage: \n\n" + result
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/874776728214577212/4r1Z01zr3-tj0SyMpSLsRnkoVUvCLC8jhFaZYfoGYq9NQblnweHJ5DMPKzNI4A4zeY47', content=announcement)
                    response = webhook.execute()
                    print(response)
                    return Response("Sabotage sent successfully.", ephemeral=True)
            else:
                return Response("Insufficient points to send sabotage", ephemeral=True)
        else:
            return Response("Chosen sabotage not available. Was likely applied already. (or wrongly typed)", ephemeral=True)
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

# def directsabotage(ctx, target: playerName, sabnumber: str):
#     "Sabotage a specific player"
#     if(contestantid in ctx.author.roles):
#         mycomponents = []
#         targetuser = db.users.find_one({"discordid": target})
#         for sabotage in targetuser['sabotagepool']:
#             print("sabotage: ", sabotage)
#             mycomponents.append(
#                 ActionRow(
#                     components=[
#                         Button(
#                             style=ButtonStyles.PRIMARY, 
#                             custom_id=[handle_sabotage, ctx.author.id, target, sabotage], 
#                             label=sabotage + " - Cost: " + str(targetuser['sabotagepool'][sabotage]['cost'])
#                         )
#                     ]
#                 )
#             )
#         return Response(
#             content=f"Choose an available sabotage against this player.",
#             components=mycomponents,
#             ephemeral=True
#         )
#     else:
#         return Response("You are not allowed to use this command!", ephemeral=True)
@discord.command()
def sabotageinfo(ctx, sabotage: str):
    f = open('gourddata.json',)
    gourddata = json.load(f)
    result = '*' + gourddata['sabotages'][sabotage]['name'] + '*\n\n' + gourddata['sabotages'][sabotage]['desc'] + ' Costs ' + str(gourddata['sabotages'][sabotage]['cost']) + ' points.\n\n'
    return Response(result)

@discord.command()
def refreshtargetsabotages(ctx, player: playerName):
    if(contestantid in ctx.author.roles):
        f = open('gourddata.json',)
        gourddata = json.load(f)
        db.users.find_one_and_update({"discordid": player}, {'$set': {
            "sabotagepool": gourddata['sabotages'],
            "sabotages": {}
            }}
        )
        return Response("Sabotage pool refreshed.")
    else:
        return Response("You are not allowed to use this command!", ephemeral=True)

discord.set_route("/interactions")
discord.update_slash_commands(guild_id=os.environ["TESTING_GUILD"])


if __name__ == '__main__':
    app.run()
