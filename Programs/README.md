### Summary of the main features of the phyton assembler for the MikroLeo:  

@ is used to indicate a RAM address. 

Decimal or hexadecimal immediate values could be used directly as 5 or 0xd.  

The $ could be used to indicate an immediate value that can be decimal (e.g. $5) or hexadecimal (e.g. $0xd).  

@R is used to indicate that an address is composed by RC:RB:RA (AMODE=1, indirect address mode).  

All text that comes after semicolon is a comment.  

All text that comes before : is a Label that will be converted into an address.  

The assembler is not case-sensitive, so, for example, ACC is equal to AcC.  

Constants could be defined by the directive #define, for example, #define Const1 $0  

In the same way, to define a hexadecimal constant, #define Const2 $0xA  

Note that the $ symbol must be used to define a constant.  

The address of a label could be loaded into a register by the use of characters '[', '>', '<' and ']'.  
To remember this, think about an address with 4 nibble as [><].  
Thus, to load the least significant nibble, ] is used.  
To load the next nibble, < is used and so on.  

For example, to load the penultimate nibble from the label TEST into the RC register:  
LDI RC,>TEST  

Pay attention with the labels because the assembler does not verify if there is duplicated label.  
