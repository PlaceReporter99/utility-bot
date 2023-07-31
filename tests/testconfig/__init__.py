import sechat
import sys

EMAIL = sys.argv[1]
PASSWORD = sys.argv[2]
TESTING_ROOM = 147571

def meta(a, b, c):
  """
  Metaclass for the Tests class, so that testing is as easy as doing Tests().
  """
  def func():
    for x in list(c.values())[3:]:
      x()
  
  return func

class Tests(metaclass=meta):
  """
  Testing functions go in this class.
  Every function must take no arguments, not even the self argument.
  """
  def test_message_send():
    bot = sechat.Bot()
    bot.login(EMAIL, PASSWORD)
    p = bot.joinRoom(TESTING_ROOM)
    MSG = "The bot is undergoing a test. Please do not send any messages until said otherwise."
    p.send(MSG)
    message = r.getRecentMessages()[-1]
    p.send("You may now send messages.")
    bot.leaveRoom(TESTING_ROOM)
    del p
    assert (message['content'] == MSG and message['user_id'] == 576644)