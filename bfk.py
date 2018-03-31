import fileinput
import sys
import os
class MemoryIndexError(Exception):
    pass

class Machine:
    def __init__(self, mem_size=30000):
        self.MEM = bytearray(mem_size)
        self.last_while_enter = None
        self.CODE = []
        self.data_ptr = 0
        self.code_ptr = 0
        self.commands = {
                '>': self.inc_index,
                '<': self.dec_index,
                '+': self.inc_value,
                '-': self.dec_value,
                '.': self.putch,
                ',': self.getch,
                '[': self.while_enter,
                ']': self.while_loop
        }

    def inc_index(self):
        self.data_ptr += 1
        if self.data_ptr > len(self.MEM) - 1:
            raise MemoryIndexError
    
    def dec_index(self):
        self.data_ptr -= 1
        if self.data_ptr > len(self.MEM) - 1:
            raise MemoryIndexError

    def inc_value(self):
        self.MEM[self.data_ptr] += 1

    def dec_value(self):
        self.MEM[self.data_ptr] -= 1

    def find_while_exit(self):
        bracket_counter = 1
        self.code_ptr += 1
        while True:
            if self.CODE[self.code_ptr] == ']':
                bracket_counter += 1
            if self.CODE[self.code_ptr] == '[':
                bracket_counter -= 1
            if bracket_counter == 0:
                break
            self.code_ptr += 1

    def while_enter(self):
        self.last_while_enter = self.code_ptr
        if self.MEM[self.data_ptr] == 0:
            self.code_ptr = self.find_while_exit()

    def while_loop(self):
        if self.MEM[self.data_ptr] != 0:
            self.code_ptr = self.last_while_enter

    def getch(self):
        ch = ''
        while len(ch) != 1:
            ch = input()
        self.MEM[self.data_ptr] = ord(ch)

    def putch(self):
        sys.stdout.write(chr(self.MEM[self.data_ptr]))

    def reset(self):
        for i, _ in enumerate(self.MEM):
            self.MEM[i] = 0
        self.data_ptr = 0
        self.code_ptr = 0

    def load(self, code):
        self.CODE = code

    def run(self, code=None):
        if code is not None:
            self.reset()
            self.load(code)
        while self.code_ptr < len(self.CODE):
            instruction = self.CODE[self.code_ptr]
            if instruction in self.commands:
                self.commands[instruction]()
            self.code_ptr += 1

if __name__ == '__main__':
    # Hello World code
    # '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
    machine = Machine()
    code = sys.argv[1]
    machine.run(code)
    sys.stdout.write(os.sep)