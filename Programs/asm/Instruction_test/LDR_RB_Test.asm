; Code for instruction test
; MikroLeo v0.19 - Rev. 1.0A

Loop:
	LDI ACC,0xE ; Loads ACC with operand
	LDR RB      ; Loads RB with the contents of the Accumulator
	CMP ACC,RB  ; Compares ACC with RB
	JPZ VAL1    ; If ACC is equal to RB, jumps to the specified label 
	JPI ERRO    ; If not, jumps to the specified label
VAL1:
	LDI ACC,0xA
	LDR RB
	CMP ACC,RB
	JPZ VAL2
	JPI ERRO
VAL2:
	LDI ACC,5
	LDR RB
	CMP ACC,RB
	JPZ VAL3
	JPI ERRO
VAL3:
	LDI ACC,2
	LDR RB
	CMP ACC,RB
	JPZ Loop    ; Tests ok, so, repeat it
	JPI ERRO

ERRO:
	OUTA 1      ; Signalize that an error occurred
ERRO2:	
	JPI ERRO2   ; Hangs the execution
	
