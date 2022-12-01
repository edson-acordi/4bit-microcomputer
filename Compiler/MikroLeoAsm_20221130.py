# ******************************************************************************
# This program is used to generate the hex codes for the MikroLeo 4-bit
# Microcomputer. The hex code is generated from an assembly text source file.
#
# https://github.com/edson-acordi/4bit-microcomputer
#
# By Edson Junior Acordi
# Initial Release: Version v0.10 - January, 03, 2022
# Last Revision:   Version v0.12 - October, 17, 2022
#
# License: GNU GPL v3
#
# Usage: python MikroLeoAsm_20221130.py sourcefilename
# Example: python MikroLeoAsm_20221130.py test.asm
#
# For the assembly language details, see the MikroLeo documentation.
#
# The code was adapted from:
# https://github.com/slu4coder/Minimal-UART-CPU-System/
# Thanks Slu4
# ******************************************************************************

import sys
import re

# OpCodes in hexadecimal notation
opCodes = {  # Indirect + Absolute Address (AMODE = 0) - RC:MAddr:LAddr
           'LDIACC': '0', 'LDIRA': '0x10', 'LDIRB': '0x20', 'LDIRC': '0x30',
           'NANDACC': '1', 'NANDACCRA': '0x11', 'NANDACCRB': '0x21',
           'NANDACCRAM': '0x31',
           'LDWACCRAM': '2',
           'LDARA': '0x13', 'LDARB': '0x23', 'LDARC': '0x33',
           'OUTA': '4', 'OUTAACC': '0x14', 'OUTARA': '0x24', 'OUTARAM': '0x34',
           'OUTB': '5', 'OUTBACC': '0x15', 'OUTBRA': '0x25', 'OUTBRAM': '0x35',
           'OUTC': '6', 'OUTCACC': '0x16', 'OUTCRA': '0x26', 'OUTCRAM': '0x36',
           'OUTD': '9', 'OUTDACC': '0x19', 'OUTDRA': '0x29', 'OUTDRAM': '0x39',
           'LDRRA': '0x17', 'LDRRB': '0x27', 'LDRRC': '0x37',
           'CMPACC': '8', 'CMPACCRA': '0x18', 'CMPACCRB': '0x28',
           'CMPACCRAM': '0x38',
           'STWRAMACC': '0x0A',
           'SUBACC': '0x0B', 'SUBACCRA': '0x1B', 'SUBACCRB': '0x2B',
           'SUBACCRAM': '0x3B',
           'JPI': '0x0C',
           'JPC': '0x0D',
           'JPZ': '0x0E',
           'ADDACC': '0x0F', 'ADDACCRA': '0x1F', 'ADDACCRB': '0x2F',
           'ADDACCRAM': '0x3F',
           'INAACC': '0X80',
           'INBACC': '0X90',
           'INCACC': '0XA0',
           'INDACC': '0XB0',
           # Indirect Address (AMODE = 1) - RC:RB:RA
           'NANDACCRAMREG': '0x71',
           'LDWACCRAMREG': '0x42',
           'OUTARAMERG': '0x74',
           'OUTBRAMERG': '0x75',
           'OUTCRAMERG': '0x76',
           'CMPACCRAMREG': '0x78',
           'OUTDRAMERG': '0x79',
           'STWRAMACCREG': '0x4A',
           'SUBACCRAMREG': '0x7B',
           'JPIREG': '0x4C',
           'JPCREG': '0x4D',
           'JPZREG': '0x4E',
           'ADDACCRAMREG': '0x7F'
           }

lines, inst, consts, lineinfo, lineadr, labels = [], [], [], [], [], {}
LINEINFO_NONE, LINEINFO_ORG, LINEINFO_BEGIN, LINEINFO_END = 0x00000, 0x10000, 0x20000, 0x40000

tmp = 0  # Temporary variable
num_inst = 0  # Used to print only non empty instructions lines
one_cycle = 0  # To run a piece of code once
count = 0  # To count the number of lines in source file
tmp2 = 0  # Temporary variable
tmp3 = 0  # Temporary variable

if len(sys.argv) != 2:
    print('usage: MikroLeoAsm.py <sourcefile>', '')
    print('Example:', '')
    print('MikroLeoAsm.py test.asm')
    sys.exit(1)
f = open(sys.argv[1], 'r')
while True:  # read in the source line
    line = f.readline()
    if not line:
        break
    # store each line without leading/trailing whitespaces
    lines.append(line.strip())

f.close()

