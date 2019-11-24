addi $3, $0, 8192
addi $2, $0, 1
addi $9, $0, 4
addi $7, $0, 8
addi $14, $0, 8448
addi $15, $0, 256
loop_1:
sb   $2, 0($3)
addi $2, $2, 1
addi $3, $3, 1
bne  $2, $15, loop_1 
addi $2, $2, -1
sb   $2, 0($3)
addi $4, $0, 8192
addi $5, $0, 0
loop_2:
lb $10, 0($4)
addi $8, $0, 0
addi $6, $0, 0
HWC:
andi $9, $10, 1
beq $9, $0, skip
addi $6, $6, 1
skip:
srl $10, $10, 1
addi $8, $8, 1
bne $8, $7, HWC
bne $6, $9 , skip_count
addi $5 ,$5, 1
skip_count:
addi $4, $4, 1
bne $4, $14, loop_2
