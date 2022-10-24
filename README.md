<img src=https://img.shields.io/badge/MikroLeo%20Hardware%20Test%3A-92%25-green>

#  MikroLeo #
<img src="https://user-images.githubusercontent.com/60040866/170414182-473c82fa-b765-4346-8646-fb2904b4dfb3.png" width="12%" height="12%" align="left">  
<br />
<br />

## 4-bit Didactic Microcomputer ##

<!-- This is a comment -->

The project is in the final testing stage.  
This project was developed mainly for educational purposes.  
It is a fully open-source hardware and software project that can be built at home.  Only the printed circuit board (PCB) needs to be sent to be produced by some company.  
Soon, the project files will be here!  

**Main Features**:
- 2k x 16 ROM (up to 4k)
- 2k x 4 RAM (up to 4k)
- 4 Output Ports (16 outputs)
- 4 Input Ports (16 inputs)
- Single Cycle Instruction/RISC
- Harvard Architecture
- 3 execution modes:
   * step
   * 3MHz (precise time base)
   * adjustable clock speed
- No MPU/MCU or complex chips
- No microcode
- Built with 74HCTxxx integrated circuits
- Dual layer Single board with 295.9mm x 196.9mm

# MikroLeo Architecture #
Note that some buffers are used to allow viewing the contents of registers at any time, since this project is mainly intended for educational purposes.  

<img src="https://user-images.githubusercontent.com/60040866/170423097-8096352b-737d-4b8a-93d4-19edffec8095.png" width="85%" height="85%">

# The MikroLeo Instruction Set #

<img src="https://user-images.githubusercontent.com/60040866/170366957-110239df-7da6-4218-90b6-5bdac46af302.png" width="80%" height="80%">  

## Instruction Set explanation and examples ##

In binary, the Instruction Word is coded as,

ROMH (Most significant byte of program memory):  
| <sub>b15</sub> | <sub>b14</sub> | <sub>b13</sub>| <sub>b12</sub>| <sub>b11</sub> | <sub>b10</sub> | <sub>b9</sub> | <sub>b8</sub> 
|---------|-----|----|----|------|------|------|------|
|<sub>MICRO2_IN</sub>|<sub>AMODE</sub>|<sub>MOD1</sub>|<sub>MOD0</sub>|<sub>MICRO3</sub>|<sub>MICRO2</sub>|<sub>MICRO1</sub>|<sub>MICRO0</sub>|

ROML (Least significant byte of program memory):  
| <sub>b7</sub> | <sub>b6</sub> |  <sub>b5</sub> | <sub>b4</sub> | <sub>b3</sub> | <sub>b2</sub> | <sub>b1</sub> | <sub>b0</sub> |  
|------|------|------|------|--------|--------|--------|--------|  
<sub>MAddr3</sub>|<sub>MAddr2</sub>|<sub>MAddr1</sub>|<sub>MAddr0</sub>|<sub>Operand3</sub>|<sub>Operand2</sub>|<sub>Operand1</sub>|<sub>Operand0</sub>|  

$\text{\small\textcolor{purple}{- Note: b15 = bit15 ... b0 = bit0}}$

### ###
**LDI - Load with Immediate**
 
| Instruction Word | AMODE:Modifier:OPCODE |      Instruction     | Affected Flags |
|------------------|-----------------------|----------------------|----------------|
| 0x000n           |0x00                   | LDI ACC,n            |ZF              |
| 0x100n           |0x10                   | LDI RA,n             |-               |
| 0x200n           |0x20                   | LDI RB,n             |-               |
| 0x300n           |0x30                   | LDI RC,n             |-               |

***Examples:***

| **Instruction Word** | **Instruction** |              **Comment**            |
|------------------|-------------|-|
| 0x0005           | LDI ACC,5   | Load ACC with operand |
| 0x1006           | LDI RA,6    | Load RA with operand |
| 0x2007           | LDI RB,7    | Load RB with operand |
| 0x300a           | LDI RC,10   | Load ACC with operand |

