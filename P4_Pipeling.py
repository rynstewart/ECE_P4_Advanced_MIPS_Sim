import time
import math

def update_LRU(LRU, val): #this function takes the LRU list and the way that is being used now and updating the list
    if val in LRU:
        LRU.insert(0, LRU.pop(LRU.index(val)))
    else:
        LRU.pop()
        LRU.insert(0, val)
    return LRU

def get_least_recently_used(LRU): #this function find the value int LRU that was used least recently
    for i in range(8):
        if (LRU[-(i + 1)] != -1):
            return LRU[-(i + 1)]

def cache_simulator(user_input, mem_addr,tag,valid,cache,MEM,Hits,Misses,ways_tag,LRU):

    print("*****Cache Simulator being accessed*****\n")

    if (user_input=='a'):

        address="{0:032b}".format(int(mem_addr, 16))                     #get mem addr
        print("Memory address: "+ address)
        set_index= int(address[26:28],2)                                    #get set index
        valid_bit= valid[set_index]                                         #check valid bit
        tag_bits= address[0:26]                                             #get tag bits
        addr_from = hex(int(address[0:32],2) & int("FFFFFFF0",16))          #first address to bring from memory
        addr_to = hex(int(address[0:32],2) | int("F",16))                   #last address to bring from memory

        print("Looking at set/block : "+str(set_index))
        print("Way information: ")
        print("valid bit: " + str(valid_bit))
        print("tag bit:" + str(tag_bits))

        if (valid_bit== 0):                                                     #empty block(miss)
            Misses+=1
            valid[set_index]=1                                                  #change the valid bit to 1
            HorM="Miss"
            tag[set_index]= tag_bits                                            #update the tag of the set

        else:                                                                   #valid bit is 1, occupied block
            if(tag[set_index]== tag_bits):                                      #tags match(hit)
                Hits+=1
                HorM="Hit"
            else:                                                                #miss due to occupied and new tag
                Misses+=1
                HorM="Miss"
                tag[set_index]= tag_bits                                           #update tag for set

        for i in range(16):                                                 #updating Cache
            cache[(set_index*16)+i]= hex(MEM[(int(addr_from,16) +i)])

        print("\nHit or Miss: "+ HorM)
        print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
        print("Bringing into block " + str(set_index) + " of the cache\n")


    elif(user_input=='b'):

        hitway=0
        hit_stat=0
        valid_way=0
        valid_bit=0

        address="{0:032b}".format(int(mem_addr, 16))             #get the address
        print("Memory address: "+ address)
        tag_bits= address[0:29]                                     #get the tag bits of this address
        addr_from = hex(int(address[0:32],2) & int("FFFFFFF8",16))  #first address to bring from memory
        addr_to = hex(int(address[0:32],2) | int("7",16))           #last address to bring from memory

        for i in range(8):                              #check to see if the tag already exist for one of the ways
            if (ways_tag[i] == tag_bits):               #if the tag exists
                hitway=i                                #save the index of this way which indicates a hit
                hit_stat=1                              #change stat of hit to 1
                break
        valid_bit = 1
        for i in range(8):                              #check if any of the ways is empty
            if (valid[i]==0):                           #if so save the index of this way
                valid_way=i
                valid_bit=0                             #valid bit of the way is zero
                break

        if(hit_stat==1):                                #hit since the tags are matching
            print("Looking at set/block : "+str(hitway))
            Hits+=1
            LRU = update_LRU(LRU, hitway)               #update LRU since we are using the way
            hit_stat=0                                  #reset
            valid_bit=1
            HorM= "Hit"
            cache_block=hitway
            block_index= hitway
        else:
            Misses+=1
            if (valid_bit==0):                          #if the way is empty
                print("Looking at set/block : "+str(valid_way))
                ways_tag[valid_way]= tag_bits           #update the tag of the way
                LRU = update_LRU(LRU, valid_way)        #update LRU
                valid[valid_way]=1                      #update valid array
                block_index= valid_way
                cache_block=valid_way
            else:                                           #if the way is not empty but the tag does not match
                temp_index = get_least_recently_used(LRU)   #get the least recent used way
                ways_tag[temp_index]= tag_bits              #update the tag
                LRU = update_LRU(LRU, temp_index)           #update LRU
                print("Looking at set/block : "+str(temp_index))
                block_index= temp_index
                cache_block=temp_index

            HorM="Miss"


        for i in range(8):                                               #updating Cache
            cache[(block_index*8)+i]= hex(MEM[(int(addr_from,16) +i)] )     #will add mem[] to load from memory

        print("Way information: ")
        print("valid bit: " + str(valid_bit))
        print("tag bit:" + str(tag_bits))
        print("\nHit or Miss: "+ HorM)
        print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
        print("Bringing into block " + str(cache_block) + " of the cache\n")


    elif(user_input=='c'): #updating cache needs to be fixed

         hit_stat = 0
         valid_way = 0
         valid_bit = 0
         hitway = 0

         address="{0:032b}".format(int(mem_addr, 16))
         print("Memory address: "+ address)
         tag_bits= address[0:27]
         set_index= int(address[27:29],2)
         addr_from = hex(int(address[0:32],2) & int("FFFFFFF8",16))  #first address to bring from memory
         addr_to = hex(int(address[0:32],2) | int("7",16))           #last address to bring from memory

                                                        #in this case we will check four different lists for each sits
         for i in range(2):                             #check to see if the tag already exist for one of the ways
             if (ways_tag[set_index][i] == tag_bits):             #if the tag exists
                 hitway=i                                #save the index of this way which indicates a hit
                 hit_stat=1                              #change stat of hit to 1
                 break
         valid_bit = 1
         for i in range(2):                              #check if any of the ways is empty
             if (valid[set_index][i]==0):                           #if so save the index of this way
                 valid_way=i
                 valid_bit=0                             #valid bit of the way is zero
                 break

         if(hit_stat==1):                                #hit since the tags are matching
             Hits+=1
             LRU[set_index] = update_LRU(LRU[set_index], hitway)               #update LRU since we are using the way
             hit_stat=0                                  #reset
             valid_bit=1
             HorM= "Hit"
             print_way=hitway

         else:
             Misses+=1
             if (valid_bit==0):                          #if the way is empty
                 ways_tag[set_index][valid_way]= tag_bits           #update the tag of the way
                 LRU[set_index] = update_LRU(LRU[set_index], valid_way)        #update LRU
                 valid[set_index][valid_way]=1                      #update valid array
                 print_way= valid_way

             else:                                           #if the way is not empty but the tag does not match
                 temp_index = get_least_recently_used(LRU[set_index])   #get the least recent used way
                 ways_tag[set_index][temp_index]= tag_bits              #update the tag
                 LRU[set_index] = update_LRU(LRU[set_index], temp_index)           #update LRU
                 print_way= temp_index
             HorM="Miss"

         if(set_index==0):
             for i in range(8):                                               #updating Cache
                 cache[(print_way*8)+i]= hex(MEM[(int(addr_from,16) +i)])     #will add mem[] to load from memory
             cache_block=print_way*1

         elif(set_index==1):
             for i in range(8):                                               #updating Cache
                 cache[((print_way*8)+16)+i]= hex(MEM[(int(addr_from,16) +i)])     #will add mem[] to load from memory
             cache_block= (print_way*1)+2

         elif(set_index==2):
             for i in range(8):                                               #updating Cache
                 cache[((print_way*8)+32)+i]= hex(MEM[(int(addr_from,16) +i)])     #will add mem[] to load from memory
             cache_block= (print_way*1)+4

         elif(set_index==3):
             for i in range(8):                                               #updating Cache
                 cache[((print_way*8)+48)+i]= hex(MEM[(int(addr_from,16) +i)])       #will add mem[] to load from memory
             cache_block= (print_way*1)+6



         print("Looking at set: "+str(set_index)+ " ,Way: "+str(print_way))
         print("Way information: ")
         print("valid bit: " + str(valid_bit))
         print("tag bit:" + str(tag_bits))
         print("\nHit or Miss: "+ HorM)
         print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
         print("Bringing into block " + str(cache_block) + " of the cache\n")


         print("\n")

    elif(user_input=='d'):

        hit_stat = 0
        valid_way = 0
        valid_bit = 0
        hitway = 0
        cache_block=0

        address="{0:032b}".format(int(mem_addr, 16))
        print("Memory address: "+ address)
        tag_bits= address[0:28]
        set_index= int(address[28:29],2)
        addr_from = hex(int(address[0:32],2) & int("FFFFFFF8",16))  #first address to bring from memory
        addr_to = hex(int(address[0:32],2) | int("7",16))           #last address to bring from memory

                                                    #in this case we will check four different lists for each sits
        for i in range(4):                             #check to see if the tag already exist for one of the ways

            if (ways_tag[set_index][i] == tag_bits):             #if the tag exists
                hitway=i                                #save the index of this way which indicates a hit
                hit_stat=1                              #change stat of hit to 1
                break
        valid_bit = 1

        for i in range(4):                              #check if any of the ways is empty
            if (valid[set_index][i]==0):                           #if so save the index of this way
                valid_way=i
                valid_bit=0                             #valid bit of the way is zero
                break

        if(hit_stat==1):                                #hit since the tags are matching
            Hits+=1
            LRU[set_index] = update_LRU(LRU[set_index], hitway)               #update LRU since we are using the way
            hit_stat=0                                  #reset
            valid_bit=1
            HorM= "Hit"
            print_way=hitway

        else:
            Misses+=1
            if (valid_bit==0):                          #if the way is empty
                ways_tag[set_index][valid_way]= tag_bits           #update the tag of the way
                LRU[set_index] = update_LRU(LRU[set_index], valid_way)        #update LRU
                valid[set_index][valid_way]=1                      #update valid array
                print_way= valid_way

            else:                                           #if the way is not empty but the tag does not match

                temp_index = get_least_recently_used(LRU[set_index])   #get the least recent used way
                ways_tag[set_index][temp_index]= tag_bits              #update the tag
                LRU[set_index] = update_LRU(LRU[set_index], temp_index)           #update LRU
                print_way= temp_index
            HorM="Miss"

        if(set_index==0):
            for i in range(8):                                               #updating Cache
                cache[(print_way*8)+i]= hex(MEM[(int(addr_from,16) +i)])     #will add mem[] to load from memory
            cache_block=print_way*1

        elif(set_index==1):
            for i in range(8):           #updating Cache
                cache[((print_way*8)+32)+i]= hex(MEM[(int(addr_from,16) +i)])    #will add mem[] to load from memory
            cache_block= (print_way*1)+4




        print("Looking at set: "+str(set_index)+ " ,Way: "+str(print_way))
        print("Way information: ")
        print("valid bit: " + str(valid_bit))
        print("tag bit:" + str(tag_bits))
        print("\nHit or Miss: "+ HorM)
        print("Memory accessed: M[ " + addr_from + " - " + addr_to+" ]" )
        print("Bringing into block " + str(cache_block) + " of the cache\n")


        print("\n")

    return Hits,Misses

