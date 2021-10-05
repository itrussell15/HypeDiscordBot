# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 22:10:11 2021

@author: Schmuck
"""

import os, json, datetime
import matplotlib.pyplot as plt
import pandas as pd

with open("activity.json", "r") as f:
    data = json.load(f)

data = data["Potato On Me"]
file_date = datetime.datetime.utcfromtimestamp(os.path.getmtime(os.getcwd() + "\\activity.json"))
df = pd.DataFrame.from_dict(data, orient = "index")
df["mins"] = df[0]/3600
df = df[df["mins"] > 0]
fig = df.plot(y = "mins", kind = "bar")
plt.suptitle("Time Spent in Discord Since {}".format(file_date.strftime('%Y-%m-%d %H:%M:%S')))
fig.set_xlabel("Username")
fig.set_ylabel("Time (hrs)")
plt.xticks(rotation = 0)
