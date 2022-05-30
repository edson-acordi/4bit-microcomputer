; Code for instruction test
; MikroLeo v0.19 - Rev. 1.0A

Loop:
	LDI ACC,1 ; Loads ACC with operand
	JPI Loop  ; Jump to the label
	