The Instruction Word, for example, for LDI RA,6 is coded as,
```
 0x1006  
   ┆┆┆└--> Least significant Nibble => Operand[b3:b0] = 6  
   ┆┆└---> Second Nibble => MAddr[b7:b4] = 0  
   ┆└----> Third Nibble => MICRO[b11:b8] = 0  
   └-----> Most significant Nibble => HiNB[b15:b12] = 1  
```

...

# Basic Documentation #

**- MikroLeo has four Registers**  
`ACC` - Accumulator (4 bit) - Stores the result of logical and arithmetic operations. Moreover, ACC stores data that is read from or written to RAM.  
`RA` - 4 bit General purpose Register (also used for addressing).  
`RB` - 4 bit General purpose Register (also used for addressing).  
`RC` - 4 bit Special purpose Register used for addressing.  

**- Two Flags**  
Flags are bits accessible only by conditional jump Instructions (JPC and JPZ).  

`CF` - Carry Flag - It is Set (CF=1) by ADD Instruction if it produces a carry or by SUB/CMP instruction if it results in a borrow.  
`ZF` - Zero Flag - It is affected by operations that modify the contents of the ACC and by CMP instruction. It is Set (ZF=1) if the result of the last operation was zero.    

Example of how CF and ZF are Set:  
```asm
LDI ACC,1  
ADD ACC,0xF  
```
This code does it,
```
   0001
+  1111
-------  
 1 0000  
 ↓   ↓  
CF  ACC

As the value zero is written to ACC, ZF=1.
```

**- Addressing Modes**  

<ins> *Immediate* </ins>  

In immediate addressing, the operand (n) is contained in the lower nibble of the instruction (b3:b0), and it is denoted by Operand, LAddr or OPR.  

Example 1:  
```asm
LDI ACC,1    ;Loads the value of the operand into the accumulator ACC.
```
Example 2:  
```asm
LDI ACC,0xA  
```
Example 3:
```asm
NAND ACC,0   ;Performs the NAND operation between the accumulator and the operand value and
             ;stores the result in the accumulator.
```
Example 4:
```asm
OUTA 0xF     ;Sends the value of the operand to the output port OUTA.
```
Example 5:
```asm
CMP ACC,0    ;Performs the comparison between the accumulator and the operand.
```
Example 6:
```asm
SUB ACC,1    ;Performs the subtraction between the accumulator and the operand and stores
             ;the result in the accumulator.
```
Example 7:
```asm
ADD ACC,5    ;Performs the addition between the accumulator and the operand and stores the
             ;result in the accumulator.
```

<ins> *Register Direct* </ins>  

In this mode, the operand must be one of the four registers (ACC, RC, RB, RA). Thus, the contents of the lower and medium nibble of the instruction (MAdrr, b7:b4 and LAddr, b3:b0) do not matter. Note that in the LDR instruction, the operand (ACC) is implied. LDR stands for load the Register Rx with ACC, being x={A,B,C}. In the LDA instruction, the operand must be one of the three registers (RC, RB, RA). LDA stands for load the accumulator with one of Rx Registers. Note that in register direct addressing mode, data can be read from or written to a register.  

Example 1:  
```asm
  LDR RA     ;Loads the value of the accumulator ACC into the RA register.
```
Example 2:  
```asm
  LDR RB     ;Loads the value of the accumulator ACC into the RB register.
```
Example 3: 
```asm
  LDA RA     ;Loads the value of the Register RA into the accumulator ACC.
```
Example 4: 
```asm
  LDA RC     ;Loads the value of the Register RC into the accumulator ACC.
```

<ins> *Register Indirect + Absolute* </ins>

In this addressing mode, the `RC` Register points to the high address (b11:b8). The medium (MAddr) and low (LAddr) nibble of the instruction, point to the medium and low address, respectively.  

The final address is composed by `RC:MAddr:LAddr`.  

