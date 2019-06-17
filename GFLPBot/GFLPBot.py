import discord
import random
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from discord import *
from discord.ext.commands import Bot
from discord.utils import get
import os
import configparser
import logging

PREFIX = "$"
logging.basicConfig(level=logging.INFO)

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
            self.config.set("General", "bot_channels", "botspam")
            self.config.set("General", "image_channels", "dreg-heap")
            self.config.set("General", "default_role", "Member")
            self.config.set("General", "doge_path", "..\\GFLPBot\\Images\\Doge")
            self.config.set("General", "restricted_users", "")
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
            GFLP_activity = Activity(name="GainFatLP.com", url="https://gainfatlp.com/",
                                     type=discord.ActivityType.playing)
            await self.client.change_presence(activity=GFLP_activity)
            print('Connected!')
            print('Username: ' + self.client.user.name)
            print('ID: ' + str(self.client.user.id))
            print("Current servers:")

            for server in self.client.guilds:
                print("{0.name}, ID: {0.id}".format(server))

        @self.client.event
        async def on_message(message):

            image_channel = self.config.get("General", "image_channels")
            voice_warning = "Please use the #voice-text channel when you are connected to voice." + \
                            "This reduces clutter for other users and makes " + \
                            "it easier for them to follow the chat."
            spam_warning = "Please keep your embedded images and links in the " + image_channel + \
                           " channel. This reduces clutter for other users.\nIf you believe your message " + \
                           "was deleted in error, please contact this bot's author: Verlieren#9842"
            restricted = self.config.get("General", "restricted_users")

            if isinstance(message.channel, discord.TextChannel):
                if message.author.bot:
                    return

                vocal_role = get(message.author.roles, name="Non-Vocalizer")

                if message.channel.name != "voice-text" and vocal_role is not None \
                        and message.author.voice is not None and message.author.voice.self_mute:

                    await message.delete()
                    print("\n")
                    print("Message Deleted:")
                    print(message.content)
                    print(message.author)
                    print(message.created_at)
                    try:
                        await message.author.send(content=voice_warning)
                    except discord.errors.Forbidden:
                        print("User has blocked bot, no DM sent")
                    return

                if message.channel.name not in image_channel and str(message.author.id) in restricted:
                    contains_url = False
                    val = URLValidator()
                    try:
                        val(message.content)
                        contains_url = True
                    except ValidationError:
                        pass

                    if message.attachments or contains_url or message.embeds:
                        await message.delete()
                        print("\n")
                        print("Message Deleted:")
                        print(message.content)
                        print(message.author)
                        print(message.created_at)
                        try:
                            await message.author.send(content=spam_warning)
                        except discord.errors.Forbidden:
                            print("User has blocked bot, no DM sent")
                        return

                if "o tru" in message.content.lower() or "otru" in message.content.lower():
                    truemoji = get(self.client.emojis, name='otru')
                    await message.add_reaction(truemoji)

                if message.content.startswith(PREFIX):
                    await self.client.process_commands(message)

        @self.client.command(name='invite')
        async def create_invite(ctx):

            response = "Permanent invite link for GainFatLP:\n" + self.config.get("General", "invite_link")
            await ctx.send(response)

        @self.client.command(name='avatar')
        async def avatar(ctx):
            embed_image = discord.Embed()
            for mentioned in ctx.message.mentions:
                embed_image.title = mentioned.display_name + "'s avatar"
                embed_image.colour = Color(0x00E5FF)
                embed_image.set_image(url=mentioned.avatar_url)
                await ctx.channel.send(embed=embed_image)

        @self.client.command(name="restrict")
        async def restrict(ctx):
            return
            # add restrict command

        @self.client.command(name='ongod',
                             pass_context=True)
        async def on_god(ctx):
            embed_image = discord.Embed()
            embed_image.colour = Color(0x00E5FF)
            embed_image.set_image(url="https://i.imgur.com/2ZFJOQP.png")
            await ctx.send(embed=embed_image)

        @self.client.command(name='ok',
                             pass_context=True)
        async def ok(ctx):
            embed_image = discord.Embed()
            embed_image.colour = Color(0x00E5FF)
            embed_image.set_image(url="https://i.imgur.com/ImZwATF.jpg")
            await ctx.send(embed=embed_image)

        @self.client.command(name='doge',
                             description='Use at your own risk',
                             pass_context=True)
        async def doge(ctx):
            if ctx.message.channel.name in self.config.get("General", "spam_channels"):
                disabledmessage = "Sorry, this command is currently disabled."
                await ctx.send(disabledmessage)
            # listoffile = os.listdir(self.config.get("General", "doge_path"))
            # allfiles = list()
            # for entry in listoffile:
            #     fullpath = os.path.join(self.config.get("General", "doge_path"), entry)
            #     allfiles.append(fullpath)
            #
            # with open(str(random.choice(allfiles)), "rb") as image:
            #     await self.client.send_file(ctx.message.channel, image)
            else:
                warning = "Sorry, {0.mention}, that command is limited to the following channels: `{1}`"
                channels = self.config.get("General", "spam_channels")
                await ctx.send(warning.format(ctx.message.author, channels))

        @self.client.event
        async def on_member_join(member):
            default_role = get(member.guild.roles, name=self.config.get("General", "default_role"))
            await member.add_roles(default_role)

            welcome_embed = Embed()
            welcome_embed.colour = Color(0x00E5FF)
            welcome_embed.set_image(url="https://i.imgur.com/IMya4ln.png")
            welcome_embed.url = "https://gainfatlp.com/"
            welcome_embed.title = "Welcome to GainFatLP!"
            welcome_embed.description = "Live a life of prosperity, gradual sustainable income, and continuous LP GAIN!"
            welcome_text = "{0.mention}, Welcome to GAIN FAT LP!\n".format(member) + \
                           "Click the link below to visit our website!"
            welcome_channel = get(member.guild.channels, name=self.config.get("General", "welcome_channel"))
            await welcome_channel.send(welcome_text, embed=welcome_embed)

        @self.client.command()
        async def joined(ctx):
            joined_embed = Embed()
            joined_embed.colour = Color(0x00E5FF)
            for mentioned in ctx.message.mentions:
                joined_embed.title = '{0.display_name} joined at {0.joined_at}'.format(mentioned)
                await ctx.channel.send(embed=joined_embed)

