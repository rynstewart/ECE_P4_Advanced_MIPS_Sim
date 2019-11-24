addi $8, $0, 1
addi $9, $0, -1
addi $10, $0, 5
addi $11, $0, -5

slt $12, $0, $8
slt $13, $10, $8
slt $14, $10, $10

slti $15, $0, 1
slti $16, $10, 1
slti $17, $10, 5

sltu $18, $0, $8
sltu $19, $10, $8
sltu $20, $10, $10
sltu $21, $11, $8

addi $18, $0, 0
addi $19, $0, 0
addi $20, $0, 0
addi $21, $0, 0

sltiu $18, $0, 1
sltiu $19, $10, 1
sltiu $20, $10, 5
sltiu $21, $11, 1