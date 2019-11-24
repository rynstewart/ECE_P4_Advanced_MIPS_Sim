lui $8, 0xFA19
ori $8, $8, 0xE366
addiu $9, $0, 1
addiu $11, $0, 0x65
addiu $15, $0, 0x2020
addiu $16, $0, 100
addiu $17, $0, 1
addiu $18, $0, 0x21e0

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

addu $20, $0, $10
andi $13, $20, 0xFFFF
srl $12, $10, 16

xor $14, $12, $13

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
j sum

pattern_match_cont:

srl $12, $12, 1
addiu $18, $18, 1
bne $17, $18, shift
j next

sum:

addiu $14, $14, 1
sb $14, 0($11)

next:

addiu $15, $15, 1
bne $15, $16, next2
j pre_collision

next2:

addiu $9, $9, 1
addiu $18, $0, 0
j pattern_match

pre_collision:
