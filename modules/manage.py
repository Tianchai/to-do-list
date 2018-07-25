from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import (
  style_from_dict, Token, prompt, print_json,
  default_style, Separator
)

def rreplace(s, old, new):
  return (s[::-1].replace(old[::-1],new[::-1], 1))[::-1]

def manage(redis, style):
  
  # Define a style for PyInquirer
  style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
  })

  # init variables
  choices = {}
  questions = [
    {
      'type': 'list',
      'name': 'action',
      'message': 'What do you want to do?',
      'choices': [
        { 'name': 'Check finished' , 'value': 'check' },
        { 'name': 'Remove' , 'value': 'remove' },
      ]
    },
  ]
  type_list = ['chore', 'task']
  action_list = ['check', 'remove']
  for type in type_list:
    choices[type] = {}
    for action in action_list:
      choices[type][action] = []

  # add list to choices for questions
  for i in range(len(type_list)):
    if redis.llen(type_list[i]) > 0:
      for j in range(len(action_list)):
        choices[type_list[i]][action_list[j]].append(
          Separator('==== %s List ====' % type_list[i].capitalize())
        )
      for j in range(redis.llen(type_list[i])):
        # get full string
        data_str = redis.lindex(type_list[i], j).decode('utf-8')
        # split name and mark from full string
        data_name, data_mark = data_str.split('|')
        # convert mark to boolean
        data_mark = True if data_mark == '1' else False
        choices[type_list[i]]['check'].append({
          'name': data_name,
          'checked': data_mark,
        })
        choices[type_list[i]]['remove'].append({
          'name': data_name,
        })
      questions.append({
        'type': 'checkbox',
        # 'qmark': '�',
        'message': 'Select finished %s(s)' % type_list[i],
        'name': 'finished_%s' % type_list[i],
        'choices': choices[type_list[i]]['check'],
        'when': lambda answers: answers['action'] == 'check'
      })
      questions.append({
        'type': 'checkbox',
        # 'qmark': '�',
        'message': 'Select %s(s) you want to remove' % type_list[i],
        'name': 'remove_%s' % type_list[i],
        'choices': choices[type_list[i]]['remove'],
        'when': lambda answers: answers['action'] == 'remove'
      })
    else:
      print('- No %s has been added.' % type_list[i])

  if redis.llen(type_list[0]) < 1 and redis.llen(type_list[1]) < 1:
    return

  answers = prompt(questions, style=style)

  if answers['action'] == 'check':
    for i in range(len(type_list)):
      for j in range(redis.llen(type_list[i])):
        # get full string
        data_str = redis.lindex(type_list[i], j).decode('utf-8')
        # split name and mark from full string
        data_name, data_mark = data_str.split('|')
        if data_name in answers['finished_%s' % type_list[i]]:
          data_str = rreplace(data_str, '|0', '|1')
        else:
          data_str = rreplace(data_str, '|1', '|0')
        redis.lset(type_list[i], j, data_str)
    print('Manage finished to-do thing(s) successful!!')
  elif answers['action'] == 'remove':
    for i in range(len(type_list)):
      j = 0
      while j < redis.llen(type_list[i]):
        # handle error index out of range after removing at least one
        if (redis.lindex(type_list[i], j) == None): continue
        # get full string
        data_str = redis.lindex(type_list[i], j).decode('utf-8')
        # split name and mark from full string
        data_name, data_mark = data_str.split('|')
        if data_name in answers['remove_%s' % type_list[i]]:
          redis.lrem(type_list[i], data_str)
        else:
          j += 1
    print('Remove to-do thing(s) successful!!')