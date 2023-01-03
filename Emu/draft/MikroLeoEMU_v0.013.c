/*
=================================================================================
= MikroLeoEMU, a simple Emulator for MikroLeo v0.19
= Author: Edson Junior Acordi
= License: GNU GPL v3
=
= For now, only debug execution mode has been implemented!
=
= https://github.com/edson-acordi/4bit-microcomputer
=
= Initial Release: Version v0.010 - October 20, 2022
= Last Revision: January 02, 2023
=
= The code was adapted from:
= https://github.com/davepoo/6502Emulator
= Thanks davepoo
= -------------------------------------------------------------------------------
= Compiling:
= Linux:   g++ -o MikroLeoEMU MikroLeoEMU.c
= Windows: g++ MikroLeoEMU.c -o MikroLeoEMU.exe
=
= To use the console with colored text in MS-Windows, it is necessary to add a
= modification to the registry (enable virtual terminal):
= reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 0x00000001 /f
=
= Running in Linux:
= ./MikroLeoEMU
==================================================================================
*/

#include <stdio.h>

// ---- Color Codes ----
//Regular text
#define BLK "\e[0;30m"
#define RED "\e[0;31m"
#define GRN "\e[0;32m"
#define YEL "\e[0;33m"
#define BLU "\e[0;34m"
#define MAG "\e[0;35m"
#define CYN "\e[0;36m"
#define WHT "\e[0;37m"
#define STD "\e[m" // Reset color

//High intensty text
#define HBLK "\e[0;90m"
#define HRED "\e[0;91m"
#define HGRN "\e[0;92m"
#define HYEL "\e[0;93m"
#define HBLU "\e[0;94m"
#define HMAG "\e[0;95m"
#define HCYN "\e[0;96m"
#define HWHT "\e[0;97m"

//High intensty background
#define BLKHB "\e[0;100m"
#define REDHB "\e[0;101m"
#define GRNHB "\e[0;102m"
#define YELHB "\e[0;103m"
#define BLUHB "\e[0;104m"
#define MAGHB "\e[0;105m"
#define CYNHB "\e[0;106m"
#define WHTHB "\e[0;107m"
// ----------------------

using Byte = unsigned char; // Byte type definition
using Word = unsigned short; // Word type definition

using u32 = unsigned int;

unsigned char keyb; // Var to pause the execution (used for degub)

Word MEM_ADDR; // Variable that points to the Memory Address (RC:MA:LA)
Byte AMODE; // AMODE bit variable
Byte ROMH; // Variable to gets Program memory ROMH
Byte ROML; // Variable to gets Program memory ROML
Word ROM; // Variable to store the Program Memory

struct ROMMem
{
	static constexpr u32 MAX_ROMMEM = 1024 * 2; // ROM Memory size definition
	Word ROMData[MAX_ROMMEM]; // ROM memory word size definition

	void Initialise()
	{ // Initialize all memory content with 0
		for (u32 i = 0; i < MAX_ROMMEM; i++)
		{
			ROMData[i] = 0;
		}
	}

	// Read 1 Word
	Word operator[](u32 Address) const
	{
		// Assert here address is < MAX_ROMMEM
		return ROMData[Address];
	}

	// Write 1 Word
	Word& operator[](u32 Address)
	{
		// Assert here address is < MAX_ROMMEM
		return ROMData[Address];
	}
};

struct RAMMem
{
	static constexpr u32 MAX_RAMMEM = 1024 * 2; // RAM Memory size definition
	Byte RAMData[MAX_RAMMEM]; // RAM memory word size definition

	//void Initialise()
	//{ // Initialize all memory content with 0
	//	for (u32 i = 0; i < MAX_RAMMEM; i++)
	//	{
	//		RAMData[i] = 0;
	//	}
	//}

	// Read 1 Byte
	Byte operator[](Word Address) const
	{
		// Assert here address is < MAX_RAMMEM
		return RAMData[Address];
	}

	// Write 1 Byte
	Byte& operator[](Word Address)
	{
		// Assert here address is < MAX_RAMMEM
		return RAMData[Address];
	}
};

struct CPU
{
	// Program Counter
	Word PC : 12;

	// Registers
	Byte ACC : 4; // Accumulator
	Byte  RA : 4; // Register RA
	Byte  RB : 4; // Register RB
	Byte  RC : 4; // Register RC

