#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 13:47:33 2021

@author: isaactrussell
"""

import discord, time, sys, os, json, random
import datetime, logging
from discord.ext import tasks

from MessageHandlers import message_has_attachments, list_sounds, delete_sound
from MessageHandlers import format_message

from SoundHandlers import play_sound

class Client(discord.Client):

    async def on_ready(self):
        self.party = {i.name: {} for i in self.guilds}
        self.activity_fp = "activity.json"
        print("RUNNING")
        self.set_up_logging()

    def set_up_logging(self):
        log_format = '%(asctime)s %(message)s'
        logging.basicConfig(filename='discord_log.log',
                            format = log_format,
                            filemode = "a",
                            level = logging.INFO)
        # logging.getLogger('discord').setLevel(logging.WARNING)
        self.log = logging.getLogger("DiscordBotLogger")
        self.log.info("Program started running")

        activity = {"start": datetime.datetime.now().strftime("%m\%d\%Y, %H:%M:%S")}
        for guild in self.guilds:
            activity.update({guild.name: {}})
            for member in guild.members:
                if not member.bot:
                    activity[guild.name].update({member.name: 0})
        with open(self.activity_fp, "w") as f:
            json.dump(activity, f, indent = 2)

    # Main function to check for when people join the party.
    # TODO update to only work with multiple people in the party
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
                if before.channel == None and not after.channel.name == 'afk' and not member.bot:
                    await play_sound(after.channel, member, self.user, self.log)

    async def on_message(self, msg):

        if msg.author == client.user:
            return

        if len(msg.attachments) >= 1 and msg.channel.type == discord.ChannelType.private:
            print("Message has attachments!")
            await message_has_attachments(msg.attachments, msg.author.name)
            sounds = list_sounds(msg.author.name)
            out = format_message(sounds)
            await msg.author.dm_channel.send(out)

        elif msg.content == "list" and msg.channel.type == discord.ChannelType.private:
            print("List sounds for {}".format(msg.author))
            sounds = list_sounds(msg.author.name)
            out = format_message(sounds)
            await msg.author.dm_channel.send(out)

        elif msg.content.startswith("delete"):
            sounds = delete_sound(msg.author.name, msg.content)
            out = format_message(sounds)
            await msg.author.dm_channel.send(out)

def load_token():
    with open("source/Secrets.txt", "r") as f:
        file = f.readlines()[0]
    return file

token = load_token()
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
client = Client(intents = intents)
client.run(token)