for t in range(len(lines)):
    lines[t] = re.sub(r';.*', '', lines[t])  # Delete all comments characters
    # and all that comes after it.
    ##lines[t] = lines[t].upper()  # Change all strings in list to uppercase
    #lines[t] = lines[t] + re.sub(r'^(&\w\w)', lines[t].upper(), lines[t])
    # Remove unnecessary spaces (duplicates)
    lines[t] = " ".join(lines[t].split())

# Extract all #define from lines to a new list (constants)
for k in range(len(lines)):
    consts = [s for s in lines if s.__contains__("#DEFINE")]
    #print('Constants 00:', consts)  # Debug

# Remove the text #define from consts[:]
for q in range(len(consts)):
    consts[q] = re.sub(r'#DEFINE', '', consts[q])
    # Remove unnecessary spaces (duplicates)
    consts[q] = " ".join(consts[q].split())
    print('Constants: ', consts)  # Debug

for i in range(len(lines)):  # PASS 1: do PER LINE replacements
    # replace '...' occurances with corresponding ASCII code(s)
    while(lines[i].find('\'') != -1):
        k = lines[i].find('\'')
        l = lines[i].find('\'', k+1)
        if k != -1 and l != -1:
            replaced = ''
            for c in lines[i][k+1:l]:
                replaced += str(ord(c)) + ' '
            lines[i] = lines[i][0:k] + replaced + lines[i][l+1:]
        else:
            break

    # replace commas with spaces
    lines[i] = lines[i].replace(',', ' ')

    # **************************************************************************
    # Method of replacing (Instructions + Argument) by a fixed name for each
    # instruction - Rudimentary Method
    # **************************************************************************

    # ========== Adjusts Instructions as defined in opCodes ===========
    # Remove unnecessary spaces (duplicates)
    lines[i] = " ".join(lines[i].split())
    print('Line:', i+1, lines[i], end=' ')  # For Debug purpose

    # Only for put hex numbers with "x" in lowercase. It is not necessary
    lines[i] = lines[i].replace('X', 'x')

    if (len(lines) >= count):  # Creates a copy of all valid instructions to
                               # show them on right side of hex codes
        if one_cycle == 0:
            inst = lines[:]  # At first pass, creates a copy of list lines[:]
            one_cycle = 1
        inst[i] = re.sub(';.*', '', inst[i])  # Deletes all comment characters
                                              # and all that comes after it.
        # Remove unnecessary spaces (duplicates)
        inst[i] = " ".join(inst[i].split())
        # Replaces "comma plus space" and "space plus comma" with comma
        # (for better visualization)
        # Replaces "comma plus space" to ","
        inst[i] = inst[i].replace(', ', ',')
        inst[i] = inst[i].replace(' ,', ',')  # Replaces space plus comma" to ,
        #inst[i] = inst[i].upper()  # Change all strings in list to uppercase
        inst[i] = inst[i].replace('X', 'x')  # Change hex numbers with "x" to
                                             # lowercase
        count = count + 1  # Until the last line

    # Delete all #defines, variable name and value from the lines[:] list
    lines[i] = re.sub(r'(\#DEFINE \w.*)', '', lines[i])

    # Replace constants names from #define directive by the corresponding values
    for l in range(len(consts)):
        # Gets the name of the constant
        const_name = consts[l].rpartition('$')[0]
        # Gets the value of the constant
        var_name = consts[l].rpartition('$')[2]
        # Remove unnecessary spaces (duplicates) from the Name of Constant to
        # match the replace function
        const_name = " ".join(const_name.split())
        lines[i] = lines[i].replace(const_name, var_name)
        #print("Changing....", lines[i])  # Debug

    #lines[i] = lines[i].upper()  # Change all strings in list to uppercase to
                                  # match with valid string for Instructions

    # ==========================================================================
    # Lets you use &H or &L to load the high or low nibble value of a char into
    # a register. It's nice to work with a text LCD.
    # Example 1: LDI ACC, &Ha ; Loads into ACC the high nibble of char 'a'
    # Example 2: LDI ACC, &La ; Loads into ACC the low nibble of char 'a'
    #
    if lines[i].find('&') != -1:
        if lines[i].find('H') != -1:
            lines[i] = re.sub(r'&\w', '', lines[i]) # Remove &H chars
            # Remove unnecessary spaces (duplicates)
            lines[i] = " ".join(lines[i].split())
            #HighNibble = format(ord(lines[i].split()[2]) >> 4 & 0xf, 'x')
            chnum = len(lines[i]) # Gets the number of characters of the current
                                  # instruction.
                                  # LDIACC n => more than 6 characters
                                  # OUTx n => equal to 6 characters
            if (chnum > 6):
                HighNibble = format(ord(lines[i].split()[2]) >> 4 & 0xf, '')
            else:
                HighNibble = format(ord(lines[i].split()[1]) >> 4 & 0xf, '')

            # At the beginning of Instruction, skips all strings except the last
            # one, which matches to the character's nibble in hex code.
            lines[i] = lines[i][0:len(lines[i])-1] + HighNibble # LDI ACC + char

        elif lines[i].find('L') != -1:
            lines[i] = re.sub(r'&\w', '', lines[i]) # Remove &L chars
            # Remove unnecessary spaces (duplicates)
            lines[i] = " ".join(lines[i].split())
            #LowNibble = format(ord(lines[i].split()[2]) & 0xf, 'x')
            chnum = len(lines[i]) # Gets the number of characters of the Current
                                  # instruction.
            if (chnum > 6):
                LowNibble = format(ord(lines[i].split()[2]) & 0xf, '')
            else:
                LowNibble = format(ord(lines[i].split()[1]) & 0xf, '')
            lines[i] = lines[i][0:len(lines[i])-1] + LowNibble # LDI ACC + char

    # ==========================================================================

    lines[i] = lines[i].upper()  # Change all strings in list to uppercase to
                                 # match with valid string for Instructions

    # --------------------------------------------------------------------------
    # Addressing Mode => AMODE = 0 (MA = MAddr, LA = LAddr)
    # --------------------------------------------------------------------------
    # LDI ACC, n
    LDIACC_strs = r'(LDI ACC \$)|(LDI ACC)'  # Valid Strings for LDI ACC
    lines[i] = re.sub(LDIACC_strs, 'LDIACC ', lines[i])  # LDI ACC

    # LDI RA, n
    LDIRA_strs = r'(LDI RA \$)|(LDI RA)'  # Valid Strings for LDI RA
    lines[i] = re.sub(LDIRA_strs, 'LDIRA ', lines[i])  # LDI RA

    # LDI RB,n
    LDIRB_strs = r'(LDI RB \$)|(LDI RB)'  # Valid Strings for LDI RB
    lines[i] = re.sub(LDIRB_strs, 'LDIRB ', lines[i])  # LDI RB

    # LDI RC, n
    LDIRC_strs = r'(LDI RC \$)|(LDI RC)'  # Valid Strings for LDI RC
    lines[i] = re.sub(LDIRC_strs, 'LDIRC ', lines[i])  # LDI RC

    # First, change 'NAND ACC' to 'NANDACC'
    lines[i] = re.sub(r'(NAND ACC)', 'NANDACC', lines[i])

    # NAND ACC, n
    lines[i] = re.sub(r'(NANDACC \$)|(NAND ACC )', 'NANDACC ', lines[i])

    # NAND ACC, RA
    lines[i] = re.sub(r'NANDACC RA$', 'NANDACCRA ' + '0', lines[i])

    # NAND ACC, RB
    lines[i] = re.sub(r'(NANDACC RB$)', 'NANDACCRB ' + '0', lines[i])

    # NAND ACC, RAM[RC:MAddr:LAddr] (passes argument 1)
    lines[i] = re.sub(r'NANDACC @(\d.*)', r'NANDACCRAM \1', lines[i])

    # First, change 'LDW ACC' to 'LDWACCRAM'
    lines[i] = re.sub(r'(LDW ACC)', 'LDWACC', lines[i])

    # LDW ACC, RAM[RC:MAddr:LAddr] (passes argument 1)
    lines[i] = re.sub(r'LDWACC @(\d.*)', r'LDWACCRAM \1', lines[i])

    # LDA RA
    lines[i] = lines[i].replace('LDA RA', 'LDARA ' + '0')

    # LDA RB
    lines[i] = lines[i].replace('LDA RB', 'LDARB ' + '0')

    # LDA RC
    lines[i] = lines[i].replace('LDA RC', 'LDARC ' + '0')

    # OUTA n
    OUTAn_strs = r'(OUTA \$)|(OUTA \b)'  # Valid Strings for OUTA n
    lines[i] = re.sub(OUTAn_strs, 'OUTA ', lines[i])  # OUTA n

    # OUTA ACC
    OUTAACC_strs = r'(\bOUTA\sACC\b)'  # Valid Strings for OUTA ACC
    lines[i] = re.sub(OUTAACC_strs, 'OUTAACC ' + '0', lines[i])  # OUTA ACC

    # OUTA RA
    OUTARA_strs = r'(OUTA RA)'  # Valid Strings for OUTA RA
    lines[i] = re.sub(OUTARA_strs, 'OUTARA ' + '0', lines[i])  # OUTA RA

    # OUTA RAM[RC:MAddr:LAddr]
    OUTARAM_strs = r'OUTA @(\d.*)'  # Valid Strings for OUTA RAM
    lines[i] = re.sub(OUTARAM_strs, r'OUTARAM \1', lines[i])  # OUTA RAM

    # OUTB n
    OUTBn_strs = r'(OUTB \$)|(OUTB \b)'  # Valid Strings for OUTB n
    lines[i] = re.sub(OUTBn_strs, 'OUTB ', lines[i])  # OUTB n

    # OUTB ACC
    OUTBACC_strs = r'(\bOUTB\sACC\b)'  # Valid Strings for OUTB ACC
    lines[i] = re.sub(OUTBACC_strs, 'OUTBACC ' + '0', lines[i])  # OUTA ACC

    # OUTB RA
    OUTBRA_strs = r'(OUTB RA)'  # Valid Strings for OUTB RA
    lines[i] = re.sub(OUTBRA_strs, 'OUTBRA ' + '0', lines[i])  # OUTB RA

    # OUTB RAM[RC:MAddr:LAddr]
    OUTBRAM_strs = r'OUTB @(\d.*)'  # Valid Strings for OUTB RAM
    lines[i] = re.sub(OUTBRAM_strs, r'OUTBRAM \1', lines[i])  # OUTB RAM

    # OUTC n
    OUTCn_strs = r'(OUTC \$)|(OUTC \b)'  # Valid Strings for OUTC n
    lines[i] = re.sub(OUTCn_strs, 'OUTC ', lines[i])  # OUTC n

    # OUTC ACC
    OUTCACC_strs = r'(\bOUTC\sACC\b)'  # Valid Strings for OUTC ACC
    lines[i] = re.sub(OUTCACC_strs, 'OUTCACC ' + '0', lines[i])  # OUTC ACC

    # OUTC RA
    OUTCRA_strs = r'(OUTC RA)'  # Valid Strings for OUTC RA
    lines[i] = re.sub(OUTCRA_strs, 'OUTCRA ' + '0', lines[i])  # OUTC RA

    # OUTC RAM[RC:MAddr:LAddr]
    OUTCRAM_strs = r'OUTC @(\d.*)'  # Valid Strings for OUTC RAM
    lines[i] = re.sub(OUTCRAM_strs, r'OUTCRAM \1', lines[i])  # OUTC RAM

    # OUTD n
    OUTDn_strs = r'(OUTD \$)|(OUTD \b)'  # Valid Strings for OUTD n
    lines[i] = re.sub(OUTDn_strs, 'OUTD ', lines[i])  # OUTD n

    # OUTD ACC
    OUTDACC_strs = r'(\bOUTD\sACC\b)'  # Valid Strings for OUTD ACC
    lines[i] = re.sub(OUTDACC_strs, 'OUTDACC ' + '0', lines[i])  # OUTD ACC

    # OUTD RA
    OUTDRA_strs = r'(OUTD RA)'  # Valid Strings for OUTD RA
    lines[i] = re.sub(OUTDRA_strs, 'OUTDRA ' + '0', lines[i])  # OUTD RA

    # OUTD RAM[RC:MAddr:LAddr]
    OUTDRAM_strs = r'OUTD @(\d.*)'  # Valid Strings for OUTD RAM
    lines[i] = re.sub(OUTDRAM_strs, r'OUTDRAM \1', lines[i])  # OUTD RAM

    # LDR RA
    lines[i] = lines[i].replace('LDR RA', 'LDRRA ' + '0')

    # LDR RB
    lines[i] = lines[i].replace('LDR RB', 'LDRRB ' + '0')

    # LDR RC
    lines[i] = lines[i].replace('LDR RC', 'LDRRC ' + '0')

    # First, change 'CMP ACC' to 'CMPACC'
    lines[i] = re.sub(r'(CMP ACC)', 'CMPACC', lines[i])

    # CMP ACC, n
    lines[i] = re.sub(r'(CMPACC \$)|(CMPACC )', r'CMPACC ', lines[i])

    # CMP ACC, RA
    lines[i] = re.sub(r'CMPACC RA$', 'CMPACCRA ' + '0', lines[i])

    # CMP ACC, RB
    lines[i] = re.sub(r'CMPACC RB$', 'CMPACCRB ' + '0', lines[i])

    # CMP ACC, RAM[RC:MAddr:LAddr] (passes argument 1)
    lines[i] = re.sub(r'CMPACC @(\d.*)', r'CMPACCRAM \1', lines[i])

    # STW RAM[RC:MAddr:LAddr], ACC (passes argument 1)
    lines[i] = re.sub(r'STW @(\d.*) ACC', r'STWRAMACC \1', lines[i])

    # First, change 'SUB ACC' to 'SUBACC'
    lines[i] = re.sub(r'(SUB ACC)', 'SUBACC', lines[i])

    # SUB ACC, n
    lines[i] = re.sub(r'(SUBACC \$)|(SUBACC )', r'SUBACC ', lines[i])

    # SUB ACC, RA
    lines[i] = re.sub(r'SUBACC RA$', 'SUBACCRA ' + '0', lines[i])

    # SUB ACC, RB
    lines[i] = re.sub(r'SUBACC RB$', 'SUBACCRB ' + '0', lines[i])

    # SUB ACC, RAM[RC:MAddr:LAddr] (passes argument 1)
    lines[i] = re.sub(r'SUBACC @(\d.*)', r'SUBACCRAM \1', lines[i])

    # First, change 'ADD ACC' to 'ADDACC'
    lines[i] = re.sub(r'(ADD ACC)', 'ADDACC', lines[i])

    # ADD ACC, n
    lines[i] = re.sub(r'(ADDACC \$)|(ADDACC )', r'ADDACC ', lines[i])

    # ADD ACC, RA
    lines[i] = re.sub(r'ADDACC RA$', 'ADDACCRA ' + '0', lines[i])

    # ADD ACC, RB
    lines[i] = re.sub(r'ADDACC RB$', 'ADDACCRB ' + '0', lines[i])

    # ADD ACC, RAM[RC:MAddr:LAddr] (passes argument 1)
    lines[i] = re.sub(r'ADDACC @(\d.*)', r'ADDACCRAM \1', lines[i])

    # INA ACC
    INAACC_strs = r'(^INA\sACC$)|(^INA$)'  # Valid Strings for INA ACC
    lines[i] = re.sub(INAACC_strs, 'INAACC ' + '0', lines[i])  # INA ACC

    # INB ACC
    INBACC_strs = r'(^INB\sACC$)|(^INB$)'  # Valid Strings for INB ACC
    lines[i] = re.sub(INBACC_strs, 'INBACC ' + '0', lines[i])  # INB ACC

    # INC ACC
    INCACC_strs = r'(^INC\sACC$)|(^INC$)'  # Valid Strings for INC ACC
    lines[i] = re.sub(INCACC_strs, 'INCACC ' + '0', lines[i])  # INC ACC

    # IND ACC
    INDACC_strs = r'(^IND\sACC$)|(^IND$)'  # Valid Strings for IND ACC
    lines[i] = re.sub(INDACC_strs, 'INDACC ' + '0', lines[i])  # IND ACC

    # --------------------------------------------------------------------------
    # Instructions to be used with Indirect Address Mode, AMODE = 1
    # (MA = RB, LA = RA). High address is always in RC.
    # The indirect Address Mode should be indicated by @R
    # --------------------------------------------------------------------------
    # CMP ACC, RAM[RC:RB:RA]
    lines[i] = re.sub(r'NANDACC (@R)$', 'NANDACCRAMREG ' + '0', lines[i])

    # LDW ACC, RAM[RC:RB:RA]
    lines[i] = re.sub('LDWACC (@R)$', 'LDWACCRAMREG ' + '0', lines[i])

    # OUTA RAM[RC:RB:RA]
    OUTARAMR_strs = r'(OUTA (@R)$)'  # Valid Strings for OUTA RAM
    lines[i] = re.sub(OUTARAMR_strs, 'OUTARAMERG ' + '0', lines[i])  # OUTA RAM

    # OUTB RAM[RC:RB:RA]
    OUTBRAMR_strs = r'(OUTB (@R)$)'  # Valid Strings for OUTB RAM
    lines[i] = re.sub(OUTBRAMR_strs, 'OUTBRAMERG ' + '0', lines[i])  # OUTB RAM

    # OUTC RAM[RC:RB:RA]
    OUTCRAMR_strs = r'(OUTC (@R)$)'  # Valid Strings for OUTC RAM
    lines[i] = re.sub(OUTCRAMR_strs, 'OUTCRAMERG ' + '0', lines[i])  # OUTC RAM

    # CMP ACC, RAM[RC:RB:RA]
    lines[i] = re.sub(r'CMPACC (@R)$', 'CMPACCRAMREG ' + '0', lines[i])

    # OUTD RAM[RC:RB:RA]
    OUTDRAMR_strs = r'(OUTD (@R)$)'  # Valid Strings for OUTD RAM
    lines[i] = re.sub(OUTDRAMR_strs, 'OUTDRAMERG ' + '0', lines[i])  # OUTD RAM

    # STW RAM[RC:RB:RA], ACC
    lines[i] = re.sub(r'STW @(R) (ACC)$', 'STWRAMACCREG ' + '0', lines[i])

    # SUB ACC, RAM[RC:RB:RA]
    lines[i] = re.sub(r'SUBACC @(R)', 'SUBACCRAMREG ' + '0', lines[i])

    # JPI [RC:RB:RA]
    lines[i] = re.sub(r'JPI @(R)', 'JPIREG ' + '0', lines[i])

    # JPC [RC:RB:RA]
    lines[i] = re.sub(r'JPC @(R)', 'JPCREG ' + '0', lines[i])

    # JPZ [RC:RB:RA]
    lines[i] = re.sub(r'JPZ @(R)', 'JPZREG ' + '0', lines[i])

    # ADD ACC, RAM[RC:RB:RA]
    lines[i] = re.sub(r'ADDACC @(R)', 'ADDACCRAMREG ' + '0', lines[i])
    # ==== End of Instructions =====

    # generate a separate lineinfo
    lineinfo.append(LINEINFO_NONE)
    if lines[i].find('#begin') != -1:
        lineinfo[i] |= LINEINFO_BEGIN
        lines[i] = lines[i].replace('#begin', '')

    if lines[i].find('#end') != -1:
        lineinfo[i] |= LINEINFO_END
        lines[i] = lines[i].replace('#end', '')

    k = lines[i].find('#ORG')
    if (k != -1):
        s = lines[i][k:].split()  # split from #org onwards
        # use element after #org as origin address
        lineinfo[i] |= LINEINFO_ORG + int(s[1], 0)
        # join everything before and after the #org ... statement
        lines[i] = lines[i][0:k].join(s[2:])

    if lines[i].find(':') != -1:
        # put label with it's line number into dictionary
        labels[lines[i][:lines[i].find(':')]] = i
        lines[i] = lines[i][lines[i].find(':')+1:]  # cut out the label

    # now split line into list of bytes (omitting whitepaces)
    lines[i] = lines[i].split()
    print('=>', lines[i])  # For Debug purpose

    # iterate from back to front while inserting stuff
    for j in range(len(lines[i])-1, -1, -1):
        try:
            # try replacing mnemonic with opcode
            lines[i][j] = opCodes[lines[i][j]]  #

        except:
            # replace '0xWORD' with 'LSB MSB'
            if lines[i][j].find('0x') == 0 and len(lines[i][j]) > 4:
                val = int(lines[i][j], 16)
                lines[i][j] = str(val & 0xff)
                lines[i].insert(j+1, str((val >> 8) & 0xff))

