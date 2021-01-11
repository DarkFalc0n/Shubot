from prawcore.exceptions import RequestException, ServerError
import re
from Reddit import reddit
import time
from utils import (
    SignalHandler,
    cakedayCheck,
    commentCheck,
    inboxCheck,
    replyToComment,
    updateKnowmore,
)
from quotes import (
    dandaCount,
    happyCakeday,
    randomQuote,
    shutupShubot,
    cancelInvite,
)


signalHandler = SignalHandler()


def main():

    # downloadNewSubtitles()
    updateKnowmore()

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
            commentCheckTime = time.time() + 1800

        if comment.saved \
                or comment.author == me \
                or re.search(r"\bre+post\b", comment.body, re.I):
            continue

        if re.search(r"chup|shut ?up|block|stop", comment.body, re.I) \
                and comment.parent().author == me:
            print(f"Replying to '{comment.permalink}' with shutupShubot")
            replyToComment(comment, shutupShubot())

            reddit.redditor("DarkFalconXX").message(
                "Sent a Shutup Shubot", comment.permalink)
            inboxCheckTime = time.time() + 3600

        elif cakedayCheck(comment):
            print(f"Replying to '{comment.permalink}' with Cakeday")
            replyToComment(comment, happyCakeday())

        elif re.search(r"\bShubham\b|\bbeastboyshub?-?(Shub| ?bot)\b|\bShubot\b|\bdanda\b|\bchippu\b",comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with random quote")
            replyToComment(comment, randomQuote())

        elif re.search(r"\bShubh\b",comment.body, re.I)
            print(f"Replying to '{comment.permalink}' with cancelled invite")
            replyToComment(comment, cancelInvite())

        elif re.search(r"dandacount", comment.body, re.I,comment.body, re.I):
            print(f"Replying to '{comment.permalink}' with Danda count")
            replyToComment(comment, dandaCount())

        signalHandler.loopEnd()


if __name__ == "__main__":
    print("Starting the bot")
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