For example, if:  
```
RC = 3  
MAddr = 2  
LAddr = 1  
```
The address to be accessed is 321h.  
In the MikroLeo python assembler, absolute addresses (`MAddr:LAddr`) are indicated by an @.

Example 1:
```asm
  LDI RC,1       ;Loads the value of the operand into the Register RC.
  OUTA @0xF4     ;Sends the contents of the RAM address pointed to by RC:MAddr:LAddr to output port A,
                 ;in this case, the RAM address is RC:MAddr:LAddr = 1F4h.
```
Example 2:
```asm
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  ADD ACC,@0xFC  ;Sum the contents of the RAM address pointed to by RC:MAddr:LAddr with ACC and stores
                 ;it in ACC. In this case, the RAM address is RC:MAddr:LAddr = 3FCh.
```
Example 3:  
```asm
  LDI RC,1       ;Loads the value of the operand into the Register RC.
  JPI @0x23      ;Jumps to the specified label. In this case, the label address is RC:MAddr:LAddr = 123h.
```
Example 4:  
```asm
  LDI RC,2       ;Loads the value of the operand into the Register RC.
  CMP ACC,0      ;Compares the contents of ACC with the operand. Is ACC equal to 0?
  JPZ @0x34      ;Jumps to the specified label if ZF=1 (ACC = 0). In this case, the label address is
                 ;RC:MAddr:LAddr = 234h.
```
Example 5:  
```asm
LOOP:  
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  STW ACC,@0x21  ;Stores the contents of the accumulator in the RAM address pointed by
                 ;RC:MAddr:LAddr, in this case, the RAM address is RC:MAddr:LAddr = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP       ;Jumps to the specified label.
```
Example 6:  
```asm
LOOP:  
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  LDW ACC,@0x21  ;Loads the contents of the RAM address pointed by RC:MAddr:LAddr in the
                 ;accumulator, in this case, the RAM address is RC:MAddr:LAddr = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP
```
Example 7:  
```asm
LOOP:  
  LDI RC,4       ;Loads the value of the operand into the Register RC.
  CMP ACC,@0x32  ;Compares the contents of ACC with the contents of the RAM address pointed by RC in
                 ;this case, the RAM address is RC:MAddr:LAddr = 432h. Is ACC equal to @432h?
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPZ LOOP       ;Jumps to the specified label if ZF=1 (ACC = @432h).
```

<ins> *Register Indirect* </ins>

In this addressing mode, the `RC` Register points to the high address (b11:b8). Likewise, the 'RB' Register points to the medium Address (MA) while the RA Register points to the low Address (LA). Note that the contents of the lower and medium nibble of the instruction (MAddr, b7:b4 and LAddr, b3:b0) do not matter.  

The final address is composed by `RC:RB:RA`.  

For example, if:  
```Thus, the contents of the lower and medium nibble of the instruction (b7:b4, b3:b0) do not matter.
RC = 3  
RB = 2  
RA = 1  
```
The address to be accessed is 321h.  
In MikroLeo's python assembler, indirect register addresses (`RC`:`RB`:`RA`) are indicated by an @R.

