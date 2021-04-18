import asyncio

import discord
from discord.ext import commands,tasks
import requests
import json

prefix = '?'

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
client = commands.Bot(command_prefix=prefix, intents=intents)

@client.command()
async def status(ctx):
    waitResponse = discord.Embed(title='**Getting API info**',description='Please wait a second! We are getting the info...',color=discord.Color.blue())

    myMassage = await ctx.send(embed=waitResponse)

    statusRequest = requests.get('https://status.mojang.com/check')

    parsedResponse = json.loads(statusRequest.text)

    statuses = {}
    for data in parsedResponse:
        for key in data:

            serverNowChecking = key
            serverStatusNow = data[key].replace("green",":white_check_mark:").replace("yellow",":warning:").replace("red",":negative_squared_cross_mark:")

            statuses[serverNowChecking] = f'**{serverNowChecking} status is {serverStatusNow}**'

    embedResponse = discord.Embed(title='**API services**',description=f'{statuses["minecraft.net"]} \n\n {statuses["session.minecraft.net"]} \n\n {statuses["account.mojang.com"]} \n\n {statuses["authserver.mojang.com"]} \n\n {statuses["sessionserver.mojang.com"]} \n\n {statuses["api.mojang.com"]} \n\n {statuses["textures.minecraft.net"]} \n\n {statuses["mojang.com"]}',color=discord.Color.blue())

    await asyncio.sleep(1)
    await myMassage.edit(embed=embedResponse)
@client.command()
async def to_uuid(ctx,*,username=None):
    if username == None:
        responsedEmbed = discord.Embed(title='**Error**',description='You did not entered any username to convert it to UUID!',color=discord.Color.red())
        await ctx.send(embed=responsedEmbed)
    else:
        response = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}')
        data = json.loads(response.text)

        print(response.text)
        if response.status_code == 200:
            respondEmbed = discord.Embed(title='**Succes**',description=f'The UUID for username {username} is {data["id"]}',color=discord.Color.green())
            await ctx.send(embed=respondEmbed)
        elif response.status_code == 204:
            respondEmbed = discord.Embed(title='**Error**',description=f'No UUID for username {username} was not found! Please check typing your username!',color=discord.Color.red())
            await ctx.send(embed=respondEmbed)

client.run('ODMzNDM2MDQ2Nzc5NjEzMjM0.YHyTzg.zAe4J3nCNytS4jBtXGehAXJBa6A')