

#Author: Trung Le, Wenjing Rao
# Homework 2 Example
# MIPS byline disassembler
# 
# To run:        python3 disassembler.py


def disassemble(decoded):
    op_code = decoded[0:6]
    rs = int(decoded[6:11],2)
    rt = int(decoded[11:16],2)
    rd = int(decoded[16:21],2)
    shamt = decoded[21:26]
    funct = decoded[26:32]
    imm = decoded[16:32]
    if(imm[0] == '1'):  # Negative immediate, need to convert 2-complement  
        imm = -(65536 - int(imm,2))
    else:
        imm = int(imm,2)

    if (op_code == '001000'): # ADDI
        print('addi ${},${},{}'.format(rt,rs,imm))
    elif(op_code == '000000' and funct == '100000' and shamt == '00000'): # ADD
        print('add ${},${},${}'.format(rd,rs,rt))
    else:
        print('Instruction not supported')
    print()



def main():
    print('ECE366: MIPS Disassembler. Currently supports add,addi instructions')
    finished = False
    while(not(finished)):
        print('Please enter 8-digit hex:    (type quit to stop) ')
        usr_input = input()
        if (usr_input == 'quit'):
            finished = True
        else:
            print('Instruction: {} . Decoded: '.format(usr_input), end='')
            # Convert to base 16 first, then to binary, and format to 32-bit string
            decoded = str(bin(int(usr_input,16))[2:].zfill(32))
            disassemble(decoded)
if __name__ == "__main__":
    main()



