#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 13:47:33 2021

@author: isaactrussell
"""

import discord, time, sys, os, json, random
import datetime, logging
from discord.ext import tasks

class Client(discord.Client):
    
    async def on_ready(self):
        self.party = {}
        print("RUNNING")
        self.guild_channel = (1, 0)
        self.set_up_logging()
        self.guild_num = 0
    
    def set_up_logging(self):
        log_format = '%(asctime)s %(message)s'
        logging.basicConfig(filename='discord_log.log',
                            format = log_format,
                            filemode = "a",
                            level = logging.INFO)    
        logging.getLogger('discord').setLevel(logging.WARNING)
        self.log = logging.getLogger("DiscordBotLogger")
        self.log.info("Program started running")
        self.log.info("Listening to {channel} in {guild}".format(guild = self.guilds[self.guild_channel[0]].name, channel = self.guilds[self.guild_channel[0]].voice_channels[self.guild_channel[1]].name))
    
    # Main function to check for when people join the party.
    async def on_voice_state_update(self, member, before, after):
        if after.channel:
                if before.channel == None and not after.channel.name == 'afk' and not member.bot:
                    await self.play_sound(after.channel, member)
        else:
            if not member.bot:
                print("{} left channel".format(member.name))
                self.log.info("{} left {} in {}".format(member.name, before.channel.name, before.channel.guild.name))
    
    def find_sound(self, name):
        with open("data.json", "r") as f:
            sounds = json.load(f)
        if name not in list(sounds.keys()) or not sounds[name]:
            out = None
        else:
            choice = random.randint(0, len(sounds[name]["intro"])-1 )
            out = sounds[name]["intro"][choice]
        return out
        
    async def play_sound(self, channel, member):
        if sys.platform == "darwin":
            execute = os.getcwd() + "//" + os.listdir()[0]
        else:
            execute = "ffmpeg"
        member_sound = self.find_sound(member.name)        
        if member_sound != None:
            sound = discord.FFmpegPCMAudio("sounds//" + member_sound, executable=execute)
            if self.user not in channel.members:
                voice = await channel.connect()
                self.log.info("{member} joined {channel} in {guild}, {sound} is playing".format(member = member.name, sound = member_sound, channel = channel.name, guild = channel.guild.name))
                voice.play(sound)
                
                while voice.is_playing():
                    time.sleep(0.2)
                await voice.disconnect()     
    
    async def on_message(self, msg):
        
        if msg.author == client.user:
            return
        
        if len(msg.attachments) >= 1 and msg.channel.type == discord.ChannelType.private:
            for i in msg.attachments:
                if i.content_type == "audio/mpeg":
                    with open(os.getcwd() + "/data.json", "r") as f:
                        data = json.load(f)
                    await i.save(os.getcwd() + "/sounds/{}".format(i.filename))
                    if msg.author.name in list(data.keys()):
                        data[msg.author.name]["intro"].append(i.filename)
                    else:
                        data.update({msg.author.name: {"intro": [i.filename]}})
                    with open("data.json", "w") as f:
                        json.dump(data, f, indent = 2)
                    await msg.author.dm_channel.send("{} was added to your sounds!".format(i.filename))
                    guilds = ", ".join(i.name for i in msg.author.mutual_guilds)
                    self.log.info("{member} in {guilds} added {sound} to to their sounds!"
                                  .format(member = msg.author, sound = i.filename, guilds = guilds))
                    
def load_token():
    with open("Secrets.txt", "r") as f:
        file = f.readlines()[0]
    return file

token = load_token()
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
client = Client(intents = intents)
client.run(token)