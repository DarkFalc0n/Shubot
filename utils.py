import re
import os
import sys

from Reddit import reddit

cakedayRedditors = []


class SignalHandler():

    def __init__(self):
        import signal
        signal.signal(signal.SIGINT, self._signalHandler)
        signal.signal(signal.SIGTERM, self._signalHandler)
        self.exitCondition = False
        self.inLoop = False

    def _signalHandler(self, signal, frame):
        print(f"RECIEVED SIGNAL: {signal}, Bye")
        if not self.inLoop:
            sys.exit(0)
        else:
            self.exitCondition = True

    def loopEnd(self):
        self.inLoop = False

        if self.exitCondition:
            sys.exit(0)

    def loopStart(self):
        self.inLoop = True


def cakedayCheck(comment):
    createdUtc = comment.created_utc + 3600 * 24 * 365
    currentUtc = utcTime()
    if currentUtc - createdUtc < 3600 * 24:
        return True
    else:
        return False

    
def commentCheck():
    for comment in reddit.user.me().comments.new():

        # Get Already wished redditors btw runs
        if re.search(r"^Happy cakeday", comment.body):
            cakedayRedditors.append(comment.parent().author)

        # Delete bad comnents
        if comment.score < -4:
            parentId = comment.parent().permalink.replace(
                "reddit", "removeddit")
            comment.delete()
            reddit.redditor("DarkFalconXX").message(
                "Comment deleted",
                comment.body + '\n\n' + parentId)
            print("Deleted comment {parentId}")

def inboxCheck():
    for msg in reddit.inbox.messages():
        if msg.subject == "Block me":
            msg.reply("Okay done")
            print("User Blocked: " + msg.author.name)
            reddit.redditor("DarkFalconXX").message(
                "User Blocked", 'u/' + msg.author.name)
            msg.author.block()

def replyToComment(comment, replyTxt):

    replyComment = comment.reply(replyTxt)
    comment.save()
    print("\tSuccess: " + replyComment.id)

def utcTime():
    from datetime import datetime
    return datetime.utcnow().timestamp()

def getAge(timestamp):
    # timestamp in format YYYYMMDD
    from datetime import date
    d = int(timestamp)
    return (date.today() - date(d // 10000, d // 100 % 100, d % 100)).days
