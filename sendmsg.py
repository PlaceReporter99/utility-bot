import sechat
import sys

EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]
EVENT_NAME = sys.argv[3]
EVENT_DATA = sys.argv[4]

bot = sechat.Bot()
bot.login(EMAIL, PASSWORD)
r = bot.joinRoom(147676)


def indent(text):
    return "\n".join("    " + x for x in text.split("\n"))

r.send(indent(f'Event "{EVENT_NAME}" was triggered by user {''}'))
