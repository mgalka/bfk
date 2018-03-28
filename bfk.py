from sys import stdout, stdin

class MemoryIndexError(Exception):
    pass

class Machine:
    def __init__(self, mem_size=30000):
        self.MEM = bytearray(mem_size)
        self.CODE = b''
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


    def getch(self):
        ch = ''
        while len(ch) != 1:
            ch = input()
        self.MEM[self.data_ptr] = ord(ch)

    def putch(self):
        print(chr(self.MEM[self.data_ptr]))

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

if __name__ == '__main__':
    machine = Machine()
    code = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
    machine.run(code)