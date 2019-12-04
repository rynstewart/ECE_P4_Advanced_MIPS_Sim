# Author: Trung Le


# Remember where each of the jump label is, and the target location 
def saveJumpLabel(asm,labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ","")
        if(line.count(":")):
            labelName.append(line[0:line.index(":")]) # append the label name
            labelIndex.append(lineCount) # append the label's index
            asm[lineCount] = line[line.index(":")+1:]
        lineCount += 1
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

def main():
    labelIndex = []
    labelName = []
    f = open("mc.txt","w+")
    h = open("mips.asm","r")
    asm = h.readlines()
    for item in range(asm.count('\n')): # Remove all empty lines '\n'
        asm.remove('\n')

    saveJumpLabel(asm,labelIndex,labelName) # Save all jump's destinations
    
    for line in asm:
        line = line.replace("\n","") # Removes extra chars
        line = line.replace("$","")
        line = line.replace(" ","")
        line = line.replace("zero","0") # assembly can also use both $zero and $0

        if(line[0:4] == "addi"): # ADDI
            line = line.replace("addi","")
            line = line.split(",")
            imm = format(int(line[2]),'016b') if (int(line[2]) > 0) else format(65536 + int(line[2]),'016b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[0]),'05b')
            f.write(str('001000') + str(rs) + str(rt) + str(imm) + '\n')

        elif(line[0:3] == "add"): # ADD
            line = line.replace("add","")
            line = line.split(",")
            rd = format(int(line[0]),'05b')
            rs = format(int(line[1]),'05b')
            rt = format(int(line[2]),'05b')
            f.write(str('000000') + str(rs) + str(rt) + str(rd) + str('00000100000') + '\n')
            
        elif(line[0:1] == "j"): # JUMP
            line = line.replace("j","")
            line = line.split(",")

            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location

            if(line[0].isdigit()): # First,test to see if it's a label or a integer
                f.write(str('000010') + str(format(int(line[0]),'026b')) + '\n')

            else: # Jumping to label
                for i in range(len(labelName)):
                    if(labelName[i] == line[0]):
                        f.write(str('000010') + str(format(int(labelIndex[i]),'026b')) + '\n')



    f.close()

if __name__ == "__main__":
    main()