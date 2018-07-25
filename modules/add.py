from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import (
  style_from_dict, Token, prompt, print_json,
  default_style, Separator, Validator, ValidationError
)

def add(redis, style):

  class isDuplicated(Validator):
    def validate(self, document):
      for i in range(redis.llen(answers['key']['type'])):
        data_str = redis.lindex(answers['key']['type'], i).decode('utf-8')
        data_name, data_mark = data_str.split('|')
        if data_name == document.text:
          raise ValidationError(
            message='This %s has already been added.' % answers['key']['type'],
            cursor_position=len(document.text) # Move cursor to end
          )

  # init variables
  questions = {}
  answers = {}

  while True:
    # chore or task?
    questions['key'] = [
      {
        'type': 'list',
        'name': 'type',
        'message': 'What do you want to add?',
        'choices': [
          { 'name': 'Chore(s)' , 'value': 'chore' },
          { 'name': 'Task(s)' , 'value': 'task' },
        ]
      },
    ]
    answers['key'] = prompt(questions['key'], style=style)

    while True:
      # enter value
      questions['data'] = [
        {
          'type': 'input',
          'name': 'value',
          'message': str(redis.llen(answers['key']['type']) + 1) + ' :',
          'validate': isDuplicated,
        },
      ]
      answers['data'] = prompt(questions['data'], style=style)

      # stop entering if input is blank
      if(answers['data']['value'] == ''): break
      else:
        # store data to redis server
        # mark 0 as an incomplete task or chore and | as spliter
        redis.rpush(answers['key']['type'], answers['data']['value'] + '|0')

    questions['action'] = [
      {
        'type': 'confirm',
        'name': 'return',
        'message': 'Return to main menu?',
      },
    ]
    answers['action'] = prompt(questions['action'], style=style)
    # return to main menu if answer is 'y'
    if(answers['action']['return']): break