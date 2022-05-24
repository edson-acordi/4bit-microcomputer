; Code for instruction test
; MikroLeo v0.19 - Rev. 1.0A

Loop:
	LDI RC,1 ; Loads RC with operand
	LDA RC   ; Loads the contents of RC into the Accumulator
	LDI RC,0
	JPI Loop ; Jump to the label address pointed by [RC:MAddr:LAddr]
	
