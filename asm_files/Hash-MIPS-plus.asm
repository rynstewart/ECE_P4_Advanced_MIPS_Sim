lui $11, 0xFA19
ori $11, $11, 0xE366
addi $9, $0, 101
addi $8, $0, 1
loop:
add $10, $8, $11
addi $8, $8, 1
bne $8, $9, loop
sb $10, 0x2008($0)