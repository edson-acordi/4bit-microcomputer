<img src=https://img.shields.io/badge/MikroLeo%20Hardware%20Test-92%25-green>  <img src=https://img.shields.io/badge/Hardware%20License-CERN--OHL--S-brightgreen>  <img src=https://img.shields.io/badge/Software%20License-GNU%20GPL-ff0000>  <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20(you liked OR want to suppport)&style=style=flat&color=9933FF" alt="Star Badge">  

#  MikroLeo #
<img src="https://user-images.githubusercontent.com/60040866/170414182-473c82fa-b765-4346-8646-fb2904b4dfb3.png" width="12%" height="12%" align="left">  
<br />
<br />

## 4-bit Didactic Microcomputer ##

<!-- This is a comment -->

The project is in the final testing stage.  

This project was developed mainly for educational purposes.  
I hope it will be a good learning platform for anyone who likes electronics, computers and programming.  

Since my first attempts, many efforts have been made to make this project real.  

It is aimed at students, enthusiasts, hackers, professors and anyone who wants to understand or improve their knowledge of electronics and learn how a simple computer works. In addition, it is also an attempt to rescue the story about the beginning of the development of integrated circuits and computers on a single chip, to demonstrate the capabilities that these machines had at that time.  

It is a fully open-source hardware and software project that can be built at home.  Only the printed circuit board (PCB) needs to be produced by some company.  

For the next steps, an important thing is to make good documentation for MikroLeo!

*Support this project!*  
*Help to promote and disseminate the knowledge.*  

---

