<img src=https://img.shields.io/badge/MikroLeo%20Hardware%20Test%3A-80%25-green>

#  MikroLeo #
<img src="https://user-images.githubusercontent.com/60040866/170414182-473c82fa-b765-4346-8646-fb2904b4dfb3.png" width="12%" height="12%" align="left">  
<br />
<br />

## 4-bit Didactic Microcomputer ##

<!-- This is a comment -->

The project is in the final testing stage.  
This project was developed mainly for educational purposes.  
It is a fully open-source hardware and software project.  
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
   * 3MHz (precise time)
   * adjustable clock speed
- No MPU/MCU or complex chips
- No microcode
- Built with 74HCTxxx integrated circuits
- Dual layer Single board with 295.9mm x 196.9mm

# MikroLeo Architecture #
<img src="https://user-images.githubusercontent.com/60040866/170423097-8096352b-737d-4b8a-93d4-19edffec8095.png" width="85%" height="85%">

# Instruction Set #

<img src="https://user-images.githubusercontent.com/60040866/170366957-110239df-7da6-4218-90b6-5bdac46af302.png" width="80%" height="80%">  

# Documentation #

**- MikroLeo has four Registers**  
`ACC` - Accumulator (4 bit) - Stores the result of logical and arithmetic operations. Moreover, ACC stores data that is read from or written to RAM.  
`RA` - 4 bit General purpose Register (also used for addressing).  
`RB` - 4 bit General purpose Register (also used for addressing).  
`RC` - 4 bit Special purpose Register used for addressing.  

**- Two Flags**  
Flags are bits accessible only by conditional jump Instructions (JPC and JPZ).  

`CF` - Carry Flag - It is Set (CF=1) by ADD Instruction if it produces a carry or by SUB/CMP instruction if it results in a borrow.  
`ZF` - Zero Flag - It is affected by all operations that change the contents of ACC. It is Set (ZF=1) if the result of the last operation was zero.    

**- Addressing Modes**  

<ins> *Immediate* </ins>  

In immediate addressing, the operand (n) is contained in the lower nibble of the instruction (b3:b0), and it is denoted by Operand or LAddr.  

Examples:  
```asm
LDI ACC,1    ;Loads the value of the operand into the accumulator ACC.
LDI ACC,0xA  
NAND ACC,0   ;Performs the NAND operation between the accumulator and the operand value and
             ;stores the result in the accumulator.
OUTA 0xF     ;Sends the value of the operand to the output port OUTA.
CMP ACC,0    ;Performs the comparison between the accumulator and the operand.
SUB ACC,1    ;Performs the subtraction between the accumulator and the operand and stores
             ;the result in the accumulator.
ADD ACC,5    ;Performs the addition between the accumulator and the operand and stores the
             ;result in the accumulator.
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

Example 1:  
```asm
LOOP:  
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  STW ACC,@0x21  ;Stores the contents of the accumulator in the RAM address pointed by
                 ;RC:MAddr:LAddr, in this case, RC:MAddr:LAddr = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP       ;Jumps to the specified label
```
Example 2:  
```asm
LOOP:  
  LDI RC,3       ;Loads the value of the operand into the Register RC.
  LDW ACC,@0x21  ;Loads the contents of the RAM address pointed by RC:MAddr:LAddr in the
                 ;accumulator, in this case, RC:MAddr:LAddr = 321h.
  LDI RC,>LOOP   ;Gets the address of the label, as this code changes the contents of the Register RC.
  JPI LOOP
```

...

-------------------------------------------------
# Pictures #

Circuit Simulation:  
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
