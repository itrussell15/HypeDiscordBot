# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 22:00:27 2021

@author: Schmuck
"""

import json, os

def save_data(data):
    with open("data.json", "w") as f:
        out = json.dump(data, f, indent = 2)
    return out

def load_data():
    with open(os.getcwd() + "/data.json") as f:
        data = json.load(f)
    return data

def remove_sound_file(name):
    for i in os.listdir(os.getcwd() + "/sounds"):
        if i == name:
            os.remove(os.getcwd() + "/sounds/{}".format(name))

        