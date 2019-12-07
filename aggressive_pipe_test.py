import time

class Statistics:
    def __init__(self, debugMode):
        self.I= ""               #current instruction being executed
        self.name = ""           # name of the instruction
        self.cycle = 0           # Total cycles in simulation
        self.DIC = 0             # Total Dynamic Instr Count
        self.threeCycles= 0      # How many instr that took 3 cycles to execute
        self.fourCycles = 0      #                          4 cycles
        self.fiveCycles = 0      #                          5 cycles
        self.DataHazard = 0      #number of data hazards
        self.ControlHazard = 0   #number of control hazards
        self.NOPcount = 0        #keeps track of NOP
        self.flushCount = 0      #keeps track of flush
        self.stallCount = 0      #keeps track of stall count
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
    print("REGISTERS:")
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

    print("\n*************************************** Used Memory values ***************************************\n")
    print("offset:     ", end="")
    for x in range(0,8,1):
        print("0x"+ format((x*4),"08x"), end=" ")
    print("\n")
    print("--------------------------------------------------------------------------------------------------",end="")
    count = 0
    print("\n")
    y=0
    for x in range(0x2000,0x2041,1):
        if((x-0x2000) % 0x20 ==0):
            print("0x" +format(0x2000+ y,"08x") + '|', end=" ")
            y += 0x20

        if count == 8:
            count = 0
            print(" ", end = "\n")
        if((x-0x2000)%4==0):  
            print('0x'+format(MEM[x], "08x"), end=" ")
            count += 1 


        
def get_imm(instr, index):

    #first check base
    if '0x' in instr[index]:
        imm = int(instr[index][2:],16)
    else:
        imm = int(instr[index])

    return imm

def cycle_tracker(instr_cycles, DIC):
    
    index = DIC      
    if "Fetch" in instr_cycles[index]:
        print("\n"+instr_cycles[index][0] +" in Fetch Cycle")
        instr_cycles[index].remove("Fetch")

    elif "Decode" in instr_cycles[index]:
        print("\n" + instr_cycles[index][0] + " in Decode Cycle")
        instr_cycles[index].remove("Decode")
        try:
            if "Fetch" in instr_cycles[index+1]:
                print("\n"+instr_cycles[index+1][0] +" in Fetch Cycle")
                instr_cycles[index+1].remove("Fetch")
        except:
            return
    
    elif "Execute" in instr_cycles[index]:
        print("\n" + instr_cycles[index][0] + " in Decode Cycle")
        instr_cycles[index].remove("Execute")
        try:
            if "Fetch" in instr_cycles[index+1]:
                print("\n"+instr_cycles[index+1][0] +" in Fetch Cycle")
                instr_cycles[index+1].remove("Fetch")
        except:
            return



