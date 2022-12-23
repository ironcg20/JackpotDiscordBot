import interactions
import time
import json

TOKEN = "MTAzNzYyOTMyMDIwMzYxNjI2Ng.GhpR78.NzFqeGnDD0IZdQCArpLiL5CSAmdLtPUZ0fvIuo"
bot = interactions.Client(token=TOKEN)

def getData():
    ## read in the JSON dict of missions in Cache/missions.json
    with open("/Users/harsha/Desktop/Leaderboard/Cache/missions.json", "r") as f:
        data = json.load(f)
    
    if data == None or data == {}:
        data = {}
        data[1053902791321604217] = ["LOLLLLLL", "MYMISSION1", "MY MISSION 2"]
    
    refreshCommands(data)

def refreshCommands(data):
    def makeChoices(myID):
        choices = []
        for missions in data[myID]:
            choices.append(interactions.Choice(name=missions, value=missions))
        if len(choices) == 0:
            choices.append(interactions.Choice(name="No missions available", value="NULL"))
        return choices

    for ids in data.keys():

        @bot.command(
            name="complete",
            description="Verify a completed mission to earn XP",
            scope=ids,
            ## add 3 options, a mission ID (can either be "1", "2", "3"), a description (string), and a file attachment
            options = [
                interactions.Option(name="mission_id", description="Mission ID", type=interactions.OptionType.STRING, required=True, choices=makeChoices(ids)),
                interactions.Option(name="description", description="Description of the mission", type=interactions.OptionType.STRING, required=True),
                interactions.Option(name="file", description="Add an image (optional)", type=interactions.OptionType.ATTACHMENT, required=False)
            ]
        )
                        
        async def verifyMission(ctx: interactions.CommandContext, mission_id: str, description: str, file: interactions.File = None):
            stem = ""
            if file != None:
                stem = f"#|# {file.url}"
            fullName = ctx.author.name + "#" + ctx.author.discriminator
            await ctx.send(f"MISSION SUBMITTED #|# {fullName} #|# {mission_id} #|# {description} " + stem)

        bot.start()

getData()