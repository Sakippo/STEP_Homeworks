#! /usr/bin/python3

'''
括弧に対応した計算機の実装方針
・式を逆ポーランド記法に変換
・スタックを用いて演算
'''

def read_number(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


#各記号に演算の優先度を割り当てる
#numberの数字が大きい方が高優先度
def read_plus(line, index):
  token = {'type': 'PLUS', 'number': 1}
  return token, index + 1


def read_minus(line, index):
  token = {'type': 'MINUS', 'number': 1}
  return token, index + 1


def read_multiply(line, index):
  token = {'type': 'MULTIPLY', 'number': 2}
  return token, index + 1  


def read_divide(line, index):
  token = {'type': 'DIVIDE', 'number': 2}
  return token, index + 1  

def read_left(line, index):
  token = {'type': 'LEFT', 'number': 0}
  return token, index + 1  

def read_right(line, index):
  token = {'type': 'RIGHT', 'number': 0}
  return token, index + 1  

def convert_to_rpn(tokens):
    #後置記法に変換
    rpn = []
    stack = []
    index = 0
    while index < len(tokens):
      if tokens[index]['type'] == 'NUMBER':
        #数字は後置記法リストに追加
        rpn.append(tokens[index])
      else:
        if stack:
          if tokens[index]['type'] == 'RIGHT':
            #右括弧が来たときは左括弧までstackをpop & リストに追加
            #右括弧はstackに追加しない
            for i in range(len(stack)):
              add = stack.pop()
              if add['type'] != 'LEFT':
                rpn.append(add)
              else:
                break
          elif tokens[index]['type'] == 'LEFT':
            #左括弧が来たときはstackにpush
            stack.append(tokens[index])
          elif stack[-1]['number'] >= tokens[index]['number']:
            #stackの一番上に積まれた記号より優先度が低いor同じ記号がきたら、(左括弧まで)stackをpop & リストに追加
            for i in range(len(stack)):
              add = stack.pop()
              if add['type'] != 'LEFT':
                rpn.append(add)
              else:
                break
            stack.append(tokens[index])
          else:
            #stackの一番上に積まれた記号より優先度が高い記号がきたら、stackにpush
            stack.append(tokens[index])
        else:
          #stackが空の時はstackにpush
          stack.append(tokens[index])

      index += 1
    
    #最後にstackを空にする
    for i in range(len(stack)):
      rpn.append(stack.pop())

    return rpn

def tokenize(line):
  #与えられた文字列を数字と記号に分解したtokensリストを作成
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index] == '*':
      (token, index) = read_multiply(line, index)
    elif line[index] == '/':
      (token, index) = read_divide(line, index)
    elif line[index] == '(':
      (token, index) = read_left(line, index)
    elif line[index] == ')':
      (token, index) = read_right(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)

  tokens = convert_to_rpn(tokens)
  return tokens

def evaluate(tokens):
  answer = 0
  index = 0
  stack = []
  
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      #数字はstackにpush
      stack.append(tokens[index])
    else:
      #記号はstackの上二つを演算
      num2 = stack.pop()['number']
      num1 = stack.pop()['number']

      if tokens[index]['type'] == 'PLUS':
        stack.append({'type': 'NUMBER', 'number': (num1 + num2)})
      elif tokens[index]['type'] == 'MINUS':
        stack.append({'type': 'NUMBER', 'number': (num1 - num2)})
      elif tokens[index]['type'] == 'MULTIPLY':
        stack.append({'type': 'NUMBER', 'number': (num1 * num2)})
      elif tokens[index]['type'] == 'DIVIDE':
        if num2 == 0:
          print("Cannot divide by 0")
          exit(1)
        else:
          stack.append({'type': 'NUMBER', 'number': (num1 / num2)})
    index += 1

  answer = stack.pop()['number']
  return answer


def test(line):
  tokens = tokenize(line)
  actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("1")
  test("1+2")
  test("1+2.0")
  test("1.0-2")
  test("1.0*2.0")
  test("1.0+2.1-3")
  test("1.0*0.0")
  test("0/3")
  test("1.0*2.0/3")
  test("3.4+4*2-1/5")
  test("(3.0+4*(2-1))/5")
  test("((3-2)*(2.0*6)-1)*6")
  test("(2-1)*(3+2)+(4/3)")
  test("(2-1.0)*0+(4.0/3)")
  test("1-2-3")
  test("2.0/0")
  print("==== Test finished! ====\n")

run_test()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
