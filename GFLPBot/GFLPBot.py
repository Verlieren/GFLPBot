import discord
from discord import *
from discord.ext.commands import Bot

PREFIX = "$"
InviteLink = "https://discord.gg/VnbX8JH"


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
            flagged = False
            warning_message = "Please use the #voice-text channel when you are connected to voice." + \
                              "This reduces clutter for other users and makes" + \
                              " it easier for them to follow the chat."

            if message.channel.type != discord.ChannelType.private:

                if message.author.bot:
                    return

                for roles in message.author.roles:
                    if roles.name == "Non-Vocalizer":
                        flagged = True

                if flagged and message.channel.name != "voice-text" and message.author.voice.self_mute \
                        and message.author.voice.voice_channel is not None:
                    await self.client.delete_message(message)
                    print("\n")
                    print("Message Deleted:")
                    print(message.content)
                    print(message.author)
                    try:
                        await self.client.start_private_message(user=message.author)
                        await self.client.say(message.author, content=warning_message)
                    except discord.errors.Forbidden:
                        print("User has blocked bot, no DM sent")

                if message.content.startswith(PREFIX):
                    await self.client.process_commands(message)
