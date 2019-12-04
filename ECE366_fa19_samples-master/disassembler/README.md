# MIPS-byline-disassembler

Goal: a simple Python program sample, which disassemble one line (via input) a Hex into a line of (output on screen) MIPS assembly instruction.
- supporting 2 MIPS instructions: add, addi

- For example:

 Input a 8-digit hex:
 
 22a7000e
 
 0x22A7000E  is addi $7, $21, 14
 
 Input a 8-digit hex: 
 
 20e6fffd
 
 0x20E6FFFD is addi $6, $7, -3
 
 Input a 8-digit hex: 
 
 30e70001
 
 not supported
 
 Input a 8-digit hex: 
 
 00e62820
 
 0x00E62820 is add $5, $7, $6
 
 Input a 8-digit hex: 
 
 quit
 
 bye!
 
 
 ## TA's version:
 The disassembler is written in Python3.0 , to run it :   
 
```bash
python3 disassembler_TrungLe.py
```
 
 

 

