from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import (
  style_from_dict, Token, prompt, print_json,
  default_style, Separator
)
from pyfiglet import Figlet
from modules.add import add
from modules.display import display
from modules.manage import manage
from modules.exit import exit
import sys
import redis
import configparser

def setupRedis():
  # get config from file config.ini
  configs = configparser.ConfigParser()
  configs.read('configs.ini')

  try:
    redisClient = redis.Redis(
      host=configs.get('redis', 'host'),
      port=configs.get('redis', 'port'),
      db=configs.get('redis', 'db'),
      password=configs.get('redis', 'pass'),
    )
  except Exception:
    pprint('Cannot connect to Redis Server : ' + str(Exception))
    sys.exit()

  return redisClient

def run(redis):
  # Print a welcome message
  welcome_msg = Figlet(font='slant')
  print(welcome_msg.renderText('To-Do List App'))

  # Define a style for PyInquirer
  style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
  })

  while True:
    # Get choice from user
    question = [
      {
        'type': 'list',
        'name': 'choice',
        'message': 'Select menu ',
        'choices': [
          { 'name': 'Add chore(s) or task(s)', 'value': 1 },
          { 'name': 'Display to-do list', 'value': 2 },
          { 'name': 'Manage to-do list', 'value': 3 },
          { 'name': 'Exit application', 'value': 4 },
        ]
      },
    ]
    answer = prompt(question, style=style)

    # Run menu from choice
    switcher = {
      1: add,
      2: display,
      3: manage,
      4: exit,
    }[answer['choice']]

    switcher(redis, style)

if __name__ == '__main__':
  redisClient = setupRedis()
  run(redisClient)