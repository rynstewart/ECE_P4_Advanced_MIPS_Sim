import time


##NEED: ori, addi, sw, beq, slt, addu, sub, xor, lw, slt, bne
def twoComplement(string):
    if(string[0] == '1'):
        imm = 65535 - int(string, 2)
        imm +=1
        imm = -imm
    else:
        imm = int(string, 2)
    return imm

class Statistics:
    def __init__(self, debugMode):
            self.I= ""               #current instruction being executed
            self.name = ""           # name of the instruction
            self.cycle = 0           # Total cycles in simulation
            self.DIC = 0             # Total Dynamic Instr Count
            self.threeCycles= 0      # How many instr that took 3 cycles to execute
            self.fourCycles = 0      #                          4 cycles
            self.fiveCycles = 0      #                          5 cycles
        #self.DataHazard = 0      #number of data hazards
        #self.ControlHazard = 0   #number of control hazards
        #self.NOPcount = 0        #keeps track of NOP
        #self.flushCount = 0      #keeps track of flush
        #self.stallCount = 0      #keeps track of stall count
            self.debugMode = debugMode
    
    def log(self,I,name,cycle,pc):
        self.I = I
        self.name = name
        self.pc = pc
        self.cycle +=  cycle
        self.DIC += 1
        self.threeCycles += 1 if (cycle == 3) else 0
        self.fourCycles += 1 if (cycle == 4) else 0
        self.fiveCycles += 1 if (cycle == 5) else 0

    def prints(self):
        #modify to work with asm instructions (not binary MC)
        '''
        imm = int(self.I[16:32],2) if self.I[16]=='0' else -(65535 -int(self.I[16:32],2)+1)
        if(self.debugMode):
            print("\n")
            print("Instruction: " + self.I)
            if(self.name == "add"):
                print("Cycle: " + str(self.cycle-4) + "|PC: " +str(self.pc*4) + " add $" + str(int(self.I[16:21],2)) + ",$" +str(int(self.I[6:11],2)) + ",$" + str(int(self.I[11:16],2)) + "   Taking 4 cycles")
            elif(self.name == "addi"):
                print("Cycle: " + str(self.cycle-4) + "|PC: " +str(self.pc*4) + " addi $" + str(int(self.I[16:21],2)) + ",$" +str(int(self.I[6:11],2)) + ","  + str(imm)  + "   Taking 4 cycles")
            elif(self.name == "beq"):
                print("Cycle: " + str(self.cycle-3) + "|PC: " +str(self.pc*4) + " beq $" + str(int(self.I[6:11],2)) + ",$" +str(int(self.I[11:16],2)) + ","  + str(imm)  + "   Taking 3 cycles")
            elif(self.name == "slt"):
                print("Cycle: " + str(self.cycle-4) + "|PC: " +str(self.pc*4) + " slt $" + str(int(self.I[16:21],2)) + ",$" +str(int(self.I[6:11],2)) + ",$" + str(int(self.I[11:16],2)) + "   Taking 4 cycles")
            elif(self.name == "sw"):
                print("Cycle: " + str(self.cycle-4) + "|PC :" +str(self.pc*4) + " sw $" + str(int(self.I[6:11],2)) + "," + str(int(self.I[16:32],2) - 8192) + "($" + str(int(self.I[6:11],2)) + ")" + "   Taking 4 cycles"  )
            else:
                print("")
            '''
     def exitSim(self):
        print("***Finished simulation***")
        print("Total # of cycles: " + str(self.cycle))
        print("Dynamic instructions count: " +str(self.DIC) + ". Break down:")
        print("                    " + str(self.threeCycles) + " instructions take 3 cycles" )  
        print("                    " + str(self.fourCycles) + " instructions take 4 cycles" )
        print("                    " + str(self.fiveCycles) + " instructions take 5 cycles" )

def saveJumpLabel(asm, labelIndex, labelName, labelAddr):
lineCount = 0
for line in asm:
    line = line.replace(" ","")
    if(line.count(":")):
        labelName.append(line[0:line.index(":")]) # append the label name
        labelIndex.append(lineCount) # append the label's index\
        labelAddr.append(lineCount*4)
        #asm[lineCount] = line[line.index(":")+1:]
    lineCount += 1
