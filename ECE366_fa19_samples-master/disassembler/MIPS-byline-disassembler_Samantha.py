# This program will take user input of an 8-digit hex representation of
# MIPS instructions (add and addi) and ouput the instruction
# translated into a human-readable string
# code by Samantha Stephans

# some useful data structures, overkill for this purpose, but is
# good to think about for future assignments
class Instruction():
    def __init__(self, hex_num):
        temp_num = int(hex_num, 16) # convert the input string to type int
        self.hex_num = hex(temp_num) # this just makes the hex number pretty with the 0x

        #make a binary string, the format gets rid of the 0b prefix in the string
        self.binary_string = format(temp_num, '0{}b'.format(32))

        # the string[0:3] syntax means the first 4 characters of string, use this fact to decode the binary

        self.opcode = self.binary_string[0:6]
        if self.opcode == '000000': # all r_types have this opcode, and function is the last 5 bits
            self.func = self.binary_string[26:32]
            self.type = 'r_type'
        else: # in this case the only else is type i
            self.func = self.opcode
            self.type = 'i_type'
        self.rs = int(self.binary_string[6:11], 2)
        self.rt = int(self.binary_string[11:16], 2)
        self.rd = int(self.binary_string[16:21], 2)
        if self.binary_string[16] == '1': # check the immediate for negative numbers and convert if needed
            self.imm = -((int(self.binary_string[16:32], 2) ^ 0xFFFF) + 1)
        else:
            self.imm = int(self.binary_string[16:32], 2)
        try:
            self.name = func_dict[self.func][1] # this will lookup the string name of the function in func_dict
        except:
            self.name = 'null'


# functions (instructions) to print the readable string
def add(instr):
    print(instr.hex_num + ' is ' + instr.name + ' $' + str(instr.rd) + ', $' + str(instr.rs) + ', $' + str(instr.rt))

def addi(instr):
    print(instr.hex_num + ' is ' + instr.name + ' $' + str(instr.rt) + ', $' + str(instr.rs) + ', ' + str(instr.imm))

# a python dictionary is like an array but instead of integer indices,
# there are 'keys' which can be of any data type.
# in this case, the binary string instruction code maps to the string name of
# the function to be called
func_dict = {'100000': (add, 'add'),
            '001000': (addi, 'addi')}

# main program runs here

# standard python syntax for printing to the screen
print("MIPS Byline Disassembler")

while(True):

    # ask the user for input, assign it to hex_instr
    hex_instr = input("Enter an 8-digit MIPS hex instruction and press enter: ")
    if hex_instr == 'quit':
        print('bye!')
        break
    else:
        # create Instruction object with the binary string
        # call the printing function for that instruction
        try:
            instruction = Instruction(hex_instr)
            function = func_dict[instruction.func][0] # get the function identity from func_dict
            function(instruction) # call this function to print
        except: # in case of invalid input
            print('not supported')