adr = 0  # PASS 2: default start address
for i in range(len(lines)):
    # iterate from back to front while inserting stuff
    for j in range(len(lines[i])-1, -1, -1):
        e = lines[i][j]
        if e[0] == '<' or e[0] == '>' or e[0] == '[' or e[0] == ']':
            continue  # only one byte is required for this label
        if e.find('+') != -1:
            e = e[0:e.find('+')]  # omit +/- expressions after a label
        if e.find('-') != -1:
            e = e[0:e.find('-')]
        try:
            labels[e]
            # is this element a label? => add a placeholder for the MSB
            #lines[i].insert(j+1, '0x@@')  # Label with 2 bytes
        except:
            pass
    if lineinfo[i] & LINEINFO_ORG:
        adr = lineinfo[i] & 0xffff   # react to #org by resetting the address
    lineadr.append(adr)  # save line start address
    # advance address by number of (byte) elements
    adr += len(lines[i]) // 2  # Compute as Word (16 bits => 2 bytes)

for l in labels:
    # update label dictionary from 'line number' to 'address'
    labels[l] = lineadr[labels[l]]
    #print('First Label', list(labels)[(len(labels))-(len(labels))])  # Debug
    #print('Final Label', list(labels)[len(labels)-1])  # Debug

    # Check for the First Label and print blank line
    if l == list(labels)[(len(labels))-(len(labels))]:
        print('')  # Print blank line (for better visualization)

    print('Label Address: ', l, '=> ', hex(labels[l]))  # For Debug purpose

    # Check for the final Label and print a blank line
    if l == list(labels)[len(labels)-1]:
        print('')  # Print blank line (for better visualization)

