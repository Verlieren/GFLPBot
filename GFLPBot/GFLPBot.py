import discord
import random
from discord import *
from discord.ext.commands import Bot
from discord.utils import get
import os
import configparser

PREFIX = "$"


class GFLPBot:

    def __init__(self):

        with open("token.token") as token_file:
            self.token = token_file.readline().strip()
        description = "\"Live a life of prosperity, gradual sustainable income, and CONTINUOUS LP GAIN\"" + \
                      " - GFLP#9979 \nThis is the official bot for GAINFATLP," + \
                      " visit us at http://GainFatLP.com/"
        self.client = Bot(command_prefix=PREFIX, description=description)

        self.config = configparser.ConfigParser()

        if not os.path.isfile("..\\config.ini"):
            self.config.add_section("General")
            self.config.set("General", "invite_link", "https://discord.gg/VnbX8JH")
            self.config.set("General", "welcome_channel", "general")
            self.config.set("General", "channels", "general, botspam, dreg-heap")
            self.config.set("General", "spam_channels", "botspam")
            self.config.set("General", "default_role", "member")
            self.config.set("General", "doge_path", "..\\GFLPBot\\Images\\Doge")
            with open("..\\config.ini", "w") as configfile:
                self.config.write(configfile)
            print("Config file not found, and a new one was generated")
        self.config.read("..\\config.ini")

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

            if "o tru" in message.content.lower() or "otru" in message.content.lower():
                truemoji = get(self.client.get_all_emojis(), name='otru')
                await self.client.add_reaction(message, truemoji)

            if message.content.startswith(PREFIX):
                await self.client.process_commands(message)

        @self.client.command(name='invite')
        async def create_invite():

            response = "Permanent invite link for GainFatLP:\n" + self.config.get("General", "invite_link")
            await self.client.say(response)

        @self.client.command(name='ongod',
                             pass_context=True)
        async def on_god(ctx):
            with open("..\\GFLPBot\\Images\\Misc\\on_god.png", "rb") as f:
                await self.client.send_file(ctx.message.channel, f)

        @self.client.command(name='ok',
                             pass_context=True)
        async def ok(ctx):
            with open("..\\GFLPBot\\Images\\Misc\\ok.jpg", "rb") as f:
                await self.client.send_file(ctx.message.channel, f)

        @self.client.command(name='doge',
                             description='Use at your own risk',
                             pass_context=True)
        async def doge(ctx):
            if ctx.message.channel.name in self.config.get("General", "spam_channels"):
                listoffile = os.listdir(self.config.get("General", "doge_path"))
                allfiles = list()
                for entry in listoffile:
                    fullpath = os.path.join(self.config.get("General", "doge_path"), entry)
                    allfiles.append(fullpath)

                with open(str(random.choice(allfiles)), "rb") as image:
                    await self.client.send_file(ctx.message.channel, image)
            else:
                warning = "Sorry, {0.mention}, that command is limited to the following channels: `{1}`"
                channels = self.config.get("General", "spam_channels")
                await self.client.say(warning.format(ctx.message.author, channels))

        @self.client.event
        async def on_member_join(member):
            role = get(member.server.roles, name=self.config.get("General", "default_role"))
            self.client.add_roles(member, role)
            welcome = "{0.mention}, Welcome to GAIN FAT LP!\n".format(member) + \
                      "Make sure to check out our website, https://GainFatLP.com/!"
            welcomechannel = get(member.server.channels, name=self.config.get("General", "welcome_channel"))
            await self.client.send_message(welcomechannel, welcome)


        # @self.client.command()
        # async def joined(name):
        #     """Says when a member joined."""
        #     selected = ""  #
        #     await self.client.send_message('{0.name} joined in {0.joined_at}'.format(selected))

