FROM ubuntu:20.04

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
#Need to run "apt-get install -y ffmpeg" and run through prompts for voice to run properly

WORKDIR E:\Coding\Projects\DiscordBot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD ["WalkUpBot.py"]