# PASS 3: replace 'reference + placeholder' with 'MSB LSB'
for i in range(len(lines)):
    for j in range(len(lines[i])):
        e = lines[i][j]
        pre = ''
        off = 0
        if e[0] == '<' or e[0] == '>' or e[0] == '[' or e[0] == ']':
            pre = e[0]
            e = e[1:]
        if e.find('+') != -1:
            off += int(e[e.find('+')+1:], 0)
            e = e[0:e.find('+')]
        if e.find('-') != -1:
            off -= int(e[e.find('-')+1:], 0)
            e = e[0:e.find('-')]
        try:
            adr = labels[e] + off
            #if pre == '&':
            # 1o Nibble of the address label
            #lines[i][j] = str(adr & 0x0)
            if pre == ']':
                lines[i][j] = str(adr & 0xf)  # 1o Nibble of the address label
            elif pre == '<':
                # 2nd Nibble of the addr label
                lines[i][j] = str((adr >> 4) & 0xf)
            elif pre == '>':
                # 3rd nibble of the addr label
                lines[i][j] = str((adr >> 8) & 0xf)
            elif pre == '[':
                # 4th nibble of the addr label
                lines[i][j] = str((adr >> 12) & 0xf)
            else:
                # If the address nibble is not especified, the instructions is a
                # jump, so calculate MAddr and LAddr
                lines[i][j] = str(adr & 0xff)  # Compute MAddr and LAddr
        except:
            pass
        try:
            # check if ALL elements are numeric
            int(lines[i][j], 0)
        except:
            print('ERROR in line ' + str(i+1)
                  + ': Undefined expression \'' + lines[i][j] + '\'')
            exit(1)