def simulate(Instructions, f, debugMode):
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    regNameInit(regName)
    LO = 24
    HI = 25
    stats = Statistics(debugMode)
    
    saveJumpLabel(Instructions,labelIndex,labelName, labelAddr)
    
    instr_cycles = []
    
    f = open(f,"w+")

    for loop in range(2):
        DIC = 0
        PC = 0
        MEM = [0]*12288 #intialize array to all 0s for 0x3000 indices
        regval = [0]*26 #0-23 and lo, hi
        lineCount = 0
        i = 0   
        while lineCount < len(Instructions):
            
            line = Instructions[lineCount]

            

            if(debugMode == 1 and loop == 1):
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
                line = line.replace("addi","")
                line = line.split(",")
                imm = get_imm(line,2)
                regval[int(line[0])] = (regval[int(line[1])] + imm)  & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                if(debugMode != 1):
                    DIC += 1
                PC += 4
                if(loop == 0):
                    instr_cycles.append(["addi", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("addi", 4, PC)
                if(debugMode == 1 and loop == 1):
                    cycle_tracker(instr_cycles, DIC)
                    DIC += 1


            elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
                line = line.replace("xor","")
                line = line.split(",")
                x = regval[int(line[1])]
                y = regval[int(line[2])]
                z = int(x)^int(y)
                regval[int(line[0])] = z & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["xor", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("xor", 4, PC)
                PC += 4

                if(debugMode == 1 and loop == 1):

                    if(i == 0):
                        print("Cycle 1: Instruction Fetch" + '\n')
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
                        print("MemtoReg is now 0")
                        print("MemWrite is now 0")
                        print("Branch is now 0")
                        print("ALUSrcA is now X")
                        print("ALUSrcB is now X")
                        print("RegDst is now 1")
                        print("RegWrite is now 1")
                        i = 0
                        DIC += 1  
                        stats.log("xor", 4, PC)


            #addu
            elif(line[0:4] == "addu"): 
                line = line.replace("addu","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["addu", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("addu", 4, PC)

                regval[int(line[0])] = (abs(regval[int(line[1])]) + abs(regval[int(line[2])])) & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                if(debugMode == 1 and loop == 1):

                    if(i == 0):
                        print("Cycle 1: Instruction Fetch" + '\n')
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
                        print("MemtoReg is now 0")
                        print("MemWrite is now 0")
                        print("Branch is now 0")
                        print("ALUSrcA is now X")
                        print("ALUSrcB is now X")
                        print("RegDst is now 1")
                        print("RegWrite is now 1")
                        i = 0
                        DIC += 1
                        stats.log("addu", 4, PC)

            elif(line[0:4] == "sltu"):
                line = line.replace("sltu","")
                line = line.split(",")
                if(abs(regval[int(line[1])]) < abs(regval[int(line[2])])):
                    regval[int(line[0])] = 1
                else:
                    regval[int(line[0])] = 0

                PC = PC + 4
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sltu", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("sltu", 4, PC) 

                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')
                if(debugMode == 1 and loop == 1):

                    if(i == 0):
                        print("Cycle 1: Instruction Fetch" + '\n')
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
                        print("MemtoReg is now 0")
                        print("MemWrite is now 0")
                        print("Branch is now 0")
                        print("ALUSrcA is now X")
                        print("ALUSrcB is now X")
                        print("RegDst is now 1")
                        print("RegWrite is now 1")
                        i = 0
                        DIC += 1
                        stats.log("sltu", 4, PC)


            elif(line[0:3] == "slt"):
                line = line.replace("slt","")
                line = line.split(",")
                if(regval[int(line[1])] < regval[int(line[2])]):
                    regval[int(line[0])] = 1
                else:
                    regval[int(line[0])] = 0

                PC = PC + 4
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["slt", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("slt", 4, PC)

                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')
                if(debugMode == 1 and loop == 1):
                   
                    if(i == 0):
                        print("Cycle 1: Instruction Fetch" + '\n')
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
                        print("MemtoReg is now 0")
                        print("MemWrite is now 0")
                        print("Branch is now 0")
                        print("ALUSrcA is now X")
                        print("ALUSrcB is now X")
                        print("RegDst is now 1")
                        print("RegWrite is now 1")
                        i = 0
                        DIC += 1
                        stats.log("slt", 4, PC)

            elif(line[0:3] == "ori"):
                line = line.replace("ori", "")
                line = line.split(",")
                imm = get_imm(line,2)
                PC = PC + 4
                regval[int(line[0])] = (imm | regval[int(line[1])]) & 0xFFFFFFFF
                if(loop == 0):
                    instr_cycles.append(["ori", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("ori", 4, PC)
                if(debugMode != 1):
                    DIC += 1
                f.write('Operation: $' + line[0] + '= $' + line[1] + " | "  + line[2] + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + '=' + line[2] + '\n')
                if(debugMode == 1 and loop == 1):
                    for j in range(2):
                        cycle_tracker(instr_cycles, DIC)
                    DIC += 1
            #bne
            elif(line[0:3] == "bne"): # BNE
                line = line.replace("bne","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["bne", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("bne", 3, PC)

                if (debugMode == 1 and loop == 1):

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
                        DIC += 1
                        stats.log("beq", 4, PC)

                if(regval[int(line[0])]!=regval[int(line[1])]):
                    if(line[2].isdigit()): # First,test to see if it's a label or a integer
                        PC = int(line[2])*4
                        lineCount = int(line[2])
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
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["beq", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("beq", 3, PC)

                if (debugMode == 1 and loop == 1):

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
                        DIC += 1
                        stats.log("beq", 4, PC)

                if(regval[int(line[0])]==regval[int(line[1])]):
                    if(line[2].isdigit()): # First,test to see if it's a label or a integer
                        PC = int(line[2])*4
                        lineCount = int(line[2])
                        f.write('PC is now at ' + str(line[2]) + '\n')
                        f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                        f.write('No Registers have changed. \n')
                        continue
                    else: # Jumping to label
                        for i in range(len(labelName)):
                            if(labelName[i] == line[2]):
                                PC = labelAddr[i]
                                lineCount = labelIndex[i]
                                f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                                f.write('No Registers have changed. \n')
                                continue
                f.write('No Registers have changed. \n')



            elif(line[0:2] =="lw" and not('lw_loop' in line)):
                line= line.replace("lw","")
                line= line.replace("(",",")
                line= line.replace(")","")
                line= line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["lw", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("lw", 5, PC)
                imm = get_imm(line, 1)
                MEM_val = MEM[ regval[int(line[2])] + imm ] & 0xFFFFFFFF
                bin_str = format(MEM_val, '32b')
                if bin_str[0] == '1':
                    MEM_val = MEM_val ^ 0xffffffff
                    MEM_val +=1
                    MEM_val = -MEM_val

                regval[int(line[0])]= MEM_val
                f.write('Operation: $' + line[0] + ' = ' + 'MEM[$' + line[2] + ' + ' + line[1] + ']; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

                if (debugMode == 1 and loop == 1):
                    
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
                        DIC += 1
                        stats.log("lw", 4, PC)

                    

            elif(line[0:2] =="sw" and not('sw_' in line)):

                line= line.replace("sw","")
                line= line.replace("(",",")
                line= line.replace(")","")
                line= line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sw", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("sw", 4, PC)
                imm = get_imm(line, 1)
                MEM_val = regval[int(line[0])] 
                MEM[ regval[int(line[2])] + imm ] = MEM_val
                f.write('Operation: MEM[ $' + line[2] + ' + ' + line[1] + ' ] = $' + line[0] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: None\n')
                if (debugMode == 1 and loop == 1):
                    
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
                        DIC += 1
                        stats.log("sw", 4, PC)


            elif(line[0:3] =="sub"):
                line = line.replace("sub","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sub", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("sub", 4, PC)
                regval[int(line[0])] = (regval[int(line[1])] - regval[int(line[2])])  & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                if(debugMode == 1 and loop == 1):

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
                        DIC += 1
                        stats.log("sub", 4, PC)


            elif(line[0:3] == "sll"): 
                line = line.replace("sll","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sll", "Fetch", "Decode", "Execute", "Memory", "Write Back"])
                    stats.log("sll", 4, PC)
                imm = get_imm(line,2)
                regval[int(line[0])] = (regval[int(line[1])] << imm) & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' << ' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                if(debugMode == 1 and loop == 1):

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
                        DIC += 1
                        stats.log("sll", 4, PC)


            lineCount += 1

    PC = (len(Instructions)-len(labelName)) * 4 
    tot_cycles = DIC + 4

    final_print(regval,MEM, PC, DIC)    
    print("\n\n**************************************** FINAL CYCLE INFO ****************************************\n")
    print("IDEAL PIPLINE: ", tot_cycles)
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
    simulate(asm, file_NameOut, select)


  

main()