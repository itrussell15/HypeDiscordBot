#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 13:47:33 2021

@author: isaactrussell
"""


import discord, time, sys, os, json, random
from discord.ext import tasks


class Client(discord.Client):
    
    async def on_ready(self):
        self.members = []
        
        self.previous_members = self.get_channel_members()
        self.previous_size = self.check_party_size()
        # discord.opus.load_opus()
        self.my_background_task.start() 
        
    @tasks.loop(seconds=1) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.guilds[0].voice_channels[0]
        current_size = self.check_party_size()
        print("PARTY SIZE GREATER THAN BEFORE: {}".format(current_size > self.previous_size))
        if current_size > self.previous_size:
            members = self.get_channel_members()
            diff = list(set(members) - set(self.previous_members)) + list(set(self.previous_members) - set(members))
            await self.play_sound(channel, diff[0])
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
        choice = random.randint(0, len(sounds[name]["intro"])-1 )
        return sounds[name]["intro"][choice]
        
    async def play_sound(self, channel, member):
        # print(member.name)
        if sys.platform == "darwin":
            execute = os.getcwd() + "//" + os.listdir()[0]
        else:
            execute = "ffmpeg.exe"
        member_sound = "sounds//" + self.find_sound(member.name)
        sound = discord.FFmpegPCMAudio(member_sound, executable=execute)
        if self.user not in channel.members:
            voice = await channel.connect()
        print("Playing Sound")
        voice.play(sound)
        print("Finished Playing Sound")
        while voice.is_playing():
            time.sleep(0.2)
        await voice.disconnect()       
    
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