for item in range(asm.count('\n')): # Remove all empty lines '\n'
    asm.remove('\n')

def regNameInit(regName):
i = 0
while i<=23:
    regName.append(str(i))
    i = i + 1
regName.append('lo')
regName.append('hi')

def final_print(regval, PC, DIC):
    ("REGISTERS:")
    print("-----------")
    for x in range(len(regval)):
        if(x == 24):
            print("lo: ", hex(regval[x]))
        elif(x == 25):
            print("hi: ", hex(regval[x]))
        else:
            print("$", x,": ", hex(regval[x]))
    print("PC: ", hex(PC))
    print("DIC: ", hex(DIC))

    print("\n")
    print("Used Memory values:\n")
    print("            ", end="")
    for x in range(0,8,1):
        print("0x"+ format((x*4),"08x"), end=" ")
    print("\n")
    print("--------------------------------------------------------------------------------------------------",end="")
    count = 0
    print("\n")
    for x in range(0x2003,0x2100,4):
        if((x-0x3)%0x20==0):
            print("0x"+format(x-0x3,"08x") + '|', end=" ")
        print("0x", end="")
        for y in range(0,4,1):
            print(format(MEM[x-y], "02x"), end="")
        print(" ", end = "")
        count += 1
        if(count == 8):
            count = 0
            print("\n")

def simulate(Instructions, f, debugMode):
    MEM = [0]*12288 #intialize array to all 0s for 0x3000 indices
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo, hi
    LO = 24
    HI = 25

    finished = False
    while(not(finished)):
        fetch = Instructions[PC]
        
        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0

        if(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            #f.write(line)
            line = line.replace("addi","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] + int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
            line = line.replace("xor","")
            line = line.split(",")
            PC = PC + 4
            #x = format(int(line[1]),'032b')^format(int(line[2]),'032b')
            x = regval[int(line[1])]
            y = regval[int(line[2])]
            z = int(x)^int(y)
            regval[int(line[0])] = z
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        #addu
        elif(line[0:4] == "addu"): 
            line = line.replace("addu","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = abs(regval[int(line[1])]) + abs(regval[int(line[2])])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                    
        #slt
        elif(line[0:3] == "slt"):
            line = line.replace("slt","")
            line = line.split(",")
            if(regval[int(line[1])] < regval[int(line[2])]):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n') 

        elif(line[0:3] == "ori"):
            line = line.replace("ori", "")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[1])] = int(line[2],16) | regval[int(line[0])]
            temp_val = format( int(regval[int(line[1])]),'032b')

            f.write('Operation: $' + line[1] + '= $' + line[0] + "|"  + line[2])
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + str( int(line[2],16) ) + '=' + str(regval[int(line[0])]) + '\n')
        
        #bne
        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            if(regval[int(line[0])]!=regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = line[2]
                    lineCount = line[2]
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')
        

        #beq
        elif(line[0:3] == "beq"): # Beq
            line = line.replace("beq","")
            line = line.split(",")
            if(regval[int(line[0])]==regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = line[2]
                    lineCount = line[2]
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')

        elif(line[0:2] == "lw"):
            line= line.replace("lw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")
            PC = PC + 4
            regval[int(line[0])]= MEM[ int(line[1]) + regval[int(line[2])] ]
            f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:2] == "sw"):
            line= line.replace("sw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")
            PC = PC + 4
            MEM[ int(line[1]) + regval[int(line[2])] ] = regval[int(line[0])]
            f.write('Operation: MEM[ $' + line[2] + ' + ' + line[1] + ' ] = $' + line[0] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: None)

        elif(line[0:3] =="sub"):
            line = line.replace("sub","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] - regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:3] == "sll"): 
            line = line.replace("sll","")
            line = line.split(",")
            PC = PC + 4
            regval[int(line[0])] = regval[int(line[1])] << int(line[2])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' << ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')  