#### The KiCad project files have been uploaded! ####
[Download KiCad Project](https://github.com/edson-acordi/4bit-microcomputer/raw/master/Kicad-files/MikroLeo/MikroLeo_v0.1901.zip "download")  
<!--
[![Download](auxiliary/download.svg)](https://github.com/edson-acordi/4bit-microcomputer/Kicad-files/MikroLeo/MikroLeo/archive/MikroLeo_v0.1901.zip)
-->
[Download Gerber Files](https://github.com/edson-acordi/4bit-microcomputer/raw/master/Kicad-files/MikroLeo/Gerber/MikroLeo_v0.1901_Rev1.01A_Gerber.zip "download")  

[Download the schematic diagram (pdf file)](https://github.com/edson-acordi/4bit-microcomputer/raw/master/Kicad-files/MikroLeo/MikroLeo_v0.1901_Rev1.01A.pdf "download")

---

#### A Python program to generate machine code has been uploaded ####
[Python code to "compile" asm files](https://github.com/edson-acordi/4bit-microcomputer/raw/master/Compiler/MikroLeoAsm_20221130.py "download")  

[Windows executable .exe to "compile" asm files](https://github.com/edson-acordi/4bit-microcomputer/raw/master/Compiler/MikroLeoAsm_20221130.exe "download")  

---

**Main Features**:
- Implements a 4 bit CPU
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
- Indirect addressing to facilitate the implementation of subroutines
- Program memory implemented with RAM to easy programming
- It accepts 300 and 600 mils memories (for those with old DIP versions)
- Supercapacitor or battery to keep the program in RAM (for low power version)
- It can be manually programmed by switches or via Arduino/Esp32
- Built with 74HCTxxx integrated circuits for low power consumption and compatibility with TTL circuits
- All parts are through-hole for easy assembly
- All control signals, registers and the program counter are available through the pin header connectors
- Dual layer Single board with 295.9mm x 196.9mm

# MikroLeo Architecture #
Note that some buffers are used to allow viewing the contents of registers at any time, since this project is mainly intended for educational purposes.  

<img src="https://user-images.githubusercontent.com/60040866/170423097-8096352b-737d-4b8a-93d4-19edffec8095.png" width="85%" height="85%">

# The MikroLeo Instruction Set #

Although MikroLeo has only 20 instructions, using the AMODE bit (b14) and the modifier bits (b13:b12), it is possible to encode 64 combinations of instructions, as can be seen below.

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

$\text{\small\textcolor{brown}{- Note: b15 = bit15 ... b0 = bit0}}$

Thus, the Instruction Word is given as,  

<img src="https://user-images.githubusercontent.com/60040866/202838098-64f25d65-caab-41fb-b613-8623593456ad.png" width="50%" height="50%">  

### ###
**LDI - Load with Immediate**

| <sub>Instruction Word</sub> | <sub>ROMH</sub> |      <sub>Instruction</sub>     | <sub>Affected Flags</sub> |
|------------------|-----------------------|----------------------|----------------|
| 0x000n           |0x00                   | LDI ACC,n            |ZF              |
| 0x100n           |0x10                   | LDI RA,n             |-               |
| 0x200n           |0x20                   | LDI RB,n             |-               |
| 0x300n           |0x30                   | LDI RC,n             |-               |

Note that the operand (immediate) is represented by the letter "n".  
The MAddr nibble is not used with this instruction, so it is left at 0.

<ins>Examples:</ins>

| **<sub>Instruction Word</sub>** | **<sub>Instruction</sub>** |              **<sub>Comment</sub>**            |
|------------------|-------------|-|
| 0x0005           | LDI ACC,5   | Load ACC with operand |
| 0x1006           | LDI RA,6    | Load RA with operand |
| 0x2007           | LDI RB,7    | Load RB with operand |
| 0x300a           | LDI RC,10   | Load ACC with operand |

The Instruction Word, for example, for LDI RA,6 is coded as,
```asm
0x1006
  ┆┆┆└──> Least significant Nibble => Operand[b3:b0] = 6
  ┆┆└───> Second Nibble => MAddr[b7:b4] = 0
  ┆└────> Third Nibble => MICRO[b11:b8] = 0
  └─────> Most significant Nibble => HiNB[b15:b12] = 1
```
Also, the instruction word (in binary) to be manually programmed into MikroLeo using physical switches is,
```asm
0001 0000 0000 0006
  ┆    ┆    ┆    └──> Operand = 6
  ┆    ┆    └───────> MAddr = 0 (For this instruction, it doesn't matter)
  ┆    └────────────> MICRO = 0 (OPCode)
  └─────────────────> HiNB = 1 (MICRO2_IN = 0, AMODE = 0, MOD = 1)
```

**NAND - Nand bit-wise**
| <sub>Instruction Word</sub> | <sub>ROMH</sub> |      <sub>Instruction</sub>     | <sub>Affected Flags</sub> |
|------------------|-----------------------|----------------------|----------------|
| 0x010n           |0x10                   | NAND ACC,n           |ZF              |
| 0x1100           |0x11                   | NAND RA,n            |-               |
| 0x210n           |0x20                   | NAND RB,n            |-               |
| 0x310n           |0x30                   | NAND ACC,@RAM        |-               |

Note that the RAM address is pointed by RC:MAddr:LAddr.

<ins>Examples:</ins>

| **<sub>Instruction Word</sub>** | **<sub>Instruction</sub>** |              **<sub>Comment</sub>**            |
|------------------|---------------|-|
| 0x0105           | NAND ACC,5      | NAND operation between the accumulator and the operand             |
| 0x1106           | NAND RA,6       | NAND operation between the register RA and the operand             |
| 0x2107           | NAND RB,7       | NAND operation between the register RB and the operand             |
| 0x310a           | NAND ACC,@0x0a  | NAND the contents of the RAM address with ACC and stores it in ACC. In this case, the RAM address = RC:0:a|

The Instruction Word, for example, for NAND ACC,5 is coded as,
```asm
0x0105
  ┆┆┆└──> Least significant Nibble => Operand[b3:b0] = 5
  ┆┆└───> Second Nibble => MAddr[b7:b4] = 0
  ┆└────> Third Nibble => MICRO[b11:b8] = 1
  └─────> Most significant Nibble => HiNB[b15:b12] = 0
```
Also, the instruction word (in binary) to be manually programmed into MikroLeo using physical switches is,
```asm
0000 0001 0000 0005
  ┆    ┆    ┆    └──> Operand = 5
  ┆    ┆    └───────> MAddr = 0 (For this instruction, it doesn't matter)
  ┆    └────────────> MICRO = 0 (OPCode)
  └─────────────────> HiNB = 0 (MICRO2_IN = 0, AMODE = 0, MOD = 1)
```
...

# Basic Documentation #

**- MikroLeo has four Registers**  
`ACC` - Accumulator (4 bit) - Stores the result of logical and arithmetic operations. Moreover, ACC stores data that is read from or written to RAM.  
`RA` - 4 bit General purpose Register (also used for addressing).  
`RB` - 4 bit General purpose Register (also used for addressing).  
`RC` - 4 bit Special purpose Register used for addressing.  

**- Two Flags**  
Flags can only be checked by conditional jump instructions (JPC and JPZ).  

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
LDI ACC,1    ;Load the operand value into the ACC accumulator.
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
OUTA 0xF     ;Sends the operand value to the OUTA output port.
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
LDR RA     ;Loads the value of the ACC accumulator into the RA register.
```
Example 2:  
```asm
LDR RB     ;Loads the value of the ACC accumulator into the RB register.
```
Example 3: 
```asm
LDA RA     ;Loads the value from the RA Register into the ACC accumulator.
```
Example 4: 
```asm
LDA RC     ;Loads the value from the RC Register into the accumulator ACC.
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
LDI RC,1       ;Loads the operand value into the RC Register.
OUTA @0xF4     ;Sends the contents of the RAM address pointed to by RC:MAddr:LAddr to output port A,
               ;in this case, the RAM address is RC:MAddr:LAddr = 1F4h.
```
Example 2:
```asm
LDI RC,3       ;Loads the operand value into the RC Register.
ADD ACC,@0xFC  ;Sum the contents of the RAM address pointed to by RC:MAddr:LAddr with ACC and stores
               ;it in ACC. In this case, the RAM address is RC:MAddr:LAddr = 3FCh.
```
Example 3:  
```asm
LDI RC,1       ;Loads the operand value into the RC Register.
JPI @0x23      ;Jumps to the specified label. In this case, the label address is RC:MAddr:LAddr = 123h.
```
Example 4:  
```asm
LDI RC,2       ;Loads the operand value into the RC Register.
CMP ACC,0      ;Compares the contents of ACC with the operand. Is ACC equal to 0?
JPZ @0x34      ;Jumps to the specified label if ZF=1 (ACC = 0). In this case, the label address is
               ;RC:MAddr:LAddr = 234h.
```
Example 5:  
```asm
LOOP:  
  LDI RC,3       ;Loads the operand value into the RC Register.
  STW ACC,@0x21  ;Stores the contents of the accumulator in the RAM address pointed by
                 ;RC:MAddr:LAddr, in this case, the RAM address is RC:MAddr:LAddr = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP       ;Jumps to the specified label.
```
Example 6:  
```asm
LOOP:  
  LDI RC,3       ;Loads the operand value into the RC Register.
  LDW ACC,@0x21  ;Loads the contents of the RAM address pointed by RC:MAddr:LAddr in the
                 ;accumulator, in this case, the RAM address is RC:MAddr:LAddr = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP
```
Example 7:  
```asm
LOOP:  
  LDI RC,4       ;Loads the operand value into the RC Register.
  CMP ACC,@0x32  ;Compares the contents of ACC with the contents of the RAM address pointed by RC in
                 ;this case, the RAM address is RC:MAddr:LAddr = 432h. Is ACC equal to @432h?
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPZ LOOP       ;Jumps to the specified label if ZF=1 (ACC = @432h).
```

<ins> *Register Indirect* </ins>

In this addressing mode, the `RC` Register points to the high address (b11:b8). Likewise, the `RB` Register points to the medium Address (MA) while the `RA` Register points to the low Address (LA). Note that the contents of the lower and medium nibble of the instruction (MAddr, b7:b4 and LAddr, b3:b0) do not matter.  

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
LDI RC,1       ;Loads the operand value into the RC Register.
LDI RB,0xF
LDI RA,4
OUTA @R        ;Sends the contents of the RAM address pointed to by RC:RB:RA to output port A,
               ;in this case, the RAM address is RC:RB:RA = 1F4h.
```
Example 2:
```asm
LDI RC,3       ;Loads the operand value into the RC Register.
LDI RB,0xF
LDI RA,0xC
ADD ACC,@R     ;Sum the contents of the RAM address pointed to by RC:RB:RA with ACC and stores
               ;it in ACC. In this case, the RAM address is RC:RB:RA = 3FCh.
```
Example 3:  
```asm
LDI RC,1       ;Loads the operand value into the RC Register.
LDI RB,2
LDI RA,3
JPI @R         ;Jumps to the specified label. In this case, the label address is RC:RB:RA = 123h.
```
Example 4:  
```asm
LDI RC,2       ;Loads the operand value into the RC Register.
LDI RB,3
LDI RA,4
CMP ACC,0      ;Compares the contents of ACC with the operand. Is ACC equal to 0?
JPZ @R         ;Jumps to the specified label if ZF=1 (ACC = 0). In this case, the label address is
               ;RC:RB:RA = 234h.
```
Example 5:  
```asm
LOOP:  
  LDI RC,3       ;Loads the operand value into the RC Register.
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
  LDI RC,3       ;Loads the operand value into the RC Register.
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
  LDI RC,4       ;Loads the operand value into the RC Register.
  LDI RB,3
  LDI RA,2
  CMP ACC,@R     ;Compares the contents of ACC with the contents of the RAM address pointed by RC in
                 ;this case, the RAM address is RC:RB:RA = 432h. Is ACC equal to @432h?
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPZ LOOP       ;Jumps to the specified label if ZF=1 (ACC = @432h).
```

# Assembler Compiler #
Released!
See examples how to use...

# How to transfer compiled program to MikroLeo #
Almost ready...:soon:

# Emulator #
In progress...🚧

# Demo #
MikroLeo in action!  

A simple program to make a LED sequencer using the output ports. 

<img src="https://user-images.githubusercontent.com/60040866/202727866-5db3f19f-970d-4fe7-933c-747d0e465b1a.mp4" width="30%" height="30%">

A simple program to initialize an LCD.

<img src="https://user-images.githubusercontent.com/60040866/203067797-5abf8e9d-f373-4fb6-898b-bcc9be4d5c2a.mp4" width="30%" height="30%">

# Building your own MikroLeo #
...:soon:
# Contribution guidelines #
...:soon:
# Pictures #

Simulation of the MikroLeo circuit (Made with "Digital"):  
[Digital](https://github.com/hneemann/Digital) is free, open source and cross-platform software with a nice interface for digital logic design and circuit simulation.
<img src="https://user-images.githubusercontent.com/60040866/170560291-f0a1727e-c2dd-46ce-8c69-752019464398.png" width="100%" height="100%">

Breadboard:  
<img src="https://user-images.githubusercontent.com/60040866/166626556-bd559537-f371-4d85-87b8-ae23018d6fd7.jpg" width="40%" height="40%">  

PCB (KiCad 3D viewer):  
To carry out the project, the [KiCad](https://www.kicad.org/) software was used, an excellent and powerful free and open-source tool for printed circuit board (PCB) designers.  
<img src="https://user-images.githubusercontent.com/60040866/166627152-4c3770eb-8091-40ed-be2d-034289695b60.png" width="60%" height="60%">  
A simple seven-segment display interface,  
<img src="https://user-images.githubusercontent.com/60040866/198721799-a761d863-84b6-472f-9a41-5be4505674a5.png" width="25%" height="25%">

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
Since the time I took an 8086 assembly language programming course and took digital electronics and microprocessors classes in college, this project has been something I've always wanted to do. I'm fascinated by electronics, computers and programming!

The project started in 2020, and the first usable version was completed on April 20, 2020.  

Initially, the development of the project used the [Logisim-Evolution](https://github.com/logisim-evolution/logisim-evolution), and later it was migrated to the [Digital](https://github.com/hneemann/Digital).  

#### Some sources of inspiration can be seen at:  

http://www.sinaptec.alomar.com.ar/2018/03/computadora-de-4-bits-capitulo-1.html  
https://www.bigmessowires.com/nibbler/  
https://gigatron.io/  
https://eater.net/  
https://apollo181.wixsite.com/apollo181/specification  
https://www.megaprocessor.com/  
http://www.mycpu.eu/  
https://minnie.tuhs.org/Programs/CrazySmallCPU/index.html  

# Dedication #
I dedicate this project to my beloved son, Leonardo Pimentel Acordi.  

# Acknowledgements #

### The authors would like to thank:  
- The IFPR (Instituto Federal do Paraná), CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico) and Fundação Araucária for the partial funding and support for this project.

- The RENESAS (https://www.renesas.com/br/en) for sending me memory samples for tests with MikroLeo.  

- All people from the Github community and externals who support this project.

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

>***Note:***  
As this project is intended for educational purposes, I have decided to use the CERN-OHL-S license for hardware to ensure that it is always free, contributing, promoting and disseminating the essential knowledge. As such, all hardware derived from it will also be open source!  
Likewise, for the software, the GNU GPL license was used.

---
## Visitor count
<!-- This is a comment ![Visitor Count](https://profile-counter.glitch.me/{edson-acordi}/count.svg)
 -->
