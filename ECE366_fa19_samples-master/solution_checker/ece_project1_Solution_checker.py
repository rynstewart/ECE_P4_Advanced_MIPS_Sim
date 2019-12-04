
# Author: Trung Le

patternCount = 0
largestC = 0
collision = [0] * 256
for i in range(101):
    originalA = i
    A = originalA
    B =    0b11111010000110011110001101100110  #B = 4196000614 or 0xFA19E366
    #B =    0b11101100111000110110011011111010  #B = 3974326010 or 0xECE366FA
    high = 0b1111111111111111111111111111111100000000000000000000000000000000
    low  = 0b0000000000000000000000000000000011111111111111111111111111111111

    MUL = A*B
    FOLD = ((MUL&high)>>32) ^ (MUL&low) 
    A = FOLD

    MUL = A*B
    FOLD = ((MUL&high)>>32) ^ (MUL&low) 
    A = FOLD

    MUL = A*B
    FOLD = ((MUL&high)>>32) ^ (MUL&low) 
    A = FOLD

    MUL = A*B
    FOLD = ((MUL&high)>>32) ^ (MUL&low) 
    A = FOLD

    MUL = A*B
    FOLD = ((MUL&high)>>32) ^ (MUL&low) 
    A = FOLD

    high = 0b11111111111111110000000000000000
    low =  0b00000000000000001111111111111111
    C = (A&high)>>16 ^ (A&low)

    high = 0b1111111100000000
    low  = 0b0000000011111111
    C = ((C&high)>>8) ^ ((C&low))
    collision[C] += 1
    if(C > largestC):
        largestC = C
    
    print('With A =', originalA, ' and B =',B, ' C (binary)=',format(C,'08b'), ' C (decimal)= ', C)
    C = bin(C)
    print(' Contains 11111 = ','11111' in C, '\n')

    if('11111' in C):
        patternCount += 1
print('Largest C: ',largestC)
print('Total matching pattern count :', patternCount)
print('Maximum collision :',max(collision), ' with the C value of ', collision.index(max(collision)))



