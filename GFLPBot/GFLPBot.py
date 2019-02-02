import discord
import random
from discord import *
from discord.ext.commands import Bot
from discord.utils import get
import os

PREFIX = "$"
INVITELINK = "https://discord.gg/VnbX8JH"

class GFLPBot:

    def __init__(self):

        with open("token.token") as token_file:
            self.token = token_file.readline().strip()
        description = "\"Live a life of prosperity, gradual sustainable income, and CONTINUOUS LP GAIN\"" + \
                      " - GFLP#9979 \nThis is the official bot for GAINFATLP," + \
                      " visit us at http://GainFatLP.com/"
        self.client = Bot(command_prefix=PREFIX, description=description)
        self.setup()

    def run(self):
        print("Running...")
        self.client.run(self.token)

    def setup(self):

        @self.client.event
        async def on_ready():
            await self.client.change_presence(game=Game(name="GainFatLP.com"))
            print('Connected!')
            print('Username: ' + self.client.user.name)
            print('ID: ' + self.client.user.id)
            print("Current servers:")
            for server in self.client.servers:
                print("{0.name}, ID: {0.id}".format(server))

        @self.client.event
        async def on_message(message):
            warning_message = "Please use the #voice-text channel when you are connected to voice." + \
                              "This reduces clutter for other users and makes" + \
                              " it easier for them to follow the chat."

            if message.channel.type != discord.ChannelType.private:

                if message.author.bot:
                    return

                role = get(message.author.roles, name="Non-Vocalizer")

                if message.channel.name != "voice-text" and role is not None and message.author.voice.self_mute \
                        and message.author.voice.voice_channel is not None:
                    await self.client.delete_message(message)
                    print("\n")
                    print("Message Deleted:")
                    print(message.content)
                    print(message.author)
                    print(message.timestamp)
                    try:
                        await self.client.send_message(destination=message.author, content=warning_message)
                    except discord.errors.Forbidden:
                        print("User has blocked bot, no DM sent")
                    return

            if "o tru" in message.content or "otru" in message.content:
                emoji = get(self.client.get_all_emojis(), name='otru')
                await self.client.add_reaction(message, emoji)

            if message.content.startswith(PREFIX):
                await self.client.process_commands(message)

        @self.client.command(name='invite')
        async def create_invite():

            response = "Permanent invite link for GainFatLP:\n" + INVITELINK
            await self.client.say(response)

        @self.client.command(name='ongod',
                             pass_context=True)
        async def on_god(ctx):
            with open("..\\Images\\Misc\\on_god.png", "rb") as f:
                await self.client.send_file(ctx.message.channel, f)

        @self.client.command(name='ok',
                             pass_context=True)
        async def ok(ctx):
            with open("..\\Images\\Misc\\ok.jpg", "rb") as f:
                await self.client.send_file(ctx.message.channel, f)

        @self.client.command(name='doge',
                             description='Use at your own risk',
                             pass_context=True)
        async def doge(ctx):
            listOfFile = os.listdir("..\\Images\\Doge")
            allFiles = list()
            for entry in listOfFile:
                fullPath = os.path.join("..\\Images\\Doge", entry)
                allFiles.append(fullPath)

            with open(str(random.choice(allFiles)), "rb") as image:
                await self.client.send_file(ctx.message.channel, image)
