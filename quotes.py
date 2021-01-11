import random
from Reddit import reddit
from prawcore.exceptions import NotFound
import re


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
    return "Happy cakeday! Here have a quote!  \n\n&nbsp;\n\n" +\
        randomQuote() + '\u200e'




# whoAmIs = None


# def getWhoAmI():
#     global whoAmIs
#     if whoAmIs is None:
#         wikiPg = reddit.subreddit("SaimanSaid").wiki["whoami"].content_md
#         whoAmIs = [a.strip() for a in wikiPg.splitlines() if a]
#     return random.choice(whoAmIs).strip()


rickRolls = None


def getRickRoll():
    global rickRolls
    if rickRolls is None:
        rickRolls = 
    return random.choice(rickRolls)


def randomQuote(quote=None):

    if quote is None:
        allQuotes = getAllQuotes()
        quote = random.choices(allQuotes, [a.weight for a in allQuotes])[0]

    if random.randint(0, 100):
        youtubeLink = quote.youtubeLink
    else:
        youtubeLink = getRickRoll()

    msg = quote.quoteText + '\n\n&nbsp;\n\n' +\
        f'[Quote Sauce](<{youtubeLink}> "A rick-roll for sure")' + \
        '\n***\n' + createFooter()

    return msg


# def createFooter():
#     me_ = getWhoAmI()
#     footer = me_

#     if not me_.startswith('$'):
#         footer = "I am " + footer
#     if not me_.endswith('$'):
#         footer = footer + " I reply to danda, Timothy or Saibot"
#     if not me_.endswith('$$'):
#         footer = footer + ' ^[Know&nbsp;more](https://redd.it/fvkvw9)'

#     footer = '^^' + footer.replace(' ', ' ^^')
#     return footer.replace('$', '')


def dandaCount(sourceComment):
    footer = "  \n\n***\n^^[Report error](<" + createMsgLink(
                "DarkFalconXX","Danda Count","DandaCount bot did not work as expected in reply to " +
                f"comment {sourceComment.permalink}") + \
            ">)<_>^^| [Suggest Danda titles](<" + createMsgLink(
                "DarkFalconXX",
                "Danda Titles Suggestion"
                "These are my suggestions:\n") +\

    footer = '  ' + footer.replace(' ', '&nbsp;').replace('<_>', ' ')

    if targetUserRegex := re.search(r'u/(\w+)', sourceComment.body, re.I):
        targetUsername = targetUserRegex.group(1)
        targetRedditor = reddit.redditor(targetUsername)
    else:
        targetRedditor = sourceComment.parent().author

    try:
        targetRedditor.id
    except NotFound:
        return f"I didn't find any u/{targetUsername}" + footer

    bcount = 0
    for comment in targetRedditor.comments.new(limit=None):
        if re.search(r'\bdanda\b', comment.body, re.I):
            bcount += 1

    dandaRank = "  \nHe has been awarded the title of "
    if bcount > 50:
        dandaRank += "Danda God"
    elif bcount > 12:
        dandaRank += "Danda Legend"
    elif bcount > 5:
        dandaRank += "Danda Master"
    elif bcount > 0:
        dandaRank += "Danda Balak"
    else:
        dandaRank = ''

    return 'Thankyou for your request comrade  \n\n&nbsp;\n  '\
        f'\nu/{targetUsername} has said "Danda" a total of '\
        f'{bcount} times!' + dandaRank + footer


def shutupShubot():
    return "It looks like I have annoyed you with my random quotes. I am sorry" +\
        "^P.S. You can simply [block&nbsp;me](https://redd.it/gh42zl) "\
        "to hide all my comments from you or to stop getting " \
        "replies from me."\

allQuotes = []

def getAllQuotes():
    if not allQuotes:
        quoteCreator()
    return allQuotes


# class Quote():
#     def __init__(self, quoteText, youtubeLink, weight, handFiltered):
#         self.quoteText = quoteText
#         self.youtubeLink = youtubeLink
#         self.weight = weight
#         self.handFiltered = handFiltered

# ``
# def quoteCreator():
#     import os
#     from utils import getAge

#     subFiles = [
#         ("subs/", a) for a in os.listdir("subs/")] + [
#         ("subs/done/", a) for a in os.listdir("subs/done/")]
#     subFiles.remove(('subs/', 'done'))

#     oldestSubAge = getAge(min(int(a[:8]) for fldr, a in subFiles)) * 1.1

#     for fldr, subFile in subFiles:

#         with open(fldr + subFile, 'r') as f:
#             quotes = f.read().split('\n\n')

#         videoId = subFile[8:]
#         subAge = getAge(subFile[:8])

#         for quote in quotes:
#             if quoteTime := re.match(r"(\d\d):(\d\d):(\d\d)", quote):
#                 hh, mm, ss = quoteTime.groups()
#             else:
#                 print(f"Time stamp not found in {quote=} \nof {subFile=}")
#                 continue
#             youtubeLink = f"https://youtu.be/{videoId}/?t={hh}h{mm}m{ss}s"

#             # Removes the time stamp
#             quoteText = re.sub("^.*\n", '', quote)
#             # Removes anything inside [] or ()
#             quoteText = re.sub(r"\[.*\]", '', quoteText)
#             quoteText = re.sub(r"\(.*\)", '', quoteText)
#             quoteText = re.sub("  ", ' ', quoteText)
#             # Remove starting -
#             quoteText = re.sub(r"^\s*-\s*", '', quoteText)

#             # sometimes two quotes are not seperated
#             if re.search(r'(\d\d):(\d\d):(\d\d)', quoteText):
#                 print(f"Invalid format of {quote=} in {subFile=}")
#                 continue

#             # Formatting
#             quoteText = quoteText.strip()
#             quoteText = re.sub(
#                 r"^\W*(and|but|so|also|that|i mean)\W*|" +
#                 r"([^a-zA-Z\?\.\!]*and|but|so|beacuse|also)\W*$",
#                 '',
#                 quoteText,
#                 flags=re.I).strip()
#             quoteText = quoteText.capitalize()

#             # Filters
#             if len(re.sub(
#                     r'\W|saiman|timothy|a+ditya', '',
#                     quoteText, flags=re.I)) < 3:
#                 continue
#             if re.search('video|^welcome', quoteText, re.I):
#                 # print(f"Banned words in '{quoteText}' of {subFile}")
#                 continue

#             handFiltered = fldr == 'subs/done/'
#             weight = (1 - subAge/oldestSubAge) ** 2

#             if re.search('t-series|pewds|pewdiepie', quoteText, re.I):
#                 weight = weight/4
#             if handFiltered:
#                 weight = weight * 1.2

#             quote = Quote(quoteText, youtubeLink, weight, handFiltered)
#             allQuotes.append(quote)
def cancelInvite()
    return "Seriously? Shub with an H? Your shaadi invitation is cancelled."