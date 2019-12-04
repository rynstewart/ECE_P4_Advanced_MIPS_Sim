#Assembly encoder by Eric Bauer

###Please use TrungLe's code for HW4 ###
#When writing this code I did not know support for tags was needed,
#this code does NOT support tags, and TrungLe's does
##I apologize for the error.


#Supports add, addi, and jump instructions
#Currently only supports immediates written in decimal.
import numpy as np

class converter:
    def __init__(self, infile):
        #read file and split lines into an array
        lines = open(infile,'r').read().split('\n')
        #split each line into command elements
        self.comms=[]
        for x in range(np.size(lines)):
            self.comms.append(lines[x].split(' '))

    def run(self):
        out=open('mc.txt','w')
        for instr in self.comms:
            line=0
            #remove extraneous characters
            for x in range(len(instr)):
                instr[x]=instr[x].replace('$','')
                instr[x]=instr[x].replace(',','')
            #encode arguments and opcode based on the command
            if instr[0]=='add':
                op=0
                func=0x20
                rd=int(instr[1])
                rs=int(instr[2])
                rt=int(instr[3])
                imm=0
            elif instr[0]=='addi':
                op=0x08
                func=0
                rd=0
                rt=int(instr[1])
                rs=int(instr[2])
                imm=int(instr[3])

            elif instr[0]=='jump':
                op=0x02
                func=0
                rt=0
                rs=0
                rd=0
                imm=int(instr[1])>>2

            line+=(op<<26)
            line+=(rs<<21)
            line+=(rt<<16)
            line+=(rd<<11)
            line+=imm
            line+=func
            out.write(format(line,'032b')+'\n')
        out.close()





#file = "mips1.asm"
thing=converter('mips1.asm')
thing.run()
#lines = open(file,'r').read().split('\n')
#    #split each line into command elements
#instr=[]
#for x in range(np.size(lines)):
#    instr.append(lines[x].split(' '))
