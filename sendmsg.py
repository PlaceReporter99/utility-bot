import re
import sys

import sechat

EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]
EVENT_NAME = sys.argv[3]
EVENT_USER = sys.argv[4]

cleaned = re.sub(r"\[.*\]", "", EVENT_USER)

bot = sechat.Bot()
bot.login(EMAIL, PASSWORD)
r = bot.joinRoom(147676)


def indent(text):
    return "\n".join("    " + x for x in text.split("\n"))


r.send(
    f'Event "{EVENT_NAME}" was triggered by {f"[{cleaned}](https://github.com/{cleaned})"}.'
)
