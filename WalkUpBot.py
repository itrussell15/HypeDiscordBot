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
        self.members = []
        print("RUNNING")
        self.set_up_logging()
        self.previous_members = self.get_channel_members()
        self.previous_size = self.check_party_size()
        self.my_background_task.start()
        self.guild_num = 0
    
    def set_up_logging(self):
        # self.log = logging.getLogger('discord')
        # self.log.setLevel(self.log.DEBUG)
        log_format = '%(asctime)s %(message)s'
        logging.basicConfig(filename='discord_log.log',
                            format = log_format,
                            filemode = "a",
                            level = logging.INFO)    
        logging.getLogger('discord').setLevel(logging.WARNING)
        self.log = logging.getLogger("DiscordBotLogger")
        self.log.info("Program started running")
        self.log.info("Listening to {channel} in {guild}".format(guild = self.guilds[0].name, channel = self.guilds[0].voice_channels[0].name))
    
    @tasks.loop(seconds=1) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.guilds[0].voice_channels[0]
        # print(channel)
        current_size = self.check_party_size()
        # print("PARTY SIZE GREATER THAN BEFORE: {}".format(current_size > self.previous_size))
        if current_size > self.previous_size:
            members = self.get_channel_members()
            diff = list(set(members) - set(self.previous_members)) + list(set(self.previous_members) - set(members))
            self.log.info("{} joined the voice chat".format(" ".join([i.name for i in diff])))
            [await self.play_sound(channel, person) for person in diff]
        self.previous_members = self.get_channel_members()
        self.previous_size = len(self.previous_members)             
    
    def get_channel_members(self):
        channel = self.guilds[0].voice_channels[0]
        return [i for i in channel.members if not i.bot]
        
    def check_party_size(self):
        return len(self.get_channel_members())
    
    def find_sound(self, name):
        with open("data.json", "r") as f:
            sounds = json.load(f)
        if name not in list(sounds.keys()):
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
                self.log.info("{member} joined the party, {sound} is playing".format(member = member.name, sound = member_sound))
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
                    with open(os.getcwd() + "\\data.json", "r") as f:
                        data = json.load(f)
                    await i.save(os.getcwd() + "\\sounds\\{}".format(i.filename))
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