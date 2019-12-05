import time

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
    
    def log(self,name,cycle,pc):
        self.name = name
        self.pc = pc
        self.cycle +=  cycle
        self.DIC += 1
        self.threeCycles += 1 if (cycle == 3) else 0
        self.fourCycles += 1 if (cycle == 4) else 0
        self.fiveCycles += 1 if (cycle == 5) else 0

        ''' 
    def prints(self):
        #modify to work with asm instructions (not binary MC)
        
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

def final_print(regval, MEM, PC, DIC):
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

def get_imm(instr, index):

    #first check base
    if '0x' in instr[index]:
        imm = int(instr[index][2:],16)
    else:
        imm = int(instr[index])

    return imm

def simulate(Instructions, f, debugMode):
    MEM = [0]*12288 #intialize array to all 0s for 0x3000 indices
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    PC = 0
    DIC = 0
    regNameInit(regName)
    regval = [0]*26 #0-23 and lo, hi
    LO = 24
    HI = 25
    stats = Statistics(debugMode)

    saveJumpLabel(Instructions,labelIndex,labelName, labelAddr)


    f = open(f,"w+")
    lineCount = 0
    i = 0
    while lineCount < len(Instructions):
        
        line = Instructions[lineCount]
        if(debugMode == 1):
            while(True):
                user_pause = input("Press enter to continue or q to quit diagnosis mode:\n")
                if(user_pause == ""):
                    print('MIPS Instruction: ' + line + '\n')
                    break
		        
                if(user_pause == "q"):
                    print("Continuing in non-stop mode")
                    debugMode = 2
                    break

                else:
                    continue
        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0
        

        if(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            #f.write(line)
            #breakpoint()
            line = line.replace("addi","")
            line = line.split(",")
            imm = get_imm(line,2)
            regval[int(line[0])] = regval[int(line[1])] + imm
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            DIC += 1
            PC += 1
            if debugMode != 1:
                stats.log("addi", 4, PC)

            if(debugMode == 1):
                #breakpoint()
                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    PC = PC + 4
                    print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0" + '\n')
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0" + '\n')
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 10")
                    print("RegDst is now X")
                    print("RegWrite is now 0" + '\n')
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC =
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 0")
                    print("RegWrite is now 1" + '\n')
                    i = 0
                    stats.log("addi", 4, PC)


        elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
            line = line.replace("xor","")
            line = line.split(",")
            #PC = PC + 4
            #x = format(int(line[1]),'032b')^format(int(line[2]),'032b')
            x = regval[int(line[1])]
            y = regval[int(line[2])]
            z = int(x)^int(y)
            regval[int(line[0])] = z
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            DIC += 1

            PC += 1
            if debugMode != 1:
                stats.log("xor", 4, PC)

            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 0")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 1")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("xor", 4, PC)


        #addu
        elif(line[0:4] == "addu"): 
            line = line.replace("addu","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("addu", 4, PC)

            regval[int(line[0])] = abs(regval[int(line[1])]) + abs(regval[int(line[2])])
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 0")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 1")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("addu", 4, PC)
        #slt
        elif(line[0:3] == "slt"):
            line = line.replace("slt","")
            line = line.split(",")
            if(regval[int(line[1])] < regval[int(line[2])]):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("slt", 4, PC)

            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')
            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 0")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 1")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("slt", 4, PC)

        elif(line[0:3] == "ori"):
            line = line.replace("ori", "")
            line = line.split(",")
            imm = get_imm(line,2)
            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("ori", 4, PC)
            regval[int(line[0])] = (imm | regval[int(line[1])]) & 0xFFFFFFFF

            f.write('Operation: $' + line[0] + '= $' + line[1] + " | "  + line[2] + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + '=' + line[2] + '\n')
            if(debugMode == 1):
                #breakpoint()
                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 10")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC =
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 0")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("ori", 4, PC)
        #bne
        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            DIC += 1
            stats.log("bne", 3, PC)
            if(regval[int(line[0])]!=regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = int(line[2])*4
                    lineCount = int(line[2])
                    if debugMode != 1:
                        stats.log("bne", 3, PC)
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            if debugMode != 1:
                                stats.log("bne", 3, PC)
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')
            if (debugMode == 1):
                # breakpoint()
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 1")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 0")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i = 0
                    stats.log("bne", 4, PC)

        #beq
        elif(line[0:3] == "beq"): # Beq
            line = line.replace("beq","")
            line = line.split(",")
            DIC += 1
            if(regval[int(line[0])]==regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = int(line[2])*4
                    lineCount = int(line[2])
                    if debugMode != 1:
                        stats.log("beq", 3, PC)
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            if debugMode != 1:
                                stats.log("beq", 3, PC)
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')

                if (debugMode == 1):
                    # breakpoint()
                    if (i == 0):
                        print("Cycle 1: Instruction Fetch" + '\n')
                        # PC = PC + 4
                        # print('PC is now at ' + str(PC) + '\n')
                        print("MemtoReg is now X")
                        print("MemWrite is now 0")
                        print("Branch is now 0")
                        print("ALUSrcA is now 0")
                        print("ALUSrcB is now 1")
                        print("RegDst is now X")
                        print("RegWrite is now 0")
                        i += 1
                        continue

                    elif (i == 1):
                        print("Cycle 2: Decode" + '\n')
                        # PC = PC + 4
                        # print('PC is now at ' + str(PC) + '\n')
                        print("MemtoReg is now X")
                        print("MemWrite is now 0")
                        print("Branch is now 0")
                        print("ALUSrcA is now 0")
                        print("ALUSrcB is now 11")
                        print("RegDst is now X")
                        print("RegWrite is now 0")
                        i += 1
                        continue

                    elif (i == 2):
                        print("Cycle 3: Execute" + '\n')
                        # PC = PC + 4
                        # print('PC is now at ' + str(PC) + '\n')
                        print("MemtoReg is now X")
                        print("MemWrite is now 0")
                        print("Branch is now 1")
                        print("ALUSrcA is now 1")
                        print("ALUSrcB is now 0")
                        print("RegDst is now X")
                        print("RegWrite is now 0")
                        i = 0
                        stats.log("beq", 4, PC)

                #continue


        elif(line[0:2] =="lw" and not('lw_loop' in line)):
            line= line.replace("lw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")
            PC = PC + 4
            DIC += 1
            imm = get_imm(line, 1)

            if debugMode != 1:
                stats.log("lw", 5, PC)
            MEM_val = MEM[ regval[int(line[2])] + imm ] & 0xFFFFFFFF

            regval[int(line[0])]= MEM_val
            f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

            if (debugMode == 1):
                # breakpoint()
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 10")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue
                elif (i == 4):
                    print("Cycle 5: Write Back" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 1")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 0")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("lw", 4, PC)

        elif(line[0:2] =="sw" and not('sw_' in line)):

            line= line.replace("sw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")
            PC = PC + 4
            DIC += 1
            #breakpoint()
            imm = get_imm(line, 1)
            if debugMode != 1:
                stats.log("sw", 4, PC)
            MEM_val = regval[int(line[0])] & 0xFFFFFFFFF
            MEM[ regval[int(line[2])] + imm ] = MEM_val
            f.write('Operation: MEM[ $' + line[2] + ' + ' + line[1] + ' ] = $' + line[0] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: None\n')
            if (debugMode == 1):
                # breakpoint()
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 10")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n')
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 1")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i = 0
                    stats.log("sw", 4, PC)


        elif(line[0:3] =="sub"):
            line = line.replace("sub","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("sub", 4, PC)
            regval[int(line[0])] = regval[int(line[1])] - regval[int(line[2])]
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 0")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 1")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("sub", 4, PC)


        elif(line[0:3] == "sll"): 
            line = line.replace("sll","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            imm = get_imm(line,2)
            if debugMode != 1:
                stats.log("sll", 4, PC)
            regval[int(line[0])] = (regval[int(line[1])] << imm) & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' << ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 1")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    # PC = PC + 4
                    # print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 0")
                    print("ALUSrcB is now 11")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now X")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now 1")
                    print("ALUSrcB is now 0")
                    print("RegDst is now X")
                    print("RegWrite is now 0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    #PC = PC + 4
                    #print('PC is now at ' + str(PC) + '\n')
                    print("MemtoReg is now 0")
                    print("MemWrite is now 0")
                    print("Branch is now 0")
                    print("ALUSrcA is now X")
                    print("ALUSrcB is now X")
                    print("RegDst is now 1")
                    print("RegWrite is now 1")
                    i = 0
                    stats.log("sll", 4, PC)

        lineCount += 1

    final_print(regval,MEM, PC, DIC)    
    print("\n************ FINAL CYCLE INFO ************\n")
    stats.exitSim()

    f.close()


def splitText(text):
    return text.split("\n")

def readIn(s):
    text = ""
    with open(s, "r") as f:
        for line in f:
            if (line != "\n" and line[0]!='#'):
                text += line

    return text

def main():
    
    while(True):
        file_Name = input("Please type input file name or enter for default (proj_A.asm), or q to quit:\n")
        if(file_Name == "q"):
            print("Bye!")
            return
        if(file_Name == ""):
            file_Name = "proj_A.asm"
        try:
            f = open(file_Name)
            f.close()
            break
        except FileNotFoundError:
            print('File does not exist')

    while(True):
        file_NameOut = input("Please type output file name or enter for default (mc.txt), or q to quit:\n")
        if(file_NameOut == "q"):
            print("Bye!")
            return
        if(file_NameOut == ""):
            file_NameOut = "mc.txt"
            break

    while(True):
        user_select = input("select one of the below or q to quit:\n" + \
            "\ta) Diagnosis mode\n" +\
            "\tb) Non-stop mode\n")

        if(user_select == "a"):
            select = 1
            break
        
        if(user_select == "b"):
            select = 2
            break

        if(user_select == "q"):
            return

        else:
            print("ERROR: Please type valid input\n")
            continue

    h = open(file_Name,"r")

    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')
    #breakpoint()
    simulate(asm, file_NameOut, select)


  

main()
