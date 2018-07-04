import random
import string

class Switch(object):
    def __init__(self):
        self.cases = {}
    def case(self, name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.cases[name] = func
        return decorator
    def print_dict(self):
        print self.cases
    def __call__(self, case, *args, **kwargs):
        return self.cases[case](*args, **kwargs)


class interpreter(object):
   '''program must be a list of commands'''
   def __init__(self, program, stack, halt):
      self.iterator = 0
      self.program = [int(i, 16) for i in list(program)]
      self.program_size = len(program)
      self.stack = stack
      self.halt = halt

   switch = Switch()

   @switch.case(0)
   def push(self):
      self.iterator += 1
      val = self.program[self.iterator % self.program_size]
      self.stack.append(val)
   @switch.case(1)
   def pop(self):
      self.stack.pop()
   @switch.case(2)
   def rot2(self):
      TOS = self.stack.pop()
      TOS1 = self.stack.pop()
      self.stack.append(TOS)
      self.stack.append(TOS1)
   @switch.case(3)
   def nand(self):
       TOS = self.stack.pop()
       self.stack[-1] &= TOS
       self.stack[-1] = ~self.stack[-1]
   @switch.case(4)
   def dup(self):
      self.stack.append(stack[-1])
   @switch.case(5)
   def inc(self):
      self.stack[-1] += 1
   @switch.case(6)
   def dec(self):
      self.stack[-1] -= 1
   @switch.case(7)
   def mult(self):
      TOS = self.stack.pop()
      self.stack[-1] *= TOS
   @switch.case(8)
   def njmp(self):
      if self.stack[-1] == 0:
         self.iterator += 1
         self.iterator = self.program[self.iterator]
      else:
         pass
   @switch.case(9)
   def jmp(self):
      if self.stack[-1] == 0:
         pass
      else:
         self.iterator += 1
         self.iterator = self.program[self.iterator]
   @switch.case(10)
   def stop(self):
      raise Exception
   @switch.case(11)
   def add(self):
      TOS = self.stack.pop()
      self.stack[-1] += TOS
   @switch.case(12)
   def sub(self):
      TOS = self.stack.pop()
      self.stack[-1] -= TOS

   def __call__(self):
      instruction_set = {
         1: self.push,
         2: self.pop,
         3: self.rot2,
         4: self.nand,
         5: self.dup,
         6: self.add,
         7: self.sub,
         8: self.mult,
         9: self.jmp,
         10: self.stop,
         11: self.inc,
         12: self.dec,
         13: self.njmp,
         14: self.nand,
         15: self.nand,
      }
      # THere needs to be only one assert per "unit test"
      # and unit tests can be locially grouped together so that programs that pass onemore than one unit test in a group get a disproportionally higher fitness score. Also, unit tests can allow only a certain number of programs to pass, and we can control the population by the number of unit tests there are.unit tests that can be passed represent a limited resource that programs compete for

      # keep the program running until an exception is raised. Then stop and return the stack
      for _ in range(self.halt):
         try:
            interpreter.switch(self.program[self.iterator], self)
            # instruction_set[self.program[self.iterator]]()
            # print instruction_set[self.program[self.iterator]]
         except Exception as e:
            break
         self.iterator += 1
      return self.stack

class Population(object):
   def __init__(self, size=1000, mutation_rate=.02):
      self.population = []
      self.size = size
      self.mutation_rate = mutation_rate
      for _ in range(self.size):
         program = ''.join(random.choice('ABCDEF' + string.digits) for _ in range(random.randrange(30)))
         self.population.append(program)

   def __iter__(self):
      return iter(self.population)

   def mutate_program(self, program):
      program = list(program)
      i = 0
      while i < len(program):
         if random.uniform(0,1) < self.mutation_rate/3:
            program[i] = random.choice('123456789ABCDEF')
         if random.uniform(0,1) < self.mutation_rate/3:
            program.insert(i, random.choice('123456789ABCDEF'))
         if random.uniform(0,1) < self.mutation_rate/3:
            del program[i] 
         i += 1
      return ''.join(program)

   def mutate(self):
      self.population = set([self.mutate_program(p) for p in self.population])

   def refill(self):
      for _ in range(self.size - len(self.population)):
         program = ''.join(random.choice('ABCDEF' + string.digits) for _ in range(random.randrange(30)))
         self.population.append(program)

   def kill(self, program):
      self.population.remove(program)
                

def trainer(population):
   print ''' starting trainer
         '''
   def test(program, remove=[]):
      for _ in range(20):
        x = random.randrange(10)
        y = random.randrange(10)
        z = random.randrange(10)
        output = interpreter(program,[x, y, z], halt=1000)()
        if len(output)==1 and output[0] == x+y+z:
           pass
        else:
           if random.uniform(0,1) < 0.8:
              remove.append(program)
           return False
        return True
   
   for __ in range(20):
      remove = []
      for program in population:
         test(program, remove)
         # convert a program to a list of integers
      for program in remove:
         population.kill(program)
      population.refill()

   for program in population:
      if test(program):
         print program, interpreter(program, [1,2,3], halt=1000)()
   

def main():
 #  program = '11126'
 #  output = interpreter(program, [], 1000)()
 #  print(output)

 #  program = '02B89'
 #  output = interpreter(program, [], 1000)()
 #  print(output)

 #  p = Population(5)
  # print [i for i in p]
   #p.mutate()
   #p.mutate()
   #print [i for i in p]
   

   population = Population()
   trainer(population)

   
if __name__ == '__main__':
  main()







