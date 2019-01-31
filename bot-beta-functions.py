import discord
from discord import *
from discord.ext.commands import Bot
import requests


PREFIX = '$'
TOKEN = 'NTQwMDUzNzI1NzAwNjg1ODQ0.DzO4ag.sfzGuairEh3UDjvUyx4Y-m_CYcc'
SERVER_ID = '497143081628598282'

# description = """\"Live a life of prosperity, gradual sustainable income, and CONTINUOUS LP GAIN\" - GFLP#9979 \n
# This is the official bot for GAINFATLP, visit us at http://GainFatLP.com/"""
client = Bot(command_prefix=PREFIX)

# @client.command()
# async def get_emoji():


@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + ' squared is ' + str(squared_value))


@client.command()
async def joined(name):
    """Says when a member joined."""
    selected = main_vault.get_member_named(name=name)
    await client.say(selected.name)
    await client.say(selected.joined_at)
    #await client.send_message('{0.name} joined in {0.joined_at}'.format(selected))


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await client.say("Bitcoin price is: $" + value)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if "o tru" in message.content:
#         await client.send_message(message.channel, "o tru")

client.run(TOKEN)