
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
    print('\n************************ CYCLE INFORMATION ************************\n')    
    if "Fetch" in instr_cycles[index][1]:
        print("\n"+instr_cycles[index][0] +" in Fetch Cycle")
        del instr_cycles[index][1] 
        return True

    if "Decode" in instr_cycles[index][1]:
        print("\n" + instr_cycles[index][0] + " in Decode Cycle")
        del instr_cycles[index][1] 
        try:
            if "Fetch" in instr_cycles[index+1][1]:
                print("\n"+instr_cycles[index+1][0] +" in Fetch Cycle")
                del instr_cycles[index+1][1]
        except:
            return False
        
        return True
    
    if "Execute" in instr_cycles[index][1]:
        print("\n" + instr_cycles[index][0] + " in Execute Cycle")
        if(instr_cycles[index][1][1] != ""):
            print("\n\t" + instr_cycles[index][1][1])
        del instr_cycles[index][1]
        
        try:
            if "Decode" in instr_cycles[index+1][1]:
                print("\n"+instr_cycles[index+1][0] +" in Decode Cycle")
                del instr_cycles[index+1][1]
        except:
            return False
        
        try:
            if "Fetch" in instr_cycles[index+2][1]:
                print("\n"+instr_cycles[index+2][0] +" in Fetch Cycle")
                del instr_cycles[index+2][1]
        except:
            return False
        
        return True

    if "Memory" in instr_cycles[index][1]:
        print("\n" + instr_cycles[index][0] + " in Memory Cycle")
        del instr_cycles[index][1]
        
        try:
            if "Execute" in instr_cycles[index+1][1]:
                print("\n"+instr_cycles[index+1][0] +" in Execute Cycle")
                if(instr_cycles[index+1][1][1] != ""):
                    print("\n\t" + instr_cycles[index+1][1][1])
                del instr_cycles[index+1][1]
        except:
            return False
        
        try:
            if "Decode" in instr_cycles[index+2][1]:
                print("\n"+instr_cycles[index+2][0] +" in Decode Cycle")
                del instr_cycles[index+2][1]
        except:
            return False
        
        try:
            if "Fetch" in instr_cycles[index+3][1]:
                print("\n"+instr_cycles[index+3][0] +" in Fetch Cycle")
                del instr_cycles[index+3][1]
        except:
            return False
        
        return True
    
    if "Write Back" in instr_cycles[index][1]:
        print("\n" + instr_cycles[index][0] + " in Write Back Cycle")
        if(instr_cycles[index][1][1] != ""):
            print("\n\t" + instr_cycles[index][1][1])
        instr_cycles[index][1]
        
        try:
            if "Memory" in instr_cycles[index+1][1]:
                print("\n"+instr_cycles[index+1][0] +" in Memory Cycle")
                del instr_cycles[index+1][1]
        except:
            return False

        try:
            if "Execute" in instr_cycles[index+2][1]:
                print("\n"+instr_cycles[index+2][0] +" in Execute Cycle")
                if(instr_cycles[index+2][1][1] != ""):
                    print("\n\t" + instr_cycles[index+2][1][1])
                del instr_cycles[index+2][1]
        except:
            return False
        
        try:
            if "Decode" in instr_cycles[index+3][1]:
                print("\n"+instr_cycles[index+3][0] +" in Decode Cycle")
                del instr_cycles[index+3][1]
        except:
            return False
        
        try:
            if "Fetch" in instr_cycles[index+4][1]:
                print("\n"+instr_cycles[index+4][0] +" in Fetch Cycle")
                del instr_cycles[index+4][1]
        except:
            return False

    return False