for i in range(len(lines)):	 # print out the result
   s = ('%04.4x' % lineadr[i]) + ": "
   for e in lines[i]:
       s += ('%02.2x' % (int(e, 0) & 0xff)) + ''
   if lines[i] != []:  # Print only non empty lines (valid instructions)
       # Search for lineadr equal to label and print it
       if lineadr[i] in labels.values():
          val = (list(labels.keys())[list(labels.values()).index(lineadr[i])])
          print(val+':')  # Print the Label at the corresponding address

       print(s, end=' ')  # Print Address and Hex Codes for valid Instructions
       num_inst = num_inst + 1
       print(inst[i])  # Print the text Instructions (like in source file)
       if (i == len(lines)-1):  # Are all lines completed?
           print('')  # Print blank line

insert = ''
showout = True  # print out the hex code result (group of 16 codes per line)
for i in range(len(lines)):
    if lineinfo[i] & LINEINFO_BEGIN:
        showout = True
    if lineinfo[i] & LINEINFO_END:
        showout = False
    if showout:
        if lineinfo[i] & LINEINFO_ORG:
            if insert:
                #print(':' + insert)
                print(insert)
                insert = ''
            print('R' + '%04.4x' % (lineinfo[i] & 0xffff)) # Reset Address

        if i == 0:
            print('')  # Print blank line
            print('Code to be transferred to the MikroLeo (using Arduino):')
            #break

        for e in lines[i]:
            # Print 4 nibble + comma + 1 space (standard Arduino-Mikroleo)
            if tmp == 1:  # <= 1
                insert += ('%2.2x' % (int(e, 0) & 0xff)) + ',' + ' '  # 4 bytes
                tmp = 0
            else:
                #insert += ('%2.2x' % (int(e, 0) & 0xff))
                insert += ('0x%2.2x' % (int(e, 0) & 0xff))
                tmp = tmp + 1
            #print('Max. ' + str(max(range(len(lines)))))
            #print('i: ' + str(i))
            if len(insert) >= 32*4 - 1:  # Print 16 datas at current line
                if max(range(len(lines))) - i > 15:  # Print lines with 16 datas
                    print(insert)
                    insert = ''

