# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 21:49:53 2021

@author: Schmuck
"""

import random, json, sys, os, time
import discord

def _find_sound(name):
        with open("data.json", "r") as f:
            sounds = json.load(f)
        if name not in list(sounds.keys()) or not sounds[name]:
            out = None
        else:
            choice = random.randint(0, len(sounds[name]["intro"])-1 )
            out = sounds[name]["intro"][choice]
        return out

async def play_sound(channel, member, bot, log):
        if sys.platform == "darwin":
            execute = os.getcwd() + "//" + os.listdir()[0]
        else:
            execute = "ffmpeg"
        member_sound = _find_sound(member.name)
        if member_sound != None:
            sound = discord.FFmpegPCMAudio("sounds//" + member_sound)
            if bot not in channel.members:
                voice = await channel.connect()
                log.info("{member} joined {channel} in {guild}, {sound} is playing".format(member = member.name, sound = member_sound, channel = channel.name, guild = channel.guild.name))
                voice.play(sound)

                while voice.is_playing():
                    time.sleep(0.2)
                await voice.disconnect()
