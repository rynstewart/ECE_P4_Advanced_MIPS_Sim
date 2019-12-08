
import time

class Statistics_Pipeine:
    def __init__(self, debugMode):
        self.I= ""               #current instruction being executed
        self.name = ""           # name of the instruction
        self.cycle = 0           # Total cycles in simulation
        self.NOPcount = 0        #keeps track of NOP
        self.branch_taken_stall = 0      #keeps track of flush
        self.lw_use_stall = 0      #keeps track of stall count
        self.compute_branch_stall = 0      #keeps track of stall count
        self.lw_branch_stall = 0
        self.ALUoutM_ALUSrcB = 0
        self.ALUoutM_ALUSrcA = 0
        self.ALUoutM_EqualD = 0
        self.ALUoutM_WriteDataE = 0
        self.ResultW_ALUSrcA = 0
        self.ResultW_ALUSrcB = 0
        self.ResultW_EqualD = 0
        self.ResultW_WriteDataE = 0
        self.debugMode = debugMode
    
    def log_forward(self, cycle, ALUoutM_ALUSrcB, ALUoutM_ALUSrcA, ALUoutM_EqualD, ALUoutM_WriteDataE, ResultW_ALUSrcA, ResultW_ALUSrcB, ResultW_EqualD,ResultW_WriteDataE):
        self.cycle +=  cycle
        self.ALUoutM_ALUSrcB += ALUoutM_ALUSrcB
        self.ALUoutM_ALUSrcA += ALUoutM_ALUSrcA
        self.ALUoutM_EqualD += ALUoutM_EqualD
        self.ALUoutM_WriteDataE += ALUoutM_WriteDataE
        self.ResultW_ALUSrcA += ResultW_ALUSrcA
        self.ResultW_ALUSrcB += ResultW_ALUSrcB
        self.ResultW_EqualD += ResultW_EqualD
        self.ResultW_WriteDataE += ResultW_WriteDataE
        
    def log_stall(self, branch_taken_stall, lw_use_stall, compute_branch_stall, lw_branch_stall):
        self.branch_taken_stall += branch_taken_stall
        self.lw_use_stall += lw_use_stall
        self.compute_branch_stall += compute_branch_stall
        self.lw_branch_stall += lw_branch_stall

    def exitSim(self):
        print("***Finished simulation***")
        print("Total # of cycles: " + str(self.cycle))
        print("\nDelay Statistics:")
        print("                 " + str(self.branch_taken_stall) + " taken branch stalls" )  
        print("                 " + str(self.lw_use_stall) + " lw use stall" )
        print("                 " + str(self.compute_branch_stall) + " compute branch stall" )
        print("                 " + str(self.lw_branch_stall) + " lw then branch stall" )
        print("\n Forwarding Path Statistics:")
        print("                            " + str(self.ALUoutM_ALUSrcA) + " ALUOutM ‐> SrcAE" )  
        print("                            " + str(self.ALUoutM_ALUSrcB) + " ALUOutM ‐> SrcBE" )
        print("                            " + str(self.ALUoutM_EqualD) + " ALUOutM ‐> WriteDataE" )
        print("                            " + str(self.ALUoutM_WriteDataE) + " ALUOutM ‐> EqualD" )
        print("                            " + str(self.ResultW_ALUSrcA) + " ResultW ‐> SrcAE" )  
        print("                            " + str(self.ResultW_ALUSrcB) + " ResultW ‐> SrcBE" )
        print("                            " + str(self.ResultW_EqualD) + " ResultW ‐> WriteDataE" )
        print("                            " + str(self.ResultW_WriteDataE) + " ResultW ‐> EqualD" )

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
#############################################################################
# this is the main cycle information tracker, it looks at the list 
# instr_cycles to see the first entry for which cycle an instruction is on
# then removes that cycle. It repeats this process for the next instructins
# as well. True is returned if an instruction still has cycles, false once
# the list has no more cycles.
#############################################################################
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
            print("\n\tForwarding Path(s):")
            for k in range(1,len(instr_cycles[index][1]),1):
                print("\n\t" + instr_cycles[index][1][k])
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
                    for k in range(1,len(instr_cycles[index+1][1]),1):
                        print("\n\t" + instr_cycles[index+1][1][k])
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
            for k in range(1,len(instr_cycles[index][1]),1):
                print("\n\t" + instr_cycles[index][1][k])
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
                    for k in range(1,len(instr_cycles[index+2][1]),1):
                        print("\n\t" + instr_cycles[index+2][1][k])
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
#############################################################################
# This function handles hazard detection. If a hazard is detected it modifies
# the inst_cycles list to include a fowarding path in the cycle
# for the cases that a forwarding path is not enough to avoid a hazard this
# function inserts an NOP to stall in the asn list
#############################################################################
def hazards_handle(stats, instr_cycles, asm, instr, labelIndex,labelName, labelAddr):


    NOP = "addi $23, $23, 0"
    DIC = len(instr_cycles) - 1
    try:    
        instr_cycles[DIC-1]
    except:
        return instr

    i = 1
    if asm[instr-i] == NOP:
        i += 1
        #breakpoint()
    if ":" in asm[instr-i] or "#" in asm[instr-i]:
        i = 2
        if ":" in asm[instr-i] or "#" in asm[instr-i]:
            i = 3
    if instr - i < 0:
        return instr


    current = asm[instr]   
    current = current.replace("\n","") # Removes extra chars
    current = current.replace("$","")
    current = current.replace(" ","")
    current_name = instr_cycles[DIC][0]
    current = current.replace(current_name,"")
    current = current.replace("(",",")
    current = current.replace(")","")
    current = current.split(",")

    prev = asm[instr-i] 
    prev = prev.replace("\n","") # Removes extra chars
    prev = prev.replace("$","")
    prev = prev.replace(" ","")
    prev_name = instr_cycles[DIC-1][0]
    prev = prev.replace(prev_name,"")
    prev = prev.replace("(",",")
    prev = prev.replace(")","")
    prev = prev.split(",")


    norm_instri = ["addi", "ori", "sll"]
    norm_instrr = ["xor", "addu", "sltu", "slt", "sub"]
    branch = ["beq", "bne"]

    if prev_name in norm_instrr or prev_name in norm_instri:
        prd = int(prev[0])
        if current_name in norm_instri:
            rs = int(current[1])
            if rs == prd:
                stats.log_forward(0,0,1,0,0,0,0,0,0)
                instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcA"

        if current_name in norm_instrr:
            rt = int(current[2])
            rs = int(current[1])
            if rs == prd:
                stats.log_forward(0,0,1,0,0,0,0,0,0)
                if instr_cycles[DIC-1][3][1] == "":
                    instr_cycles[DIC-1][3].append("ALUoutM --> ALUSrcA")
                else:    
                    instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcA"
            if rt == prd:
                stats.log_forward(0,1,0,0,0,0,0,0,0)
                if instr_cycles[DIC-1][3][1] == "":
                    instr_cycles[DIC-1][3].append("ALUoutM --> ALUSrcB")
                else:    
                    instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcB"

    if prev_name in norm_instrr or prev_name in norm_instri:
        prd = int(prev[0])
        if current_name == "sw":
            rt = int(current[2])
            if rt == prd:
                stats.log_forward(0,1,0,0,0,0,0,0,0)
                instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcB"


    if prev_name in norm_instrr or prev_name in norm_instri:
        prd = int(prev[0])
        if current_name in branch:
            rt = int(current[1])
            rs = int(current[0])
            if rs == prd or rt == prd:
                stats.log_forward(0,0,0,1,0,0,0,0,0)
                instr_cycles[DIC-1][3][1] = "ALUoutM --> EqualD"
                stats.log_stall(0,0,1,0)
                if asm[instr-1] != NOP and asm[instr-(i-1)] != NOP:
                    asm.insert(instr, NOP)
                    labelIndex.clear()
                    labelName.clear()
                    labelAddr.clear()                            
                    saveJumpLabel(asm,labelIndex,labelName, labelAddr)
                    return instr-1


    if prev_name in norm_instrr or prev_name in norm_instri:
        prd = int(prev[0])
        if current_name == "lw":
            rt = int(current[2])
            if rt == prd:
                stats.log_forward(0,1,0,0,0,0,0,0,0)
                instr_cycles[DIC-1][3][1] = "ALUoutM --> ALUSrcB"


    if prev_name == "lw":
        prd = int(prev[0])
        if current_name in branch:
            rt = int(current[2])
            rs = int(current[1])
            if rs == prd or rt == prd:   
                stats.log_forward(0,0,0,0,0,0,0,1,0)
                instr_cycles[DIC - 1][5][1] = "ResultW --> EqualD"
                stats.log_stall(0,0,0,2)
                if asm[instr-1] != NOP and asm[instr-(i-1)] != NOP:
                    asm.insert(instr, NOP)
                    asm.insert(instr, NOP)
                    labelIndex.clear()
                    labelName.clear()
                    labelAddr.clear()                            
                    saveJumpLabel(asm,labelIndex,labelName, labelAddr)
                    return instr-1


    if prev_name in "lw":
        prd = int(prev[0])
        if current_name in norm_instrr or prev_name in norm_instri:
            rt = int(current[2])
            rs = int(current[1])
            if rs == prd:
                stats.log_forward(0,0,0,0,0,1,0,0,0)
                if instr_cycles[DIC-1][3][1] == "":
                    instr_cycles[DIC-1][5].append("ResultW --> ALUSrcA")
                else:    
                    instr_cycles[DIC-1][5][1] = "ResultW --> ALUSrcA"
            if rt == prd:
                stats.log_forward(0,0,0,0,0,0,1,0,0)
                if instr_cycles[DIC-1][5][1] == "":
                    instr_cycles[DIC-1][5].append("ResultW --> ALUSrcB")
                else:    
                    instr_cycles[DIC-1][5][1] = "ResultW --> ALUSrcB"       
            if rt == prd or rs == prd:
                stats.log_stall(0,1,0,0)
                if asm[instr-1] != NOP and asm[instr-(i-1)] != NOP:
                    asm.insert(instr, NOP)
                    labelIndex.clear()
                    labelName.clear()
                    labelAddr.clear()                            
                    saveJumpLabel(asm,labelIndex,labelName, labelAddr)
                    return instr-1
    
    return instr
            

def simulate(Instructions, f, debugMode):
    labelIndex = []
    labelName = []
    labelAddr = []
    regName = []
    regNameInit(regName)
    LO = 24
    HI = 25
    stats = Statistics_Pipeine(debugMode)
    NOP = "addi $23, $23, 0"
    
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
        if loop == 1 and debugMode == 2:
            tot_cycles = len(instr_cycles)+5
            stats.log_forward(tot_cycles,0,0,0,0,0,0,0,0)
        while lineCount < len(Instructions):
            
            line = Instructions[lineCount]

            

            if(debugMode == 1 and loop == 1):
                while(True):
                    if not_Done:
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
                    break

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
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    if(int(line[0])==23):
                        instr_cycles.append(["addi-NOP INSTRUCTION", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    else:
                        instr_cycles.append(["addi", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                        lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)


            elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)


            #addu
            elif(line[0:4] == "addu"): 
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
                        continue
                    DIC += 1
                    not_Done = True
                
                line = line.replace("addu","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["addu", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)

                regval[int(line[0])] = (abs(regval[int(line[1])]) + abs(regval[int(line[2])])) & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
                

            elif(line[0:4] == "sltu"):
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)

                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')


            elif(line[0:3] == "slt"):
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)

                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')


            elif(line[0:3] == "ori"):
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)
                if(debugMode != 1):
                    DIC += 1
                f.write('Operation: $' + line[0] + '= $' + line[1] + " | "  + line[2] + '\n'),
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + '=' + line[2] + '\n')

            #bne
            elif(line[0:3] == "bne"): # BNE
                if (debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
                        continue
                    DIC += 1
                    not_Done = True
                line = line.replace("bne","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["bne", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)


                if(regval[int(line[0])]!=regval[int(line[1])]):
                    stats.log_stall(1, 0, 0, 0)
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
                                break
                        if Instructions[lineCount+1] != NOP:
                            Instructions.insert(lineCount+1, NOP)  
                            labelIndex.clear()
                            labelName.clear()
                            labelAddr.clear()    
                            saveJumpLabel(Instructions,labelIndex,labelName, labelAddr)   
                        f.write('No Registers have changed. \n')
                    continue

                f.write('No Registers have changed. \n')
                


            #beq
            elif(line[0:3] == "beq"): # Beq
                if (debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
                        continue
                    DIC += 1
                    not_Done = True
                line = line.replace("beq","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["beq", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)

                if(regval[int(line[0])]==regval[int(line[1])]):
                    stats.log_stall(1, 0, 0, 0)
                    if(line[2].isdigit()): # First,test to see if it's a label or a integer
                        PC = int(line[2])*4
                        lineCount = int(line[2])
                        f.write('PC is now at ' + str(line[2]) + '\n')
                        f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                        f.write('No Registers have changed. \n')
                    else: # Jumping to label
                        for i in range(len(labelName)):
                            if(labelName[i] == line[2]):
                                PC = labelAddr[i]
                                lineCount = labelIndex[i]
                                f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                                f.write('No Registers have changed. \n')
                                break
                        if Instructions[lineCount+1] != NOP:
                            Instructions.insert(lineCount+1, NOP)
                            labelIndex.clear()
                            labelName.clear()
                            labelAddr.clear()                            
                            saveJumpLabel(Instructions,labelIndex,labelName, labelAddr)
                    continue
                                

                f.write('No Registers have changed. \n')



            elif(line[0:2] =="lw" and not('lw_loop' in line)):
                
                if (debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)

                rs = regval[int(line[2])]
                imm = get_imm(line, 1)                    

                MEM_val = MEM[ rs + imm ] & 0xFFFFFFFF
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
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
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
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)
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
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
                        continue
                    DIC += 1
                    not_Done = True

                line = line.replace("sub","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sub", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)
                regval[int(line[0])] = (regval[int(line[1])] - regval[int(line[2])])  & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

            elif(line[0:3] == "sll"): 
                
                if(debugMode == 1 and loop == 1):
                    if not_Done:
                        not_Done = cycle_tracker(instr_cycles, DIC)
                        breakpoint()
                        stats.log_forward(1,0,0,0,0,0,0,0,0)
                        continue
                    DIC += 1
                    not_Done = True

                line = line.replace("sll","")
                line = line.split(",")
                if(debugMode != 1):
                    DIC += 1
                if(loop == 0):
                    instr_cycles.append(["sll", ["Fetch",""], ["Decode",""], ["Execute",""], ["Memory", ""], ["Write Back", ""]])
                    lineCount = hazards_handle(stats, instr_cycles, Instructions, lineCount,labelIndex,labelName, labelAddr)
                imm = get_imm(line,2)
                regval[int(line[0])] = (regval[int(line[1])] << imm) & 0xFFFFFFFF
                f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' << ' + line[2] + '; ' + '\n')
                f.write('PC is now at ' + str(PC) + '\n')
                f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')


            lineCount += 1

    PC = (len(Instructions)-len(labelName)) * 4 

    final_print(regval,MEM, PC, DIC)    
    print("\n\n**************************************** FINAL CYCLE INFO ****************************************\n")
    print("PIPLINED CYCLES: ", stats.cycle)
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