if insert:  # Print the rest of data (last line with less than 16 datas)
    print(insert[:-2])  # Print the hex code without the last comma
    #print('Constants 02:', consts)  # Debug

insert = ''
showout = True  # print out the binary code result (group of 16 codes per line)
for i in range(len(lines)):
    if lineinfo[i] & LINEINFO_BEGIN:
        showout = True
    if lineinfo[i] & LINEINFO_END:
        showout = False
    if showout:
        if lineinfo[i] & LINEINFO_ORG:
            if insert:
                print(':' + insert)
                insert = ''
            #print('%04.4x' % (lineinfo[i] & 0xffff))

        if i == 0:
            print('')  # Print blank line
            print('Binary code to be manually programmed:')
            #break

        for e in lines[i]:
            # Print 4 nibble + comma + 1 space
            if tmp == 1:  # <= 1
                #print(format(int(e, 0), '08b'))  # Print bin code (LSB)
                tmp = 0
            else:
                s = ('%04.4x' % lineadr[i]) + ":"  # Current Address
                #print(s, end=" ")  # Print Address

                # Print the bin code (MSB)
                #print(format(int(e, 0), '08b'), end=" ")
                tmp = tmp + 1

            if len(insert) >= 1*1 - 1:  # Print 16 datas at current line
                insert = ''

