addi $8, $0, 1
addi $9, $0, 2
addi $10, $0, 3
addi $11, $0, 4
addi $12, $0, 5

add $13, $8, $9
addiu $14, $8, 9
mult $8, $9
multu $8, $9
srl $13, $8, 1
slt $13, $8, $9
sltu $13, $8, $9
j label

label:
addi $8, $0, 3
loop:
addi $8, $8, -1
bne $8, $0, loop


beq $8, $0, end

mult $8, $9
multu $8, $9
end:
addi $9, $0, 100


lui $8, 0xFA19
ori $8, $8, 0xE366
addiu $9, $0, 1
addiu $11, $0, 101
addiu $15, $0, 0x2020
addiu $16, $0, 100
addiu $17, $0, 1
addiu $18, $0, 0x21e0
#addi $19, $0, 0xFFFF

hash:

multu $9, $8
mfhi $12
mflo $13
xor $10, $12, $13

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13

multu $10, $8
mfhi $12
mflo $13
xor $10, $12, $13

#multu $10, $17
addu $20, $0, $10
andi $13, $20, 0xFFFF
srl $12, $10, 16

xor $14, $12, $13
#multu $14, $17

sb $14, 0($18)
lbu $13, 0($18)
srl $12, $14, 8
xor $14, $12, $13
sb $14, 0($15)

addiu $9, $9, 1
addiu $15, $15, 1
bne $9, $11, hash


addiu $9, $0, 0x2020
addiu $10, $0, 0x2000
addiu $15, $0, 0
addiu $16, $0, 100
addiu $22, $0, 1

find_max:

slt $18, $16, $15
bne $18, $0, done

lbu $12, 0($9)
lbu $13, 4($10)
#subu $14, $12, $13
addu $11, $0, $9
addiu  $9, $9, 1
addiu $15, $15, 1
slt $17, $13, $12
bne $17, $0, store
j find_max

store:

sb $12, 4($10)
sb $11, 0($10)
addu $20, $11, $0
srl $20, $20, 8
sb $20, 1($10)
j find_max

done:

addiu $9, $0, 0x2020
addiu $10, $0, 0x1F   
addiu $11, $0, 0x2008
addu $14, $0, $0
#sb $14, 0($11)
addu $15, $0, $0
addiu $16, $0, 100
addiu $17, $0, 8
addu $18, $0, $0

pattern_match:

lbu $12, 0($9)

shift:
andi $13, $12, 0x1F
bne $13, $10, pattern_match_cont
j adding

pattern_match_cont:

srl $12, $12, 1
addiu $18, $18, 1
bne $17, $18, shift
j next

adding:

addiu $14, $14, 1
sb $14, 0($11)


#srl $12, $12, 1
#addiu $18, $18, 1
#bne $17, $18, shift
#j next

next:

addiu $15, $15, 1
bne $15, $16, next2
j pre_collision

next2:

addiu $9, $9, 1
addiu $18, $0, 0
j pattern_match