	// Outputs
	Byte OUTA : 4; // Output A
	Byte OUTB : 4; // Output B
	Byte OUTC : 4; // Output C
	Byte OUTD : 4; // Output D

	// Status Flags
	Byte C : 1; // Carry
	Byte Z : 1; // Zero

	void Reset(ROMMem& memory)
	{ // Initialises PC, ACC, Registers, Flags, Outputs and ROM memory
		PC = 0x000; // Reset Vector Address
		ACC = 0x0;
		RA = 0x0;
		RB = 0x0;
		RC = 0x0;
		C = 0;
		Z = 0;
		OUTA = 0x0;
		OUTB = 0x0;
		OUTC = 0x0;
		OUTD = 0x0;

		memory.Initialise();
	}

	void bin(long n)
	{ // Simple Function to Prints a Nibble with Binary format (used for MikroLeo OUTx)
		long i;
		for (i = 1 << 3; i > 0; i = i / 2) // Number of digits is defined by the second number
		{
			if((n & i) != 0)
			{
				printf("1");
			}
			else
			{
				printf("0");
			}
		}
	}

	// --- Function to Change the text Color / Background Color ---
	void red()
	{
		printf(RED);
	}

	void hred()
	{
		printf(HRED);
	}

	void yellow()
	{
		printf(YEL);
	}

	void hyellow()
	{
		printf(HYEL);
	}

	void green()
	{
		printf(GRN);
	}

	void hgreen()
	{
		printf(HGRN);
	}

	void blue()
	{
		printf(BLU);
	}

	void hblue()
	{
		printf(HBLU);
	}

	void hcyn()
	{
		printf(HCYN);
	}

	void hmag()
	{
		printf(HMAG);
	}

	void bluhb()
	{ // High intensity Background Blue
		printf(BLUHB);
	}

	void reset_color()
	{
		printf(STD);
	}
	// ----------------------- End of Color -----------------------

	Word FetchWord(u32& Cycles, ROMMem& memory)
	{
		Word ROMData = memory[PC]; // Gets Instruction Word from ROM memory
		//printf("ROMData: %x\n", ROMData); // For debug purpose
		return ROMData; // Returns the Instruction Word
	}

	/*Byte FetchNibble(u32& Cycles, RAMMem& memory_ram)
	{
		//if (AMODE == 0)

		Byte RAMData = memory_ram[MEM_ADDR]; // Gets a byte from RAM memory
		//printf("ROMData: %x\n", ROMData); // For debug purpose
		return RAMData; // Returns the byte
	}*/

	void Get_Mem_Addr()
	{ // Gets the Memory Address (RC:MA:LA) accordingly to AMODE bit

		if (AMODE == 0)
		{ // Get the Memory Address RC:MAddr:OPR
			MEM_ADDR = RC; // Get High Address
			MEM_ADDR = MEM_ADDR << 8; // Shift High Address to the correct position
			MEM_ADDR = MEM_ADDR | ROML; // Gets Mid and Low Address (MA:LA)
		}
		else
		{ // Get the Memory Address RC:RB:RA (AMODE=1)
			MEM_ADDR = RC; // Get High Address
			MEM_ADDR = MEM_ADDR << 4;
			MEM_ADDR = MEM_ADDR | RB; // Get Mid Address (RB)
			MEM_ADDR = MEM_ADDR << 4; // Shift High and Mid Address to the correct position
			MEM_ADDR = MEM_ADDR | RA; // Get Low Addres (RA)
		}
	}

	void Print_MEM_ADDR(RAMMem& memory_ram)
	{
		hcyn(); // Set Color
		// Prints the RAM Memory Address and its contents
		printf("RAM[0x%03x] = 0x%01x\n", MEM_ADDR, (memory_ram[MEM_ADDR] & 0x0f)); // Uses hex with 3 nibbles for the MEM_ADDR and
		                                                                           // Reset high nibble of memory_ram data
		reset_color();
		printf("CPU Results: Press <Enter>");
	}

