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
    
    def set_up_logging(self):
        # self.log = logging.getLogger('discord')
        # self.log.setLevel(self.log.DEBUG)
        log_format = '%(asctime)s %(message)s'
        logging.basicConfig(filename='discord_log.log',
                            format = log_format,
                            filemode = "a",
                            level = logging.INFO)    

        logging.info("Listening to {channel} in {guild}".format(guild = self.guilds[1].name, channel = self.guilds[1].voice_channels[0].name))
    
    @tasks.loop(seconds=1) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.guilds[1].voice_channels[0]
        # print(channel)
        current_size = self.check_party_size()
        print("PARTY SIZE GREATER THAN BEFORE: {}".format(current_size > self.previous_size))
        if current_size > self.previous_size:
            members = self.get_channel_members()
            diff = list(set(members) - set(self.previous_members)) + list(set(self.previous_members) - set(members))
            [await self.play_sound(channel, person) for person in diff]
        self.previous_members = self.get_channel_members()
        self.previous_size = len(self.previous_members)             
    
    def get_channel_members(self):
        channel = self.guilds[1].voice_channels[0]
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
            execute = "ffmpeg.exe"
        member_sound = self.find_sound(member.name)        
        if member_sound != None:
            sound = discord.FFmpegPCMAudio("sounds//" + member_sound, executable=execute)
            if self.user not in channel.members:
                voice = await channel.connect()
                logging.info("{member} joined the party, {sound} is playing".format(member = member.name, sound = member_sound))
                print("HERE")
                voice.play(sound)
                
                while voice.is_playing():
                    time.sleep(0.2)
                await voice.disconnect()     
                
    class Logging:
        
        def __init__(self, path = "log.txt"):
            self.path = path
            if path not in os.listdir(os.getcwd()):
                self.__create_file()
            # self.log = self.write_to_log(path)
        
        def formatted_time(self):
            format_time = lambda x: x.strftime("%H:%M:%S %m-%d-%Y")
            return format_time(datetime.datetime.now())
        
        #Create file method, to be used only if needed.
        def __create_file(self):
            with open(self.path, "w") as f:
                f.close()   
            self.write_to_log("Beginning of Log")
        
        def write_to_log(self, message, to_print = False):
            if self.path not in os.listdir(os.getcwd()):
                self.__create_file()
                
            if to_print:
                print(message)
                
            with open(os.getcwd() + "\{}".format(self.path), "a") as f:
                f.write("\n{date} --> {message}".format(date = self.formatted_time(), message = message))
                f.close() 
            
    
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