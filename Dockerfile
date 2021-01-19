FROM ubuntu:latest 
# WORKDIR /app

RUN apt update -y
RUN apt upgrade -y

RUN apt install python3 python3-pip build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
COPY . /
# COPY sub .
RUN pip3 install praw prawcore python-dotenv 
CMD ["bash","run.sh"]