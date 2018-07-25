def display(redis, style):

  # define color for print out
  class bcolors:
    PURPLE = '\033[95m'
    CYAN = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

  # init variables
  type_list = ['chore', 'task']
  completed = {'chore': 0, 'task': 0}
  print('') # print new line
  for i in range(len(type_list)):
    print(
      bcolors.CYAN,
      '==== %s List ====' % type_list[i].capitalize(),
      bcolors.ENDC,
      sep=''
    )  
    # check if there is any data in list
    if (redis.llen(type_list[i]) < 1):
      print(
        bcolors.RED,
        u'\u2716',
        ' No %s in list.' % type_list[i],
        bcolors.ENDC + '\n',
        sep='')
      continue
    else:
      for j in range(redis.llen(type_list[i])):
        # get full string
        data_str = redis.lindex(type_list[i], j).decode('utf-8')
        # split name and mark from full string
        data_name, data_mark = data_str.split('|')
        if data_mark == '1': completed[type_list[i]] += 1
        color = bcolors.GREEN if data_mark == '1' else bcolors.PURPLE
        data_mark = u'\u2714' if data_mark == '1' else '-'
        print(color, data_mark, ' ', data_name, bcolors.ENDC, sep='')
    print(
      bcolors.YELLOW,
      '%s Completed : %d / %d' % (
        u'\u274a', completed[type_list[i]], redis.llen(type_list[i]),
      ),
      bcolors.ENDC + '\n',
      sep=''
    )

  # if there is at least one task or chore, print remark
  if redis.llen(type_list[0]) > 0 or redis.llen(type_list[1]) > 0:
    print(
      bcolors.CYAN + 'Remark' + bcolors.ENDC,
      bcolors.GREEN + '%s = Completed Task' % u'\u2714' + bcolors.ENDC,
      bcolors.PURPLE + '- = Incompleted Task' + bcolors.ENDC,
      bcolors.ENDC,
      sep='\n'
    )