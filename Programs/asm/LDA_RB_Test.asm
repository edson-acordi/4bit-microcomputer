; Code for instruction test
; MikroLeo v0.19 - Rev. 1.0A

Loop:
	LDI RB,0   ; Loads RB with operand
	LDA RB     ; Loads contents of RB into the Accumulator
	CMP ACC,RB ; Compare ACC with RB
	JPZ VAL1   ; If ACC is equal to RB, jumps to the specified label 
	JPI ERRO   ; If not, signalize that an error occurred
VAL1:
	LDI RB,9
	LDA RB
	CMP ACC,RB
	JPZ VAL2
	JPI ERRO
VAL2:
	LDI RB,0xB
	LDA RB
	CMP ACC,RB
	JPZ VAL3
	JPI ERRO
VAL3:
	LDI RB,0xF ; Last test
	LDA RB
	CMP ACC,RB ; Compare ACC with RB
	JPZ END    ; If ACC is equal to RB, jumps to the specified label 
	OUTA 1     ; If not, signalize that an error occurred
	JPI ERRO   ; Jumps to the error label
END:
	JPI Loop   ; Tests ok, so, repeat it
ERRO:
	JPI ERRO   ; Hangs the execution
	
