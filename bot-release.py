import discord
from discord import *
from discord.ext.commands import Bot

PREFIX = '$'
TokenFile = open("token.token", "r")
Token = TokenFile.readline()

description = "\"Live a life of prosperity, gradual sustainable income, and CONTINUOUS LP GAIN\" - GFLP#9979 \n" + \
              "This is the official bot for GAINFATLP, visit us at http://GainFatLP.com/"
client = Bot(command_prefix=PREFIX, description=description)


@client.event
async def on_message(message):
    flagged = False
    warning_message = "Please use the #voice-text channel when you are connected to voice. This reduces clutter " + \
                      "for other users and makes it easier for them to follow the chat."
    if message.channel.type != discord.ChannelType.private:
        for roles in message.author.roles:
            if roles.name == "Non-Vocalizer":
                flagged = True
        if flagged and message.channel.name != "voice-text" and message.author.voice.self_mute \
                and message.author.voice.voice_channel is not None:
            await client.delete_message(message)
            await client.start_private_message(user=message.author)
            await client.send_message(message.author, content=warning_message)
            print("\n")
            print("message deleted:")
            print(message.content)
            print(message.author)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="GainFatLP.com"))
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
    print("Current servers:")
    for server in client.servers:
        print("{0.name}, ID: {0.id}".format(server))

client.run(Token)
