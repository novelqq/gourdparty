import os
import env
import game
import enum
from flask import Flask
from flask_discord_interactions import DiscordInteractions
from flask_discord_interactions import Response

class QuestDifficulty(enum.Enum):
    easy = "easy"
    med = "med"
    hard = "hard"

gourdparty_game = game.Game()

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
def listplayers(ctx):
    players = 'List of players:\n'
    if(len(gourdparty_game.players) == 0):
        return "No players"
    for player in gourdparty_game.players:
        players = players + gourdparty_game.players[player].name + '\n'
    
    return players

@discord.command(annotations={"rounds": "The number of rounds"})
def newgame(ctx, rounds: int):
    if game_created == False:
        if '872945305908289627' in ctx.author.roles:
            return Response(f"Gourd Party has started. {rounds} left.")
        else:
            return Response("You are not allowed to use this command!", ephemeral=True)
    else:
        return Response("Game still in progress!", ephemeral=True)

@discord.command()
def startgame(ctx):
    "Starts a game"
    if len(gourdparty_game.players) != 0:
        return gourdparty_game.startGame()
    else:
        return Response("Not enough players!", ephemeral=True)


@discord.command()
def joingame(ctx):
    "Join gourdparty"
    return Response(gourdparty_game.addPlayer(ctx.author.id, ctx.author.display_name), ephemeral=True)

@discord.command(annotations= {"theme": "Theme text"})
def settheme(ctx, theme: str):
    "Set the theme for the current round"
    gourdparty_game.theme = theme
    return Response("Theme set.", ephemeral=True)

@discord.command()
def myquests(ctx):
    "List your current quests."
    return gourdparty_game.players[ctx.author.id].prettyprintquests()

@discord.command(annotations = {"choice": "Quest Difficulty", "completed": "True or False"})
def handinquest(ctx, choice: QuestDifficulty, completed: bool):
    return gourdparty_game.players[ctx.author.id].completequest(choice, completed)

@discord.command()
def mypoints(ctx):
    "Lists your total points available."
    return str(gourdparty_game.players[ctx.author.id].points)
discord.set_route("/interactions")
discord.update_slash_commands(guild_id=os.environ["TESTING_GUILD"])

if __name__ == '__main__':
    app.run()