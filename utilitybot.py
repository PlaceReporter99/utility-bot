import html
import re
import secrets
import subprocess
import sys
import time
from urllib.request import urlopen

import sechat
from deep_translator import GoogleTranslator
from sechat.events import Events
from transformers import Conversation, pipeline

# import streamlit as st

c = Conversation()
h = pipeline("conversational", pad_token_id=0)
last_msg = ""

main_ = __name__ == "__main__"

if main_:
    bot = sechat.Bot()
    bot.login(sys.argv[1], sys.argv[2])
    r = bot.joinRoom(1)
    t = bot.joinRoom(147676)
    priv = bot.joinRoom(147571)
    sb2 = bot.joinRoom(147516)
    baso = bot.joinRoom(146039)
    den = bot.joinRoom(148152)
    t4d = bot.joinRoom(148981)

    def ai(text):
        global c, h, last_msg  # skipcq: PYL-W0602
        c.add_user_input(html.unescape(text))
        response = h(c).generated_responses[-1]
        if response == last_msg:
            c = Conversation()
            c.add_user_input(html.unescape(text))
            last_msg = h(c).generated_responses[-1]
        else:
            last_msg = response
        return last_msg


def onn(room):
    room.on(Events.MESSAGE, roomer(room))


def indent(text):
    return "\n".join("    " + x for x in text.split("\n"))


def remove_lead_space(text):
    it = iter(text)
    # skipcq: PTC-W0047
    while (result := next(it)) == " ":  # skipcq: PTC-W0063
        pass
    return result + "".join(it)


def remove_space(text):
    lead_space_x = remove_lead_space(text)
    return remove_lead_space(lead_space_x[::-1])[::-1]


def remote(event):
    if event.content[:10] == "remotesay ":
        r.send(event.user_name + ": " + html.unescape(event.content[10:]))
        g.send(g.buildReply(event.message_id, "Message sent."))


