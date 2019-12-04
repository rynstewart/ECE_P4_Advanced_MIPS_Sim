# Created by Samantha Stephans for ECE 366 fall '19

# bring in your header file, the * means you can use
# anyting in the header as if it was declared in this file
from header import *

# define registers and memory as dictionaries
registers = {0: 0,
            'PC': 0}
memory = {}
for i in range(8,24):
    registers[i] = 0

# main program, will read the file and execute the instructions
instr_list = []
line_count = 0
debug = False
filename = 'hex_sample.txt'
print("loading instructions from " + filename)
if (input('enable debug? y/n ').lower() == 'y'):
    print('debug enabled')
    debug = True
file = open(filename, 'r')  #open the instruction file

# you will need to read in the whole file first before executing anything
i = 0
for instr in file:
    if (instr == '\n' or instr[0] == '#'):
        continue
    line_count += 1
    instr = instr[0:10]
    if debug:
        print(instr)
    temp = Instruction(instr)
    instr_list.append(temp)
    instr_list.append('')
    instr_list.append('')
    instr_list.append('')
    i += 4

# the simulation of the program:
pc = 0
while pc < line_count*4:
    if pc % 4 == 0:
        if (instr_list[pc].type == 'r_type'):
            function = r_types[instr_list[pc].func]
        else:
            function = i_types[instr_list[pc].opcode]
        function(instr_list[pc], registers, debug, memory)
    pc = registers['PC']
# show the contents of the registers and memory after program completion
print_all(registers, memory)