if insert:  # Print the rest of data (last line)
    print(int((insert)))
    #print('Constants 02:', consts)  # Debug

if (i == len(lines)-1):  # Is all lines Finished ?
    print('')  # Print blank line
    print(num_inst, 'Instructions were coded! (MikroLeo v0.19)')
    print('')  # Print blank line


#*******************************************************************************
# Generate hex file to be loaded into the Program Memory in Digital Simulation
# Output: sourcefilename_Micro2.hex (ROMH)
# Digital file: MikroLeo_v0.19.dig
insert = ''
showout = True  # print out the result (group of 16 codes per line)
for i in range(len(lines)):
    if lineinfo[i] & LINEINFO_BEGIN:
        showout = True
    if lineinfo[i] & LINEINFO_END:
        showout = False
    if showout:
        if lineinfo[i] & LINEINFO_ORG:
            if insert:
                #print(':' + insert)
                print(insert)
                insert = ''
            #print('%04.4x' % (lineinfo[i] & 0xffff))

        if i == 0:
            print('Code to be loaded into the Program Memory Micro2 (ROMH) on'
                  ' the software Digital:')
            print('v2.0 raw')

            # Get file name and add to the name Micro2 and change the extension
            # to .hex
            file_name_M2 = re.sub(
                r'(.*)\.(\w+)', r'\1_Micro2.hex', sys.argv[1])
            # Open the file for Micro2 in write mode
            with open(file_name_M2, 'w') as file_object:
                file_object.write('v2.0 raw' + '\n')  # Writes the Head file
                #pass

        for e in lines[i]:
            # Print 2 nibble (standard for Digital-hnemman-MikroLeo)
            if tmp2 >= 2:  # <= 1
                tmp2 = 0
            else:
                insert += ('%2.2x' % (int(e, 0) & 0xff)) + ' '  # 2 bytes
                tmp2 = tmp2 + 2
            if len(insert) >= 24*4 - 1:  # Print 16 datas at current line
                # Write data to .hex Micro2 file
                with open(file_name_M2, 'a') as file_object:
                    file_object.write(insert + '\n')
                print(insert)
                insert = ''