def roomer(r):

    def msg(event):
        if (result := re.match(
                r"🐟 <i>(.*)'s line quivers\.<\/i>",
                html.unescape(event.content),
                re.UNICODE,
        )) and event.user_id == 375672:
            if result.group(1) == "Utility Bot":
                r.send("/fish")
                r.send(
                    "Stack Exchange does not let me send 2 messages with the same content in quick sucsession, which is why I have to send this message. :("
                )
                r.send("/fish")
            else:
                with open("optout.txt") as f:
                    if result.group(1) not in f.read().split("\n"):
                        r.send(
                            f"@{result.group(1).replace(' ', '')} your fish is ready!"
                        )
        elif event.content[:5] == "echo ":
            if event.user_id == 540406 or event.content[5:10] != "/fish":
                r.send(html.unescape(event.content[5:]))
            else:
                r.send(
                    r.buildReply(event.message_id, "Sorry, I cannot do that."))
        elif event.content[:8] == "echochr ":
            r.send(html.unescape(chr(int(event.content[8:]))))
        elif event.content[:5] == "calc ":
            allowed = {
                "+",
                "-",
                "*",
                "/",
                "=",
                "!",
                "<",
                ">",
                "&",
                "|",
                "^",
                "~",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "0",
                " ",
                "(",
                ")",
                ".",
                "%",
            }
            string = html.unescape(event.content[5:])
            val = set(string)
            result = []
            if val.issubset(allowed):
                try:
                    r.send(
                        r.buildReply(
                            event.message_id,
                            "The answer is\n" + subprocess.check_output([
                                "timeout",
                                "-s",
                                "SIGKILL",
                                "10s",
                                "python3",
                                "calculate.py",
                                string,
                            ]).decode("utf-8").replace("\n", ""),
                        ) + ".", )
                except subprocess.CalledProcessError:
                    r.send(
                        r.buildReply(
                            event.message_id,
                            "Sorry, the calculation took longer than 10 seconds.",
                        ))
            else:
                r.send(
                    r.buildReply(
                        event.message_id,
                        "Sorry, only characters in the set " +
                        str(sorted(allowed)) +
                        " are allowed due to security reasons.",
                    ))
        elif event.content[:5] == "ping ":
            r.send("@" + re.sub(" ", "", html.unescape(event.content[5:])))
        elif event.content[:10] == "remotesay ":
            com = html.unescape(event.content[10:])
            li = com.partition(",")
            if li[1] == "":
                li = ("147516", ",", li[0])

            if li[0] == "147571":
                r.send(
                    r.buildReply(event.message_id,
                                 "Sorry, I'm afraid I can't do that."))
            else:
                global g  # skipcq: PYL-W0601
                g = bot.joinRoom(int(li[0]))
                g.send(event.user_name + ": " + li[2])
                g.on(Events.MESSAGE, remote)
                r.send(r.buildReply(event.message_id, "Message sent."))
        elif event.content == "getsource":
            r.send(
                r.buildReply(
                    event.message_id,
                    "https://github.com/PlaceReporter99/utility-bot/blob/main/utilitybot.py",
                ))
        elif event.content[:6] == "getcmd":
            commands = {
                "echo <message>":
                "                      Sends the message given to it.",
                "echochr <character number>":
                "          Sends the unicode character with the codepoint of the number given to it. Must be in base 10.",
                "calc <python expression>":
                "            Sends the answer to the given Python expression. Uses a restricted character set due to security reasons. Times out after 10 seconds.",
                "ping <user name>":
                "                    Pings the person with the username that was passed to it.",
                "remotesay <room>, <message>":
                "         Sends a message in the specified room ID. If no room ID is given, the room defaults to Sandbox 2.",
                "getsource":
                "                           Sends a link to the source code.",
                "getcmd <command>":
                "                    Sends the command description. If no command is given, it lists the commands with their descriptions instead.",
                "emptystring":
                "                         Sends a picture of an empty string.",
                "help":
                "                                Shows some information.",
                "op / status":
                "                         Replies with a random message from statuses.txt. Exists to quickly check whether the bot is running.",
                "webscrape <URL>":
                "                     Sends the HTML content of the specified URL.",
                "random <quantity>, <start>, <end>":
                "   Sends the specified number of random numbers in the inclusive range (using secrets.choice). 1 argument uses the range 0 to 255, and 2 arguments uses the range 0 to <end>. Maximum argument value is 1000 for <quantity> and 9 * 10 ** 18 for all other arguments.",
                "translate <text> | <to> | <from>":
                "    Translates <text> from the language code in <from> (automatically detects language if none is given) to the language code in <to> (translates to English if none is given). See https://utility-bot.streamlit.app/Supported_translation_languages for supported languages and their language codes.",
                "fishinv":
                "                             Get's the bot's fishing inventory, with the fishing game being run by OakBot.",
                "ai <prompt>":
                "                         Talk to an AI. It's just one big conversation shared across every room the bot operates in.",
            }
            if len(event.content) > 6:
                try:
                    r.send(
                        r.buildReply(
                            event.message_id,
                            "`" + (result := [
                                x for x in commands if re.match(
                                    event.content.partition(" ")[2], x)
                            ][0]) + "`: " + commands[result],
                        ))
                except IndexError:
                    r.send(
                        r.buildReply(event.message_id,
                                     "Command does not exist."))
            else:
                r.send(
                    indent(
                        f"@{event.user_name.replace(' ', '')}\nHere are the available commands for this bot and their structures:\n\n"
                        + ("\n".join(f"{chr(8226)} {x}: {commands[x]}"
                                     for x in commands)), ))
        elif event.content == "emptystring":
            r.send(
                r.buildReply(event.message_id,
                             "https://i.stack.imgur.com/Fh2Cq.png"))
        elif event.content == "help":
            r.send(
                r.buildReply(
                    event.message_id,
                    'Type in "getcmd" (without the quotes) for a list of commands and their descriptions.\n\nRepo: https://github.com/PlaceReporter99/utility-bot\nWebsite: https://utility-bot.streamlit.app/',
                ))
        elif event.content in ("op", "status"):
            with open("status.txt") as f, open(__file__) as g:
                r.send(
                    r.buildReply(
                        event.message_id,
                        secrets.choice(f.read().split("\n")).replace(
                            "[prog_rand]",
                            secrets.choice(g.read().split("\n"))),
                    ))
        elif event.content[:10] == "webscrape ":
            try:
                r.send(
                    indent(
                        f"@{event.user_name.replace(' ', '')}" +
                        "\nHere is the source code of the HTML webpage:\n\n" +
                        urlopen(event.content[10:]).read().decode("utf-8")))
            except Exception as err:  # skipcq: PYL-W0703
                r.send(r.buildReply(event.message_id, f"`{repr(err)}`"))

        elif event.content[:7] == "random ":
            args = [int(x) for x in event.content[7:].split(",")]
            if len(args) == 1:
                args.append(0)
                args.append(255)
            elif len(args) == 2:
                args.insert(1, 0)
            if args[0] > 1000 or any(x > 9 * 10**18 for x in args):
                r.send(
                    r.buildReply(
                        event.message_id,
                        "Sorry, that will probably take me too long."))
            else:
                numbers = [
                    secrets.choice(range(args[1], args[2] + 1))
                    for x in range(args[0])
                ]
                r.send(
                    r.buildReply(event.message_id,
                                 f"Here are your random numbers:\n{numbers}"))
        elif event.content[:10] == "translate ":
            arguments = [
                remove_space(x)
                for x in html.unescape(event.content[10:]).split("|")
            ]
            while len(arguments) < 3:
                arguments.append("auto")
            r.send(
                r.buildReply(
                    event.message_id,
                    GoogleTranslator(**dict(
                        zip(
                            ["target", "source"],
                            [
                                a if (a := arguments[1]) != "auto" else "en",
                                arguments[2],
                            ],
                        ))).translate(arguments[0]),
                ))
        elif event.content == "fishinv":
            r.send("/fish inv")
        elif event.content[:3] == "ai ":
            r.send(r.buildReply(event.message_id, ai(event.content[3:])))

    return msg


if main_:
    for room in [r, t, priv, sb2, baso, den, t4d]:
        onn(room)

    try:
        counter = 0
        print("Startup Successful.")
        t.send("Bot has started.")
        priv.send("Bot has started.")
        sb2.send("Bot has started. No freezing!")
        den.send("Bot has started. Hello everyone!")
        while True:
            print(f"Bot is running. Seconds since start: {counter}")
            # st.write(f"Bot is running. Seconds since start: {counter}")
            time.sleep(1)
            counter += 1
    finally:
        r.send("Bot has stopped for updates.")
        bot.leaveAllRooms()
