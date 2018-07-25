from pyfiglet import Figlet
import sys

def exit(redis, style):
  exit_msg = Figlet(font='slant')
  print(exit_msg.renderText('Good Bye . . .'))
  sys.exit()