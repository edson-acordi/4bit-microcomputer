; -----------------------------------
; Where is the stack in the MikroLeo?
; -----------------------------------
; Code example for implementing a simple subroutine
; (1-level Stack) using indirect addressing
;
; Edson Junior Acordi
; December 25, 2022
; -----------------------------------

; ==== Defines the initial address of the Stack ====
#DEFINE STACK_ADDR $0x7 ; High nibble of initial Stack address in RAM (used with RC).

; Initial Stack Address:
; Stack = RC:MAddr:LAddr = 0x700
;         |    |     |
;         |    |     +---> Low nibble
;         |    +---------> Medium nibble
;         +--------------> High nibble

; Note:
; RAM Address 0x700 => To save the ACC content
; RAM Address 0x701 => To save the RA content
; RAM Address 0x702 => To save the RB content
; RAM Address 0x703 => To save the least significant nibble of the subroutine's return address
; RAM Address 0x704 => To save the medium nibble of the subroutine's return address 
; RAM Address 0x705 => To save the most significant nibble of the subroutine's return address
;               |||
;               ||+---> LAddr
;               |+----> MAddr
;               +-----> RC
; =======================================================

INI:
; do anything ... (main program)

; ---- Save Context (ACC, RA e RB) ----
LDI RC, STACK_ADDR ;High Stack address [11:8]
STW @0x00, ACC ;Saves the contents of ACC to the Stack
LDA RA
STW @0x01, ACC ;Save the contents of RA to the Stack
LDA RB
STW @0x02, ACC ;Save the contents of RB to the Stack
; ----------------------------------------

; ---- Salva Return Address (PUSH PC) ----
LDI ACC, ]RET0 ;Get the low address [3:0]
STW @0x03, ACC
LDI ACC, <RET0 ;Get the medium address [7:4]
STW @0x04, ACC
LDI ACC, >RET0 ;Get the high address [11:8]
STW @0x05, ACC
; ---------------------------------------------

; ---- Call the subroutine (CALL) ----
LDI RC, >SUBROUT0 ;Get the high address of the subroutine [11:8]
LDI RB, <SUBROUT0 ;Get the medium address of the subroutine [7:4]
LDI RA, ]SUBROUT0 ;Get the low address of the subroutine [3:0]
JPI @R ;Call the SUBROUT0
; ----------------------------------

; ---- Subroutine Return Point ----
RET0:
; Restore the Context
LDI RC, STACK_ADDR ;High stack address [11:8]
LDW ACC, @0x02 ;Get the content of RB
LDR RB
LDW ACC, @0x01 ;Get the content of RA
LDR RA
LDW ACC, @0x00 ;Get the content of ACC
; ---------------------------------------

; Continue executing the main program’s instructions after the subroutine returns
; ...
LDI RC, >INI ;Obtém o endereço alto do label INI [11:8]
JPI INI

; ========================================================
; ---- Subroutine ----
SUBROUT0:
; do anything ... (subroutine code)

; Restore the Return Address (POP PC)
LDI RC, STACK_ADDR ;Required if RC has been modified
LDW ACC, @0x03 ;Gets the low return address
LDR RA
LDW ACC, @0x04 ;Gets the medium return address
LDR RB
LDW ACC, @0x05 ;Gets the high return address
LDR RC

; Returns from the Subroutine (RET)
JPI @R ;Returns to address RET0
; ========================================================


