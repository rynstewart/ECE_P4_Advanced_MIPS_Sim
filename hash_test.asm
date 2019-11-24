lui $8, 0xFA19
ori $8, $8, 0xE366
addiu $9, $0, 1
addiu $11, $0, 0x65
addiu $15, $0, 0x2020
addiu $16, $0, 0x0064
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