def simulate_cache(Instructions, f, debugMode,user_input,tag,valid,cache,ways_tag,LRU):

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
    final_hits=0
    final_misses=0

    saveJumpLabel(Instructions,labelIndex,labelName, labelAddr)


    f = open(f,"w+")
    lineCount = 0
    i = 0


    while lineCount < len(Instructions):

        line = Instructions[lineCount]



        f.write('------------------------------ \n')
        if(not(':' in line)):
            f.write('MIPS Instruction: ' + line + '\n')
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0


        if(line[0:4] == "addi"): # ADDI, $t = $s + imm; advance_pc (4); addi $t, $s, imm
            line = line.replace("addi","")
            line = line.split(",")
            imm = get_imm(line,2)
            regval[int(line[0])] = (regval[int(line[1])] + imm)  & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            DIC += 1
            PC += 4

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
            DIC += 1

            PC += 4

        elif(line[0:4] == "addu"):

            line = line.replace("addu","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("addu", 4, PC)

            regval[int(line[0])] = (abs(regval[int(line[1])]) + abs(regval[int(line[2])])) & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:4] == "sltu"):

            line = line.replace("sltu","")
            line = line.split(",")
            if(abs(regval[int(line[1])]) < abs(regval[int(line[2])])):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            DIC += 1
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')

        elif(line[0:3] == "slt"):

            line = line.replace("slt","")
            line = line.split(",")
            if(regval[int(line[1])] < regval[int(line[2])]):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            DIC += 1

            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')

        elif(line[0:3] == "ori"):
            line = line.replace("ori", "")
            line = line.split(",")
            imm = get_imm(line,2)
            PC = PC + 4
            DIC += 1
            regval[int(line[0])] = (imm | regval[int(line[1])]) & 0xFFFFFFFF

            f.write('Operation: $' + line[0] + '= $' + line[1] + " | "  + line[2] + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + '=' + line[2] + '\n')

        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")
            DIC += 1

            if(regval[int(line[0])]!=regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = int(line[2])*4
                    lineCount = int(line[2])
                    f.write('PC is now at ' + str(line[2]) + '\n')
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            if debugMode != 1:
                                stats.log("bne", 3, PC)
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')
                            break
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')

        elif(line[0:3] == "beq"): # Beq
            line = line.replace("beq","")
            line = line.split(",")
            DIC += 1

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

        elif(line[0:2] =="lw" and not('lw_loop' in line)):
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

            line= line.replace("lw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")

            PC = PC + 4
            DIC += 1
            imm = get_imm(line, 1)
            MEM_val = MEM[ regval[int(line[2])] + imm ] & 0xFFFFFFFF
            cache_addr= hex(regval[int(line[2])] + imm)

            final_hits,final_misses=cache_simulator(user_input,cache_addr,tag,valid,cache,MEM,final_hits,final_misses,ways_tag,LRU)

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

            line= line.replace("sw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")
            PC = PC + 4
            DIC += 1
            imm = get_imm(line, 1)
            MEM_val = regval[int(line[0])]
            cache_addr= hex(regval[int(line[2])] + imm)
            final_hits,final_misses=cache_simulator(user_input,cache_addr,tag,valid,cache,MEM,final_hits,final_misses,ways_tag,LRU)
            MEM[ regval[int(line[2])] + imm ] = MEM_val
            f.write('Operation: MEM[ $' + line[2] + ' + ' + line[1] + ' ] = $' + line[0] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: None\n')


        elif(line[0:3] =="sub"):

            line = line.replace("sub","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1

            regval[int(line[0])] = (regval[int(line[1])] - regval[int(line[2])])  & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')


        elif(line[0:3] == "sll"):

            line = line.replace("sll","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            imm = get_imm(line,2)
            regval[int(line[0])] = (regval[int(line[1])] << imm) & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' << ' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        lineCount += 1

    PC = (len(Instructions)-len(labelName)) * 4

    printarray = [[0 for i in range(16)] for j in range(4)]

    print("\n\n**************************************** FINAL CACHE RESULTS ****************************************\n")


    for i in range(16):
        printarray[0][i]=cache[i]
        printarray[1][i]=cache[i+16]
        printarray[2][i]=cache[i+32]
        printarray[3][i]=cache[i+48]


    print("Total hits: " + str(final_hits))
    print("Total misses: " + str(final_misses))
    print("Hit rate: " + str(final_hits/(final_misses+final_hits)))
    print("\nFinal Cache content: \n"+ str(printarray[0])+"\n"+str(printarray[1])+"\n"+str(printarray[2])+"\n"+str(printarray[3]))
    print("\n\n")

    final_print(regval,MEM, PC, DIC)





    f.close()


def multi(MemtoReg, MemWrite, Branch, ALUSrcA, ALUSrcB, RegDst, RegWrite):

    print("MemtoReg is now " + MemtoReg)
    print("MemWrite is now " + MemWrite)
    print("Branch is now " + Branch)
    print("ALUSrcA is now " + ALUSrcA)
    print("ALUSrcB is now " + ALUSrcB)
    print("RegDst is now " + RegDst)
    print("RegWrite is now " + RegWrite + '\n')

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

        #if "$8" in line:
            #breakpoint()

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
            
            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "10", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "0", "1")
                    i = 0
                    stats.log("addi", 4, PC)

            line = line.replace("addi","")
            line = line.split(",")
            imm = get_imm(line,2)
            regval[int(line[0])] = (regval[int(line[1])] + imm)  & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + line[2] + '; ' + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            DIC += 1
            PC += 4
            if debugMode != 1:
                stats.log("addi", 4, PC)


        elif(line[0:3] == "xor"): #$d = $s ^ $t; advance_pc (4); xor $d, $s, $t
            
            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "0", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "1", "1")
                    i = 0
                    stats.log("xor", 4, PC)

            line = line.replace("xor","")
            line = line.split(",")
            x = regval[int(line[1])]
            y = regval[int(line[2])]
            z = int(x)^int(y)
            regval[int(line[0])] = z & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' ^ $' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')
            DIC += 1

            PC += 4
            if debugMode != 1:
                stats.log("xor", 4, PC)


        #addu
        elif(line[0:4] == "addu"): 

            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "0", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "1", "1")
                    i = 0
                    stats.log("addu", 4, PC)

            line = line.replace("addu","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("addu", 4, PC)

            regval[int(line[0])] = (abs(regval[int(line[1])]) + abs(regval[int(line[2])])) & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' + ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')

        elif(line[0:4] == "sltu"):

            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "0", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "1", "1")
                    i = 0
                    stats.log("sltu", 4, PC)

            line = line.replace("sltu","")
            line = line.split(",")
            if(abs(regval[int(line[1])]) < abs(regval[int(line[2])])):
                regval[int(line[0])] = 1
            else:
                regval[int(line[0])] = 0

            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("sltu", 4, PC)

            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' < $' + line[2] + '? 1 : 0 ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[ int(line[0]) ]) + '\n')


        elif(line[0:3] == "slt"):

            if(debugMode == 1):

                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "0", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "1", "1")
                    i = 0
                    stats.log("slt", 4, PC)

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

        elif(line[0:3] == "ori"):
           
            if(debugMode == 1):
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    multi("X", "0", "0", "1", "10", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n')
                    multi("0", "0", "0", "X", "X", "0", "1")
                    i = 0
                    stats.log("ori", 4, PC)

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

        #bne
        elif(line[0:3] == "bne"): # BNE
            line = line.replace("bne","")
            line = line.split(",")

            if (debugMode == 1):
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    multi("X", "0", "1", "1", "0", "X", "0")
                    i = 0
                    stats.log("bne", 3, PC)
            DIC += 1

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
                            break    
                f.write('No Registers have changed. \n')
                continue
            f.write('No Registers have changed. \n')


        #beq
        elif(line[0:3] == "beq"): # Beq
            line = line.replace("beq","")
            line = line.split(",")

            if (debugMode == 1):
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    multi("X", "0", "1", "1", "0", "X", "0")
                    i = 0
                    stats.log("beq", 3, PC)
            
            DIC += 1

            if(regval[int(line[0])]==regval[int(line[1])]):
                if(line[2].isdigit()): # First,test to see if it's a label or a integer
                    PC = int(line[2])*4
                    lineCount = int(line[2])
                    if debugMode != 1:
                        stats.log("beq", 3, PC)
                    f.write('PC is now at ' + str(line[2]) + '\n')
                    f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                    f.write('No Registers have changed. \n')
                    continue
                else: # Jumping to label
                    for i in range(len(labelName)):
                        if(labelName[i] == line[2]):
                            PC = labelAddr[i]
                            if debugMode != 1:
                                stats.log("beq", 3, PC)
                            lineCount = labelIndex[i]
                            f.write('PC is now at ' + str(labelAddr[i]) + '\n')       
                f.write('No Registers have changed. \n')

                continue


        elif(line[0:2] =="lw" and not('lw_loop' in line)):

            if (debugMode == 1):
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    multi("X", "0", "0", "1", "10", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n')
                    multi("X", "0", "0", "X", "X", "X", "0")
                    i += 1
                    continue
                elif (i == 4):
                    print("Cycle 5: Write Back" + '\n')
                    multi("1", "0", "0", "X", "X", "0", "1")
                    i = 0
                    stats.log("lw", 5, PC)

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

            if (debugMode == 1):
                if (i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n')
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue

                elif (i == 2):
                    print("Cycle 3: Execute" + '\n')
                    multi("X", "0", "0", "1", "10", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n')
                    multi("X", "1", "0", "X", "X", "X", "0")
                    i = 0
                    stats.log("sw", 4, PC)

            line= line.replace("sw","")
            line= line.replace("(",",")
            line= line.replace(")","")
            line= line.split(",")
            PC = PC + 4
            DIC += 1
            imm = get_imm(line, 1)
            if debugMode != 1:
                stats.log("sw", 4, PC)
            MEM_val = regval[int(line[0])] 
            MEM[ regval[int(line[2])] + imm ] = MEM_val
            f.write('Operation: MEM[ $' + line[2] + ' + ' + line[1] + ' ] = $' + line[0] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: None\n')


        elif(line[0:3] =="sub"):

            if(debugMode == 1):
                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "0", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "1", "1")
                    i = 0
                    stats.log("sub", 4, PC)

            line = line.replace("sub","")
            line = line.split(",")
            PC = PC + 4
            DIC += 1
            if debugMode != 1:
                stats.log("sub", 4, PC)
            regval[int(line[0])] = (regval[int(line[1])] - regval[int(line[2])])  & 0xFFFFFFFF
            f.write('Operation: $' + line[0] + ' = ' + '$' + line[1] + ' - ' + '$' + line[2] + '; ' + '\n')
            f.write('PC is now at ' + str(PC) + '\n')
            f.write('Registers that have changed: ' + '$' + line[0] + ' = ' + str(regval[int(line[0])]) + '\n')


        elif(line[0:3] == "sll"):

            if(debugMode == 1):
                if(i == 0):
                    print("Cycle 1: Instruction Fetch" + '\n')
                    multi("X", "0", "0", "0", "1", "X", "0")
                    i += 1
                    continue

                elif (i == 1):
                    print("Cycle 2: Decode" + '\n' )
                    multi("X", "0", "0", "0", "11", "X", "0")
                    i += 1
                    continue


                elif (i == 2):
                    print("Cycle 3: Execute" + '\n' )
                    multi("X", "0", "0", "1", "0", "X", "0")
                    i += 1
                    continue

                elif (i == 3):
                    print("Cycle 4: Memory" + '\n' )
                    multi("0", "0", "0", "X", "X", "1", "1")
                    i = 0
                    stats.log("sll", 4, PC) 

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

        lineCount += 1

    PC = (len(Instructions)-len(labelName)) * 4 

    final_print(regval,MEM, PC, DIC)    
    print("\n\n**************************************** FINAL CYCLE INFO ****************************************\n")
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

######################################### UI WORK ###################################
    
    while(True):
        choice_Name = input("Please select one of the following or q to quit:\n" +\
            "\t1 for Processor Simulation of MC\n" + 
            "\t2 for Processor Simulation of PC\n" + \
            "\t3 for CacheSim\n")

        if (choice_Name == "1"):
            print("You have chosen Processor Simulation of MC" + '\n')
            break

        elif(choice_Name == "2"):
            print("You have chosen Processor Simulation of PC" + '\n')
            break

        elif(choice_Name == "3"):
            print("You have chosen CacheSim")
            break
        
        elif(choice_Name == "q"):
            print("Bye!")
            return
        
        print("Please input a valid selection.\n")
    
    choice_Name = int(choice_Name)
        
    
    while(True):
        file_Name = input("Please type input file name or enter for default (proj_A.asm or proj_B.asm), or q to quit:\n")
        if(file_Name == "q"):
            print("Bye!")
            return
        
        if(file_Name == ""):
            if choice_Name != 3:
                file_Name = "proj_A.asm"
            else:
                file_Name = "proj_B.asm"
            print("File to be used is " + file_Name + "\n")

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

######################################### END UI WORK ##########################################

    h = open(file_Name,"r")

    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')
    if choice_Name == 1:
        simulate(asm, file_NameOut, select)
    if choice_Name == 2:
        print("IP\n")
    if choice_Name == 3:

        user_input= input("Which cache configuration would you like to run (a,b,c,d)\n")
        if(user_input=='a'):

            tag=[0 for i in range(4)]
            valid=[0 for i in range(4)]
            Cache=[0 for i in range(64)]
            ways_tag=[0]
            LRU=[]

            simulate_cache(asm,file_NameOut,select,user_input,tag,valid,Cache,ways_tag,LRU)

        elif(user_input=='b'):
            ways_tag=[0 for i in range(8)]
            valid=[0 for i in range(8)]
            LRU=[-1 for i in range(8)]
            Cache=[0 for i in range(64)]
            tag=[0]

            simulate_cache(asm,file_NameOut,select,user_input,tag,valid,Cache,ways_tag,LRU)

        elif(user_input=='c'):
            valid = [[0 for i in range(2)] for j in range(4)]
            ways_tag = [[0 for i in range(2)] for j in range(4)]
            LRU = [[-1 for i in range(2)] for j in range(4)]
            Cache = [0 for i in range(64)]
            tag=[0]
            simulate_cache(asm,file_NameOut,select,user_input,tag,valid,Cache,ways_tag,LRU)
        elif(user_input=='d'):
            valid = [[0 for i in range(4)] for j in range(2)]
            ways_tag = [[0 for i in range(4)] for j in range(2)]
            LRU = [[-1 for i in range(4)] for j in range(2)]
            Cache = [0 for i in range(64)]
            tag=[0]
            simulate_cache(asm,file_NameOut,select,user_input,tag,valid,Cache,ways_tag,LRU)

        print("IP\n")


  

main()
