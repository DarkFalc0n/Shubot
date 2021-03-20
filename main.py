from prawcore.exceptions import RequestException, ServerError
import re
from Reddit import reddit
import time
import random
from utils import (
    SignalHandler,
    cakedayCheck,
    commentCheck,
    inboxCheck,
    replyToComment,
)
from quotes import (
    dandaCount,
    happyCakeday,
    randomQuote,
    shutupShubot,
    cancelInvite,
    pickRandom,
    randomQuote,
    fBomb,
)


signalHandler = SignalHandler()


def main():

    commentCheckTime = 0
    inboxCheckTime = 0
    me = reddit.user.me()

    for comment in reddit.subreddit("onlyhere").stream.comments():

        signalHandler.loopStart()

        if time.time() > inboxCheckTime:
            inboxCheck()
            inboxCheckTime = time.time() + 3600 * 12

        if time.time() > commentCheckTime:
            commentCheck()
            commentCheckTime = time.time() + 9000

        if comment.saved \
                or comment.author == me \
                or re.search("\bre+post\b", comment.body, re.I):
            continue

        if re.search(r"\bchup\b|\bshut\b|\bblock\b|\bstop\b", comment.body, re.I) \
                and comment.parent().author == me:
            print(f"Replying to '{comment.permalink}' with shutupShubot")
            replyToComment(comment, shutupShubot())

            reddit.redditor("DarkFalconXX").message(
                "Sent a Shutup Shubot", comment.permalink)
            inboxCheckTime = time.time() + 3600

        elif cakedayCheck(comment):
            print(f"Replying to '{comment.permalink}' with Cakeday")
            replyToComment(comment, happyCakeday())

        elif re.search(r"\bbalak\b", comment.body, re.I):
            if random.randint(0,3):
                comment.save()
                print(f"Ignored the '{comment.permalink}' balak trigger")
            else:
                print(f"Replying to {comment.permalink} with balak trigger")
                mesg= randomQuote("bbsquotes")
                replyToComment(comment, mesg)
                
        elif re.search(r"\bbbsquote\b",comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with random quote")
            replyToComment(comment, randomQuote("bbsquotes"))

        elif re.search(r"\bShubh\b|\bBeastBoyShubh\b",comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with cancelled invite")
            replyToComment(comment, cancelInvite())

        elif re.search(r"dandacount", comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with Danda count")
            replyToComment(comment, dandaCount(comment))
        
        elif re.search(r"fuck", comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with F-Bomb")
            replyToComment(comment, fBomb(comment))

        elif re.search(r"\bHello\b|\bHi\b|\bHey\b", comment.body, re.I) and re.search(r"\bShubot\b|\bu/IamShubot\b", comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with greetings")
            replyToComment(comment, randomQuote("greetings"))

        elif re.search(r"\bbot\b",comment.body, re.I) and re.search(r"\bgood\b|\bawesome\b|\bbadass\b|\bnice\b", comment.body, re.I) and comment.parent().author == me:
            print(f"Replying to '{comment.permalink}' with good bot reply")
            replyToComment(comment, randomQuote("goodbot"))

        elif re.search(r"\bbot\b",comment.body, re.I) and  re.search(r"\bbad\b", comment.body, re.I) and comment.parent().author == me:
            print(f"Replying to '{comment.permalink}' with bad bot reply")
            replyToComment(comment, randomQuote("notbot"))

        elif re.search(r"\bmikasa\b|\bmikasa's\b", comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with mikasa reply")
            replyToComment(comment, "Haaye kya ladki hai ye Mikasa (っ´ω`c)")
        
        elif re.search(r"\bthanks\b|\bthank", comment.body, re.I) and comment.parent().author == me:
            print(f"Replying to '{comment.permalink}' with thanks reply")
            replyToComment(comment, randomQuote("thanks"))

        elif re.search(r"\bno u\b", comment.body, re.I):
            if random.randint(0,3):
                print(f"Ignored {comment.permalink} with no u trigger")
                comment.save()
            else:
                print(f"Replying to {comment.permalink} with beizzati")
                replyToComment(comment, "Beizzati, lol") 
                  
        elif re.search(r"\bfreefire\b|\bfree fire\b", comment.body, re.I):
            if random.randint(0,2):
                print(f"Ignored {comment.permalink} with freefire trigger")
                comment.save()
            else:
                print(f"Replying to {comment.permalink} with freefire reply")
                replyToComment(comment,"Thak gaya hu vro, freefire spam ka reply dete dete....")

        signalHandler.loopEnd()

if __name__ == "__main__":
    print("Starting Shubot.....")
    while(True):
        try:
            main()
        # Network Issues
        except (RequestException, ServerError) as e:
            print(e)
            time.sleep(60)
        else:
            raise "Program Finished Abnormally"
            break
