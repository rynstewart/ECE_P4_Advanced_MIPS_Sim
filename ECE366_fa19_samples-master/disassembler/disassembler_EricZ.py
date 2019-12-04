# Author: Eric Zavala
# Homework 2 Example

# Main Program
response = raw_input("Input an 8-digit hex: ")

while(response != 'quit'):
    x = int(response,16)
    first6 = x & int('0xfc000000',16)

    if first6 == int('0x00000000',16):#check that coditions for add instr are true
        last6 = x & int('0x000000ff',16)
        if last6 == int('0x00000020',16):
            rs = x & int('0x03e00000',16)
            rs = rs >> 21
            rt = x & int('0x001f0000',16)
            rt = rt >> 16
            rd = x & int('0x0000f800',16)
            rd = rd >> 11
            print("0x" + str(x) + " is add $" + str(rd) + ", $" + str(rs) + ", $" + str(rt) + "\n")
    elif first6 == int('0x20000000',16):# check conditions for addi instr are true
        rs = x & int('0x03e00000',16)
        rs = rs >> 21
        rt = x & int('0x001f0000',16)
        rt = rt >> 16
        imm = x & int('0x0000ffff',16)
        # convert to signed
        if imm & (1 << 15):
            imm -= 1 << 16
        print(hex(x) + " is addi $" + str(rt) + ", $" + str(rs) + ", " + str(imm) + "\n")
    else:
        print("Instruction not supported")
    response = raw_input("Input an 8-digit hex: ")
print("End program")

