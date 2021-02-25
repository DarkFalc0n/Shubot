import random
from Reddit import reddit
from prawcore.exceptions import NotFound
import re
import os

def urlQuote(a):
    from urllib.parse import quote
    return quote(a, safe='')


def createMsgLink(to=None, subject=None, message=None):
    from requests import Request
    return Request(url="https://www.reddit.com/message/compose/", params={
        "to": to,
        "subject": subject,
        "message": message, }).prepare().url


def happyCakeday():
    return "Happy cakeday to you. Wanna hear a Shub exclusive quote? Here you go: \n\n&nbsp;\n\n" +\
        randomQuote("bbsquotes") + '\u200e'

rickRolls = None

def getRickRoll():
    global rickRolls
    if rickRolls is None:
        rickRolls = "https://youtu.be/dQw4w9WgXcQ"
    return rickrolls

def pickRandom(filename=None):
    f = open(f"sub\{filename}.txt")
    x=(f.read()).split("\n")
    return random.choices(x)

def randomQuote(quote=None):

    if random.randint(0, 50):
        msg = pickRandom(quote) 
    else:
        youtubeLink = getRickRoll()
        msg = pickRandom(quote) + '\n\n&nbsp;\n\n' +\
        f'[Quote Source](<{youtubeLink}>)'
    

    return msg

def dandaCount(sourceComment):
    if targetUserRegex := re.search(r'u/(\w+)', sourceComment.body, re.I):
        targetUsername = targetUserRegex.group(1)
        targetRedditor = reddit.redditor(targetUsername)
    else:
        targetRedditor = sourceComment.parent().author

    try:
        targetRedditor.id
    except NotFound:
        return f"I didn't find any u/{targetUsername}" 

    bcount = 0
    for comment in targetRedditor.comments.new(limit=None):
        if re.search(r'\bdanda\b', comment.body, re.I):
            bcount += 1

    dandaRank = f"\n Time for celebrations, honouring u/{targetUsername} with the title\n"
    if bcount > 50:
        dandaRank += "#Danda God"
    elif bcount > 12:
        dandaRank += "#Danda Legend"
    elif bcount > 5:
        dandaRank += "#Danda Master"
    elif bcount > 0:
        dandaRank += "#Danda Balak"
    else:
        dandaRank = " "

    return 'It seems like \n\n&nbsp;\n  '\
        f'\nu/{targetUsername} has said "Danda" a total of '\
        f'{bcount} times!' + dandaRank

def fBomb(sourceComment):
    bcount = sourceComment.body.count("fuck")   
    return "I have noticed that you've dropped " + f'{bcount} F-bomb(s) in your comment, \n #NOTED.'\
    
def shutupShubot():
    return r"It looks like I have annoyed you with my random quotes. I am sorry" +\
        r"\n^P.S. You can simply block me "\
        "to hide all my comments from you or to stop getting " \
        "replies from me."\

allQuotes = ["Default_quote#1","Default_quote#2","Default_quote#3"]

def getAllQuotes():
    if not allQuotes:
        quoteCreator()
    return allQuotes

def cancelInvite():
    return "Seriously? Shub with an H? Your shaadi invitation is cancelled."


