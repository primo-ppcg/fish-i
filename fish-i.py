import sys
from fractions import Fraction
import random
from getch import getch

NOUNS = {
  48: 0, 49: 1, 50:  2, 51:  3, 52:  4,  53:  5,  54:  6,  55:  7,
  56: 8, 57: 9, 97: 10, 98: 11, 99: 12, 100: 13, 101: 14, 102: 15
}

DYADICS = { *b'%*+,-()=' }
STACKS  = { *b'$:@[]lr{}~' }
MIRRORS = { *b'#/<>\\^_vx|' }
CONTROL = { *b' !&.;?ginop', 0 }
QUOTES  = { 34, 39 }

def mainloop(program, col_max, row_max):
  pc = (0, 0)
  dx, dy = 1, 0
  stack = []
  stacks = []
  register = None
  registers = []
  skip = False
  slurp = False
  slurp_char = None

  while True:
    code = program.get(pc, 0)

    if skip:
      skip = False

    elif slurp:
      if code != slurp_char:
        stack.append(code)
      else:
        slurp = False
        slurp_char = None

    elif code in NOUNS:
      stack.append(NOUNS[code])

    elif code in DYADICS:
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

    elif code in STACKS:
      if   code ==  36: stack[-2:] = stack[:-3:-1]
      elif code ==  58: stack.extend(stack[-1:])
      elif code ==  64: stack[-3:] = stack[-1:] + stack[-3:-1]
      elif code ==  91:
        n = stack.pop()
        stacks.append(stack[:-n])
        stack = stack[-n:]
        registers.append(register)
        register = None
      elif code ==  93:
        stack = stacks.pop() + stack
        register = registers.pop()
      elif code == 108: stack.append(len(stack))
      elif code == 114: stack.reverse()
      elif code == 123: stack = stack[1:] + stack[:1]
      elif code == 125: stack = stack[-1:] + stack[:-1]
      elif code == 126: stack = stack[:-1]

    elif code in MIRRORS:
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

    elif code in CONTROL:
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
        program[(x, y)] = v
        col_max[x] = max(col_max.get(x, 0), y)
        row_max[y] = max(row_max.get(y, 0), x)

    elif code in QUOTES:
      slurp = True
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


def run(source):
  lines = source.splitlines()
  program = {}
  col_max = {}
  row_max = {}
  for y, line in enumerate(lines):
    for x, c in enumerate(line):
      program[(x, y)] = ord(c)
      col_max[x] = max(col_max.get(x, 0), y)
      row_max[y] = max(row_max.get(y, 0), x)
  mainloop(program, col_max, row_max)


def main(argv):
  filename = ''
  try:
    filename = argv[1]
    with open(filename) as file:
      source = file.read()
  except IndexError:
    sys.exit('Usage: %s program.fsh'%argv[0])
  except OSError:
    sys.exit('File not found: %s'%filename)

  try:
    run(source)
  except:
    sys.exit('something smells fishy...')


if __name__ == '__main__':
  main(sys.argv)