	void Result(void)
	{
	// Prints the CPU Results
		PC++; // Next Instruction
		hyellow(); // Set Color
		printf(" ACC: %d\n", ACC); reset_color();
		hmag(); // Set Color
		printf("  RA: %d\n  RB: %d\n  RC: %d\n", RA, RB, RC); reset_color();
	  hred(); // Set red color
		printf("  PC: 0x%03x\n", PC); // Uses hex with 3 nibbles for the Program Counter
		reset_color();
		hgreen(); // Set Color
		printf("   Z: %d\n   C: %d\n", Z, C); reset_color();
		printf("OUTA: "); bin(OUTA); printf("\n");
		printf("OUTB: "); bin(OUTB); printf("\n");
		printf("OUTC: "); bin(OUTC); printf("\n");
		printf("OUTD: "); bin(OUTD); printf("\n\n");
	}

	// --- High Nibble + Opcodes (ROMH) in hex ---
	static constexpr Byte
		// ---- Indirect + Absolute Address (AMODE = 0) - RC:MAddr:OPR ----
		// LDI
		INS_LDIACC = 0x00, // LDI ACC,n
		INS_LDIRA  = 0x10, // LDI RA,n
		INS_LDIRB  = 0x20, // LDI RB,n
		INS_LDIRC  = 0x30, // LDI RC,n

		// NAND
		INS_NANDACC    = 0x01, // NAND ACC,n
		INS_NANDACCRA  = 0x11, // NAND ACC,RA
		INS_NANDACCRB  = 0x21, // NAND ACC,RB
		INS_NANDACCRAM = 0x31, // NAND ACC,RAM[RC:MAddr:OPR]

		// LDW
		INS_LDWACCRAM = 0x02, // LDW ACC,RAM[RC:MAddr:OPR]

		// LDA
		INS_LDARA = 0x13, // LDA RA
		INS_LDARB = 0x23, // LDA RB
		INS_LDARC = 0x33, // LDA RC

		// OUTA
		INS_OUTA    = 0x4,  // OUTA n
		INS_OUTAACC = 0x14, // OUTA ACC
		INS_OUTARA  = 0x24, // OUTA RA
		INS_OUTARAM = 0x34, // OUTA RAM[RC:MAddr:OPR]

		// OUTB
		INS_OUTB    = 0x05,  // OUTB n
		INS_OUTBACC = 0x15, // OUTB ACC
		INS_OUTBRA  = 0x25, // OUTB RA
		INS_OUTBRAM = 0x35, // OUTB RAM[RC:MAddr:OPR]

		// OUTC
		INS_OUTC    = 0x06,  // OUTC n
		INS_OUTCACC = 0x16, // OUTC ACC
		INS_OUTCRA  = 0x26, // OUTC RA
		INS_OUTCRAM = 0x36, // OUTC RAM[RC:MAddr:OPR]

		// LDR
		INS_LDRRA		= 0x17, // LDR RA
		INS_LDRRB		= 0x27, // LDR RB
		INS_LDRRC		= 0x37, // LDR RC

		// CMP
    INS_CMPACC    = 0x08,  // CMP ACC, n
    INS_CMPACCRA  = 0x18, // CMP ACC, RA
    INS_CMPACCRB  = 0x28, // CMP ACC, RB
    INS_CMPACCRAM = 0x38, // CMP ACC, RAM[RC:MAddr:OPR]

    // OUTD
    INS_OUTD    = 0x09,  // OUTD n
    INS_OUTDACC = 0x19, // OUTD ACC
    INS_OUTDRA  = 0x29, // OUTD RA
    INS_OUTDRAM = 0x39, // OUTD RAM[RC:MAddr:OPR]

		// ------------------------------------------------------------------

		// ---- Indirect Address (AMODE = 1) - RC:RB:RA ----
		// LDW
		INS_LDWACCRAMREG = 0x42; // LDW ACC,RAM[RC:RB:RA]



		// -------------------------------------------------

	// -------- End Opcodes --------

