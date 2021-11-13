import sys
from collections import deque
from fractions import Fraction
import random

from getch import getch

T_NOUN, T_DYADIC, T_STACK, T_MIRROR, T_CONTROL, T_QUOTE, T_OTHER = range(7)
SYMBOLS = {
  T_NOUN:    b'0123456789abcdef',
  T_DYADIC:  b'%*+,-()=',
  T_STACK:   b'$:@[]lr{}~',
  T_MIRROR:  b'#/<>\\^_vx|',
  T_CONTROL: b'\0 !&.;?ginop',
  T_QUOTE:   b'"\''
}
TYPES = dict([(c, t) for t, chars in SYMBOLS.items() for c in chars])
NOUNS = dict([(c, (c-48)%39) for c in SYMBOLS[T_NOUN]])

def run(program, col_max, row_max):
  pc = (0, 0)
  dx, dy = 1, 0
  stack = deque()
  stacks = []
  register = None
  registers = []
  skip = False
  slurp_char = None

  while True:
    code, type = program.get(pc, (0, T_CONTROL))

    if skip:
      skip = False

    elif slurp_char is not None:
      if code != slurp_char:
        stack.append(code)
      else:
        slurp_char = None

    elif type == T_NOUN:
      stack.append(NOUNS[code])

    elif type == T_DYADIC:
      a, b = stack.pop(), stack.pop()
      if   code ==  37: c = b % a
      elif code ==  42: c = b * a
      elif code ==  43: c = b + a
      elif code ==  44:
        c = Fraction(b, a)
        if c.denominator == 1:
          c = c.numerator
      elif code ==  45: c = b - a
      elif code ==  40: c = int(b < a)
      elif code ==  41: c = int(b > a)
      elif code ==  61: c = int(b == a)
      stack.append(c)

    elif type == T_STACK:
      if code ==  36:
        b, a = stack.pop(), stack.pop()
        stack.extend([b, a])
      elif code ==  58:
        stack.append(stack[-1])
      elif code ==  64:
        c, b, a = stack.pop(), stack.pop(), stack.pop()
        stack.extend([c, a, b])
      elif code ==  91:
        n = stack.pop()
        tmp = deque()
        for _ in range(n):
          tmp.appendleft(stack.pop())
        stacks.append(stack)
        stack = tmp
        registers.append(register)
        register = None
      elif code ==  93:
        if len(stacks) >= 1:
          stack = stacks.pop() + stack
          register = registers.pop()
        else:
          stack = deque()
          register = None
      elif code == 108: stack.append(len(stack))
      elif code == 114: stack.reverse()
      elif code == 123: stack.rotate(-1)
      elif code == 125: stack.rotate(1)
      elif code == 126: stack.pop()

    elif type == T_MIRROR:
      if   code ==  35: dx, dy = (-dx, -dy)
      elif code ==  47: dx, dy = (-dy, -dx)
      elif code ==  60: dx, dy = ( -1,   0)
      elif code ==  62: dx, dy = (  1,   0)
      elif code ==  92: dx, dy = ( dy,  dx)
      elif code ==  94: dx, dy = (  0,  -1)
      elif code ==  95: dx, dy = ( dx, -dy)
      elif code == 118: dx, dy = (  0,   1)
      elif code == 120: dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
      elif code == 124: dx, dy = (-dx,  dy)

    elif type == T_CONTROL:
      if   code ==  33:
        skip = True
      elif code ==  38:
        if register is None:
          register = stack.pop()
        else:
          stack.append(register)
          register = None
      elif code ==  46:
        y, x = stack.pop(), stack.pop()
        pc = (x, y)
      elif code ==  59:
        return
      elif code ==  63:
        skip = not bool(stack.pop())
      elif code == 103:
        y, x = stack.pop(), stack.pop()
        stack.append(program.get((x, y), 0))
      elif code == 105:
        char = getch()
        if char:
          stack.append(char[0])
        else:
          stack.append(-1)
      elif code == 110:
        n = stack.pop()
        if isinstance(n, Fraction) and n.denominator > 1:
          print(float(n), end = '')
        else:
          print(n, end = '')
      elif code == 111:
        n = stack.pop()
        print(chr(int(n)), end = '')
      elif code == 112:
        y, x, v = stack.pop(), stack.pop(), stack.pop()
        program[(x, y)] = (v, TYPES.get(v, T_OTHER))
        col_max[x] = max(col_max.get(x, 0), y)
        row_max[y] = max(row_max.get(y, 0), x)

    elif type == T_QUOTE:
      slurp_char = code

    else:
      raise RuntimeError("Invalid instruction", code)

    x = pc[0] + dx
    if x < 0 or x > row_max.get(pc[1], 0):
      if dx < 0:
        x = row_max.get(pc[1], 0)
      elif dx > 0:
        x = 0
    y = pc[1] + dy
    if y < 0 or y > col_max.get(pc[0], 0):
      if dy < 0:
        y = col_max.get(pc[0], 0)
      elif dy > 0:
        y = 0

    pc = (x, y)


def parse(source):
  lines = source.splitlines()
  program = {}
  col_max = {}
  row_max = {}
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      program[(x, y)] = (ord(c), TYPES.get(ord(c), T_OTHER))
      col_max[x] = max(col_max.get(x, 0), y)
      row_max[y] = max(row_max.get(y, 0), x)
  return program, col_max, row_max


def main(argv):
  filename = ''
  try:
    filename = argv[1]
    with open(filename, encoding='utf-8') as file:
      source = file.read()
  except IndexError:
    sys.exit('Usage: %s program.fsh'%argv[0])
  except OSError:
    sys.exit('File not found: %s'%filename)

  program, col_max, row_max = parse(source)

  try:
    run(program, col_max, row_max)
  except:
    sys.exit('something smells fishy...')


if __name__ == '__main__':
  main(sys.argv)