if insert:  # Print the rest of data (last line)
    print(insert)
    # Write the rest of data to .hex Micro2 file
    with open(file_name_M2, 'a') as file_object:
        file_object.write(insert)
print('')  # Blank line
# ******************************************************************************

# ******************************************************************************
# Generate hex files to be loaded into the Program Memory in Digital Simulation
# Output: sourcefilename_Micro1.hex (ROML)
insert = ''
showout = True  # print out the result (group of 16 codes per line)
for i in range(len(lines)):
    if lineinfo[i] & LINEINFO_BEGIN:
        showout = True
    if lineinfo[i] & LINEINFO_END:
        showout = False
    if showout:
        if lineinfo[i] & LINEINFO_ORG:
            if insert:
                #print(':' + insert)
                print(insert)
                insert = ''
            #print('%04.4x' % (lineinfo[i] & 0xffff))

        if i == 0:
            print('Code to be loaded into the Program Memory Micro1 (ROML) on'
                  ' the software Digital:')
            print('v2.0 raw')

            # Get file name and add to the name Micro1 and change the extension
            # to .hex
            file_name_M1 = re.sub(
                r'(.*)\.(\w+)', r'\1_Micro1.hex', sys.argv[1])
            # Open the file for Micro1 in write mode
            with open(file_name_M1, 'w') as file_object:
                file_object.write('v2.0 raw' + '\n')  # Writes the Head file
                #pass

        for e in lines[i]:
            # Print 4 nibble + comma + 1 space (standard Arduino-MikroLeo)
            if tmp3 == 0:  # <= 1
                #insert += ('%2.2x' % (int(e, 0) & 0xff)) + ' '  # 4 bytes
                tmp3 = tmp3 + 1
            else:
                insert += ('%2.2x' % (int(e, 0) & 0xff)) + ' '
                tmp3 = 0
            if len(insert) >= 24*4 - 1:  # Print 16 datas at current line
                # Write data to .hex Micro1 file
                with open(file_name_M1, 'a') as file_object:
                    file_object.write(insert + '\n')
                print(insert)
                insert = ''

if insert:  # Print the rest of data (last line)
    print(insert)
    # Write the rest of data to .hex Micro1 file
    with open(file_name_M1, 'a') as file_object:
        file_object.write(insert)
print('')  # Blank line

print('Files to be loaded into Program Memory (Micro2 and Micro1):', '\n',
      file_name_M2, '\n', file_name_M1)
# ******************************************************************************

# ------------------------------------------------------------------------------
# "Assembler" for MikroLeo 4-bit Microcomputer v0.19
# Copyrigh (c) 2022 Edson Junior Acordi
# ------------------------------------------------------------------------------