def hazards_handle(instr_cycles, asm, instr):
    foward_path = "no forward needed"
    try:    
        asm[instr-1]
    except:
        return
    DIC = len(instr_cycles) - 1

    current = asm[instr]   
    current = current.replace("\n","") # Removes extra chars
    current = current.replace("$","")
    current = current.replace(" ","")
    current_name = instr_cycles[DIC][0]
    current = current.replace(current_name,"")
    current = current.split(",")

    prev = asm[instr-1] 
    prev = prev.replace("\n","") # Removes extra chars
    prev = prev.replace("$","")
    prev = prev.replace(" ","")
    prev_name = instr_cycles[DIC-1][0]
    prev = prev.replace(prev_name,"")
    prev = prev.split(",")

    norm_instri = ["addi", "ori", "sll"]
    norm_instrr = ["xor", "addu", "sltu", "slt", "sub"]
    branch = ["beq", "bne"]

    if prev_name in norm_instrr or prev_name in norm_instri:
        prd = int(prev[1])
        if current_name in norm_instri:
            rs = int(current[1])
            if rs == prd:
                instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcA"
                return
            if current_name in norm_instrr:
                rt = int(current[2])
                rs = int(current[1])
                if rs == prd:
                    instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcA"
                if rt == prd:
                    instr_cycles[DIC-1][3][1].append("ALUoutM --> ALUSrcB")
        

    '''
    elif current_name in norm_instrr:
        current = current.replace(current_name,"")
        current = current.split(",")
        rs = regval[int(current[1])]
        rt = regval[int(current[2])]
    elif current_name in branch:
        current = current.replace(current_name,"")
        current = current.split(",")
        rs = regval[int(current[1])]
        rt = regval[int(current[2])]
    elif current_name == "lw":
        current = current.replace(current_name,"")
        current = current.split(",")
        rd = regval[int(current[0])]
   
    return forward_path

    #NEED:
    #whether any stage contains a bubble, due to stall or
    #flush, used to solve which hazard, hazard information (which forwarding path is
    #being activated: 
    #cycle count, statistics of delays
    #(caused by each category), statistics of forward-path usage. 
    '''


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
        not_Done = True
        while lineCount < len(Instructions):
            
            line = Instructions[lineCount]

            

            if(debugMode == 1 and loop == 1):
                while(True):
                    user_pause = input("Press enter to continue or q to quit diagnosis mode:\n\n")
                    if(user_pause == ""):
                        print('MIPS Instruction: ' + line + '\n')
                        break
                    
                    if(user_pause == "q"):
                        print("Continuing in non-stop mode\n")
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
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True

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
                    instr_cycles.append(["addi", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("addi", 4, PC)


            elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True
                
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
                    instr_cycles.append(["xor", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("xor", 4, PC)
                PC += 4


            #addu
            elif(line[0:4] == "addu"): 
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True
                
                line = line.replace("addu","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["addu", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("addu", 4, PC)

                regval[int(line[0])] = (abs(regval[int(line[1])]) + abs(regval[int(line[2])])) & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                

            elif(line[0:4] == "sltu"):
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True

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
                    instr_cycles.append(["sltu", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("sltu", 4, PC) 

                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')


            elif(line[0:3] == "slt"):
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True

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
                    instr_cycles.append(["sltu", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("slt", 4, PC)

                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')


            elif(line[0:3] == "ori"):
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True

                line = line.replace("ori", "")
                line = line.split(",")
                imm = get_imm(line,2)
                PC = PC + 4
                regval[int(line[0])] = (imm | regval[int(line[1])]) & 0xFFFFFFFF
                if(loop == 0):
                    instr_cycles.append(["ori", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("ori", 4, PC)
                if(debugMode != 1):
                    DIC += 1
                f.write('Operation: $' + line[0] + '= $' + line[1] + " | "  + line[2] + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + '=' + line[2] + '\n')

            #bne
            elif(line[0:3] == "bne"): # BNE
                line = line.replace("bne","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["bne", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("bne", 3, PC)

                if(regval[int(line[0])]!=regval[int(line[1])]):
                    
                    if (debugMode == 1 and loop == 1):
                        if not_Done:
                            not_Done = cycle_tracker(instr_cycles, DIC)
                            continue
                        DIC += 1
                        not_Done = True

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
                    instr_cycles.append(["beq", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("beq", 3, PC)

                if(regval[int(line[0])]==regval[int(line[1])]):
                    
                    if (debugMode == 1 and loop == 1):
                        if not_Done:
                            not_Done = cycle_tracker(instr_cycles, DIC)
                            continue
                        DIC += 1
                        not_Done = True

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
                                break
                        continue
                                

                f.write('No Registers have changed. \n')



            elif(line[0:2] =="lw" and not('lw_loop' in line)):
                
                if (debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True
                
                line= line.replace("lw","")
                line= line.replace("(",",")
                line= line.replace(")","")
                line= line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["lw", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
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

            elif(line[0:2] =="sw" and not('sw_' in line)):
                
                if (debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True

                line= line.replace("sw","")
                line= line.replace("(",",")
                line= line.replace(")","")
                line= line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sw", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("sw", 4, PC)
                imm = get_imm(line, 1)
                MEM_val = regval[int(line[0])] 
                MEM[ regval[int(line[2])] + imm ] = MEM_val
                f.write('Operation: MEM[ $' + line[2] + ' + ' + line[1] + ' ] = $' + line[0] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: None\n')

            elif(line[0:3] =="sub"):
                
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        continue
                    DIC += 1
                    not_Done = True

                line = line.replace("sub","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sub", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    stats.log("sub", 4, PC)
                regval[int(line[0])] = (regval[int(line[1])] - regval[int(line[2])])  & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

            elif(line[0:3] == "sll"): 
                
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        #hazards_handle(instr_cycles, DIC, asm, instr, regval)
                        continue
                    DIC += 1
                    not_Done = True

                line = line.replace("sll","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sll", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    breakpoint()
                    hazards_handle(instr_cycles, Instructions, lineCount)
                    stats.log("sll", 4, PC)
                imm = get_imm(line,2)
                regval[int(line[0])] = (regval[int(line[1])] << imm) & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' << ' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')


            lineCount += 1

    PC = (len(Instructions)-len(labelName)) * 4 
    tot_cycles = DIC + 4

    final_print(regval,MEM, PC, DIC)    
    print("\n\n**************************************** FINAL CYCLE INFO ****************************************\n")
    print("IDEAL PIPLINE: ", tot_cycles)

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