	void Execute(u32 Cycles, ROMMem& memory, RAMMem& memory_ram)
	{
		while (Cycles > 0)
		{
			ROM = FetchWord(Cycles, memory); // Gets the Instruction Word from Program Memory (ROM)
			ROMH = ROM >> 8; // Gets the value of ROMH from ROMData
			ROML = ROM & 0x00FF; // Gets the value of ROML from ROMData

			AMODE = (ROMH & 0x40) >> 6; // Gets the value of AMODE bit (divide by 64 - bit 7 of ROMH)

			Get_Mem_Addr(); // Gets the Memory Address accordingly to AMODE bit

			bluhb(); // Set text Color

			switch(ROMH) // Executes the current Instruction
			{
				// ---- Indirect + Absolute Address (AMODE = 0) - RC:MAddr:OPR ----
				case INS_LDIACC:
				{ // LDI ACC,n
					printf("\r=> LDI ACC,%d", ROML & 0x0F); // For debug purpose
					// Note: ROML & 0x0F => gets the Operand (eliminates MAddr)
					ACC = ROML & 0x0F; // Executes the Instruction, Loads ACC with Operand
					Z = (ACC == 0); // Compute ZF
				} break;

				case INS_LDIRA:
				{// LDI RA,n
					printf("\r=> LDI RA,%d", ROML & 0x0F); // For debug purpose
					RA = ROML & 0x0F;
				} break;

				case INS_LDIRB:
				{// LDI RB,n
					printf("\r=> LDI RB,%d", ROML & 0x0F); // For debug purpose
					RB = ROML & 0x0F;
				} break;

				case INS_LDIRC:
				{// LDI RC,n
					printf("\r=> LDI RC,%d", ROML & 0x0F); // For debug purpose
					RC = ROML & 0x0F; // Execute the Instruction
				} break;

				case INS_NANDACC:
				{// NAND ACC,n
					printf("\r=> NAND ACC,%d", (ROML & 0x0F)); // For debug purpose
					ACC = ~(ACC & (ROML & 0x0F)); // Execute the Instruction
					Z = (ACC == 0); // Computes ZF
				} break;

				case INS_NANDACCRA:
				{// NAND ACC,RA
					printf("\r=> NAND ACC,RA"); // For debug purpose
					ACC = ~(ACC & RA);
					Z = (ACC == 0);
				} break;

				case INS_NANDACCRB:
				{// NAND ACC,RB
					printf("\r=> NAND ACC,RB"); // For debug purpose
					ACC = ~(ACC & RB);
					Z = (ACC == 0);
				} break;

				case INS_NANDACCRAM:
				{// NAND ACC,RAM[RC:MAddr:OPR]
					printf("\r=> NAND ACC,@0x%02x", (0x0ff & MEM_ADDR)); // For debug purpose
					ACC = ~(ACC & memory_ram[MEM_ADDR]);
					Z = (ACC == 0);
				} break;

				case INS_LDWACCRAM:
				{// LDW ACC,RAM[RC:MAddr:OPR]
					printf("\r=> LDW ACC,@0x%02x", 0x0ff & MEM_ADDR); // For debug purpose
					ACC = memory_ram[MEM_ADDR];
					Z = (ACC == 0);
				} break;

				case INS_LDARA:
				{// LDA RA
					printf("\r=> LDA RA"); // For debug purpose
					ACC = RA;
					Z = (ACC == 0);
				} break;

				case INS_LDARB:
				{// LDA RB
					printf("\r=> LDA RB"); // For debug purpose
					ACC = RB;
					Z = (ACC == 0);
				} break;

				case INS_LDARC:
				{// LDA RC
					printf("\r=> LDA RC"); // For debug purpose
					ACC = RC;
					Z = (ACC == 0);
				} break;

				case INS_OUTA:
				{// OUTA n
					printf("\r=> OUTA %d", ROML & 0x0F); // For debug purpose
					OUTA = ROML & 0x0F;
				} break;

				case INS_OUTAACC:
				{// OUTA ACC
					printf("\r=> OUTA ACC"); // For debug purpose
					OUTA = ACC;
				} break;

				case INS_OUTARA:
				{// OUTA RA
					printf("\r=> OUTA RA"); // For debug purpose
					OUTA = RA;
				} break;

				case INS_OUTARAM:
				{// OUTA RAM[RC:MAddr:OPR]
					printf("\r=> OUTA @0x%02x", (0x0FF & MEM_ADDR)); // For debug purpose
					OUTA = memory_ram[MEM_ADDR];
				} break;

				case INS_OUTB:
				{// OUTB n
					printf("\r=> OUTB %d", ROML & 0x0F); // For debug purpose
					OUTB = ROML & 0x0F;
				} break;

				case INS_OUTBACC:
				{// OUTB ACC
					printf("\r=> OUTB ACC"); // For debug purpose
					OUTB = ACC;
				} break;

				case INS_OUTBRA:
				{// OUTB RA
					printf("\r=> OUTB RA"); // For debug purpose
					OUTB = RA;
				} break;

				case INS_OUTBRAM:
				{// OUTB RAM[RC:MAddr:OPR]
					printf("\r=> OUTB @0x%02x", (0x0FF & MEM_ADDR)); // For debug purpose
					OUTB = memory_ram[MEM_ADDR];
				} break;

				case INS_OUTC:
				{// OUTC n
					printf("\r=> OUTC %d", ROML & 0x0F); // For debug purpose
					OUTC = ROML & 0x0F;
				} break;

				case INS_OUTCACC:
				{// OUTC ACC
					printf("\r=> OUTC ACC"); // For debug purpose
					OUTC = ACC;
				} break;

				case INS_OUTCRA:
				{// OUTC RA
					printf("\r=> OUTC RA"); // For debug purpose
					OUTC = RA;
				} break;

				case INS_OUTCRAM:
				{// OUTC RAM[RC:MAddr:OPR]
					printf("\r=> OUTC @0x%02x", (0x0FF & MEM_ADDR)); // For debug purpose
					OUTC = memory_ram[MEM_ADDR];
				} break;

				case INS_LDRRA:
				{// LDR RA
					printf("\r=> LDR RA"); // For debug purpose
					RA = ACC ;
				} break;

				case INS_LDRRB:
				{// LDR RB
					printf("\r=> LDR RB"); // For debug purpose
					RB = ACC ;
				} break;

				case INS_LDRRC:
				{// LDR RC
					printf("\r=> LDR RC"); // For debug purpose
					RC = ACC;
				} break;

				case INS_CMPACC:
				{// CMP ACC,n
					printf("\r=> CMP ACC,%d", (ROML & 0x0F)); // For debug purpose
					Z = ACC == (ROML & 0x0F); // To computes ZF, (ACC - n == 0 ?) or (ACC == n ?)
					C = ACC >= (ROML & 0x0F); // To computes CF, (ACC - n >= 0 ?) or (ACC >= n ?)
				} break;

				case INS_CMPACCRA:
				{// CMP ACC,RA
					printf("\r=> CMP ACC,RA"); // For debug purpose
					Z = ACC == RA; // To computes ZF, (ACC - RA == 0 ?) or (ACC == RA ?)
					C = ACC >= RA; // To computes CF, (ACC - RA >= 0 ?) or (ACC >= RA ?)
				} break;

				case INS_CMPACCRB:
				{// CMP ACC,RB
					printf("\r=> CMP ACC,RB"); // For debug purpose
					Z = ACC == RB; // To computes ZF, (ACC - RB == 0 ?) or (ACC == RB ?)
					C = ACC >= RB; // To computes CF, (ACC - RB >= 0 ?) or (ACC >= RB ?)
				} break;

				case INS_CMPACCRAM:
				{// CMP ACC,RAM[RC:MAddr:OPR]
					printf("\r=> CMP ACC,@0x%02x", (0x0FF & MEM_ADDR)); // For debug purpose
					Z = ACC == memory_ram[MEM_ADDR]; // To computes ZF, (ACC - RAM == 0 ?) or (ACC == RAM ?)
					C = ACC >= memory_ram[MEM_ADDR]; // To computes CF, (ACC - RAM >= 0 ?) or (ACC >= RAM ?)
				} break;




				case INS_OUTD:
				{// OUTD n
					printf("\r=> OUTD %d", ROML & 0x0F); // For debug purpose
					OUTD = ROML & 0x0F;
				} break;

				case INS_OUTDACC:
				{// OUTD ACC
					printf("\r=> OUTD ACC"); // For debug purpose
					OUTD = ACC;
				} break;

				case INS_OUTDRA:
				{// OUTD RA
					printf("\r=> OUTD RA"); // For debug purpose
					OUTD = RA;
				} break;

				case INS_OUTDRAM:
				{// OUTC RAM[RC:MAddr:OPR]
					printf("\r=> OUTD @0x%02x", (0x0FF & MEM_ADDR)); // For debug purpose
					OUTD = memory_ram[MEM_ADDR];
				} break;




				//-----------------------------------------------------------------

				//---- Indirect Address (AMODE = 1) - RC:RB:RA ----
				case INS_LDWACCRAMREG:
				{// LDW ACC,RAM[RC:RB:RA]
					printf("\r=> LDW ACC,@R"); // For debug purpose
					ACC = memory_ram[MEM_ADDR];
					Z = (ACC == 0);
				} break;

				default:
				{ // Instruction not defined for MikroLeo
					printf("\n");
					printf("Instruction not handled 0x%02x", ROMH);
				} break;
			}

			printf(" - INSTRUCTION WORD: 0x%04x", ROM);
			printf(" - AMODE: %d", AMODE);
			reset_color();
			printf("\n");
			Print_MEM_ADDR(memory_ram);
			keyb = getc(stdin); // Press <Enter> to execute the Instruction
			Result(); // Print CPU results
			Cycles--; // Until the number of Cycles ends
		}
	}
};