Example 1:
```asm
  LDI RC,1       ;Loads the value of the operand into the Register RC.
  LDI RB,0xF
  LDI RA,4
  OUTA @R        ;Sends the contents of the RAM address pointed to by RC:RB:RA to output port A,
                 ;in this case, the RAM address is RC:RB:RA = 1F4h.
```
Example 2:
```asm
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  LDI RB,0xF
  LDI RA,0xC
  ADD ACC,@R     ;Sum the contents of the RAM address pointed to by RC:RB:RA with ACC and stores
                 ;it in ACC. In this case, the RAM address is RC:RB:RA = 3FCh.
```
Example 3:  
```asm
  LDI RC,1       ;Loads the value of the operand into the Register RC.
  LDI RB,2
  LDI RA,3
  JPI @R         ;Jumps to the specified label. In this case, the label address is RC:RB:RA = 123h.
```
Example 4:  
```asm
  LDI RC,2       ;Loads the value of the operand into the Register RC.
  LDI RB,3
  LDI RA,4
  CMP ACC,0      ;Compares the contents of ACC with the operand. Is ACC equal to 0?
  JPZ @R         ;Jumps to the specified label if ZF=1 (ACC = 0). In this case, the label address is
                 ;RC:RB:RA = 234h.
```
Example 5:  
```asm
LOOP:  
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  LDI RB,2
  LDI RA,1
  STW ACC,@R     ;Stores the contents of the accumulator in the RAM address pointed by
                 ;RC:RB:RA, in this case, the RAM address is RC:RB:RA = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP       ;Jumps to the specified label.
```
Example 6:  
```asm
LOOP:  
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  LDI RB,2
  LDI RA,1
  LDW ACC,@R     ;Loads the contents of the RAM address pointed by RC:RB:RA in the
                 ;accumulator, in this case, the RAM address is RC:RB:RA = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP
```
Example 7:  
```asm
LOOP:  
  LDI RC,4       ;Loads the value of the operand into the Register RC.
  LDI RB,3
  LDI RA,2
  CMP ACC,@R     ;Compares the contents of ACC with the contents of the RAM address pointed by RC in
                 ;this case, the RAM address is RC:RB:RA = 432h. Is ACC equal to @432h?
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPZ LOOP       ;Jumps to the specified label if ZF=1 (ACC = @432h).
```

...

-------------------------------------------------
# Pictures #

Simulation of the Mikroleo circuit (Made with the "Digital" Software, developed by Helmut Neemann):  
<img src="https://user-images.githubusercontent.com/60040866/170560291-f0a1727e-c2dd-46ce-8c69-752019464398.png" width="100%" height="100%">

Breadboard:  
<img src="https://user-images.githubusercontent.com/60040866/166626556-bd559537-f371-4d85-87b8-ae23018d6fd7.jpg" width="40%" height="40%">  

PCB (Kicad 3D viewer):  
<img src="https://user-images.githubusercontent.com/60040866/166627152-4c3770eb-8091-40ed-be2d-034289695b60.png" width="60%" height="60%">  

PCB Prototype:  
<img src="https://user-images.githubusercontent.com/60040866/166628285-47b3ee24-fd4e-49f8-9bca-21af1cec307d.jpg" width="55%" height="55%">  

-------------------------------------------

# Development stages #

- [x] - Bibliographic research
- [x] - Architecture definition
- [x] - Circuit design
- [x] - Circuit simulation
- [x] - Prototype assembly on breadboard
- [x] - Printed circuit board design
- [x] - Prototype assembly on PCB
- [ ] - Final Tests


# History and Motivation #
Since the time I took an 8086 assembly language programming course, this project has been something that I have always wanted to do.  
The project started in 2020, and the first usable version was completed on April 20, 2020.  
Initially, the development of the project used the Logisim-Evolution software, and later it was migrated to the Digital software (Helmut Neemann).  

Some sources of inspiration can be seen at:  

http://www.sinaptec.alomar.com.ar/2018/03/computadora-de-4-bits-capitulo-1.html  
https://www.bigmessowires.com/nibbler/  
https://gigatron.io/  
https://eater.net/  
https://apollo181.wixsite.com/apollo181/specification  

# Dedication #
This project is dedicated to my son, Leonardo Pimentel Acordi.  

# Acknowledgements #

The authors would like to thank the IFPR (Instituto Federal do Paraná) and CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico) for partially funding this project.

# Authors #

>Edson Junior Acordi  
Matheus Fernando Tasso  
Carlos Daniel de Souza Nunes  

# License #

**Hardware:** Licensed under CERN-OHL-S v2 or any later version  
https://ohwr.org/cern_ohl_s_v2.txt

**Software:** Licensed under GNU GPL v3  
https://www.gnu.org/licenses/gpl-3.0.txt

**Documentation:** Licensed under CC BY-SA 4.0  
https://creativecommons.org/licenses/by-sa/4.0/
