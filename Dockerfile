FROM ubuntu:20.04

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install nano

#Need to run "apt-get install -y ffmpeg" through CLI afterward due to user input being required
#Run sudo docker exec -it <my-container> bash and then apt-get install -y ffmpeg when in the terminal

RUN mkdir /home/schmuck
WORKDIR home/schmuck

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD ["HelloWorld.py"]
#CMD ["WalkUpBot.py"]