int main()
{
	ROMMem mem; // Define a estrutura variável mem com o tipo da estrutura ROMMen
	RAMMem mem_ram;
	CPU cpu;  // Define a estrutura variável cpu com o tipo da estrutura CPU
	cpu.Reset(mem);

	// ---- Inline a little program ----
	// Mainly used to test each implemented instruction
	mem[0x000] = CPU::INS_LDIRA; // Put the Instruction Code into the ROM memory
	mem[0x000] = (mem[0x000] << 8) | 0x0f; // Move Opcode to ROMH and put MAddr:OPR in ROML[b7:b0]
	/*
	mem[0x000] = (mem[0x000] << 8) | 0x0f; // Move Opcode to ROMH and put MAddr:OPR in ROML[b7:b0]
                      ┆     ┆    ┆   ┆└──> Operand n
											┆			┆		 ┆	 └───> MAddr
											┆			┆    └───────> ROMH OR (MAddr:Operand)
											┆			└────────────> Shifts ROMH 8bit left
											└──────────────────> ROM Address
	*/

	mem[0x001] = CPU::INS_LDIRC; // Put the Instruction Code into the ROM memory
	mem[0x001] = (mem[0x001] << 8) | 0x07; // Move Opcode to ROMH and put MAddr:OPR in ROML[b7:b0]

	mem[0x002] = CPU::INS_LDIACC; // Put the Instruction Code into the ROM memory
	mem[0x002] = (mem[0x002] << 8) | 0x41; // Move Opcode to ROMH and put MAddr:OPR in ROML[b7:b0]

  mem[0x003] = CPU::INS_NANDACC; // Put the Instruction Code into the ROM memory
  mem[0x003] = (mem[0x003] << 8) | 0x11; // Move Opcode to ROMH and put MAddr:OPR in ROML[b7:b0]

  mem_ram[0x712] = 0x01; // Write a byte to a RAM Address

  mem_ram[0x70f] = 0x04; // Write a byte to a RAM Address

  mem_ram[0x700] = 0x07; // Write a byte to a RAM Address

  mem[0x004] = CPU::INS_OUTCRAM;
  mem[0x004] = (mem[0x004] << 8) | 0x00;

  mem[0x005] = CPU::INS_LDWACCRAMREG;
  mem[0x005] = (mem[0x005] << 8) | 0x00;

	mem[0x006] = CPU::INS_LDRRA;
	mem[0x006] = (mem[0x006] << 8) | 0x00;

	mem[0x007] = CPU::INS_CMPACC;
	mem[0x007] = (mem[0x007] << 8) | 0x03;

	mem[0x008] = CPU::INS_CMPACCRA;
	mem[0x008] = (mem[0x008] << 8) | 0x00;

	mem[0x009] = CPU::INS_CMPACCRB;
	mem[0x009] = (mem[0x009] << 8) | 0x00;

	mem[0x00a] = CPU::INS_CMPACCRAM;
	mem[0x00a] = (mem[0x00a] << 8) | 0x00;


	//printf("mem0: %x\n", mem[0x000]);
	//printf("mem1: %x\n", mem[0x001]);
	//printf("mem2: %x\n", mem[0x002]);
	// ---- End Inline a little program ---

	// ---- Loads a program from hex or bin file ----
	// ...
	// ----------------------------------------------
	// For inline program, don't forget to set the number of cycles!
	cpu.Execute(11, mem, mem_ram); // Run a specific number of cycles

	return 0;
}

/*
--------------------------------------------------------------------------------
 MikroLeoEMU - A simple Emulator for MikroLeo 4-bit Microcomputer v0.19
 Copyrigh (c) 2022 Edson Junior Acordi
--------------------------------------------------------------------------------
 */
