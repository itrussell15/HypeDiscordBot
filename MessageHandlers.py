# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 00:08:46 2021

@author: Schmuck
"""

import os
from FileHandlers import load_data, save_data, remove_sound_file

async def message_has_attachments(attachments, user):
    for i in attachments:
        if i.content_type == "audio/mpeg":
            data = load_data()
            await i.save(os.getcwd() + "/sounds/{}".format(i.filename))
            if user in list(data.keys()):
                data[user]["intro"].append(i.filename)
            else:
                data.update({user: {"intro": [i.filename]}}) 
    save_data(data)

def list_sounds(user):
    data = load_data()
    if data[user]["intro"]:
        return data[user]["intro"]
    else:
        return None

def delete_sound(user, selection):
    split_content = selection.split(" ")
    selection = split_content[-1]
    
    if len(split_content) == 2 and selection.isdigit():
        data = load_data()
        sounds = data[user]["intro"]
        if sounds:
            selection = int(selection)
            if selection >= 1 and selection <= len(sounds) + 1:
                remove_sound_file(sounds[selection - 1])
                sounds.pop(selection - 1)
                data[user]["intro"] = sounds
                save_data(data)
                return list_sounds(user)
            else:
                print("Invalid Input")
    else:
        print("Invalid Input")
        
def format_message(sounds):
    if sounds:
        out = "**Your sounds are:**\n" + "\n".join(["{}- {}".format(n + 1, i) for n, i in enumerate(sounds)])
    else:
        out = "**You have no sounds!**"
    return out