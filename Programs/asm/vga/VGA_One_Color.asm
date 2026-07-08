; ======================================================================================
; MikroLeo Basic VGA Driver v0.1
; May 03, 2026
; Edson Junior Acordi
; This code fills the screen of a 640×480 VGA monitor with a single color
; ======================================================================================
; Clock: 3MHz | HSYnc: 31.25 kHz | VSync: 59.52 Hz | MikroLeo Horizontal Pixel width: 8
; Effective horizontal pixels: 76
; Equivalent VGA horizontal line: 608 pixels
;
; VGA Output:
; OUTB[0]   = HSync Pulse (VGA monitor pin 13)
; OUTC[0]   = VSync Pulse (VGA monitor pin 14)
; OUTD[2:0] = Pixel Data, RGB of 1-bit, 8 colors (VGA monitor pins 1, 2 and 3)
;
; Important:
; - Use a 68 Ohms resistor between OUTB[0] and pin 13 of the VGA monitor (HSync)
; - Use a 68 Ohms resistor between OUTC[0] and pin 14 of the VGA monitor (VSync)
; - Use a 510 Ohms resistor between OUTD[0] and pin 1 of the VGA monitor (Red)
; - Use a 510 Ohms resistor between OUTD[1] and pin 2 of the VGA monitor (Green)
; - Use a 510 Ohms resistor between OUTD[2] and pin 3 of the VGA monitor (Blue)
;
; HSync and VSync are active at low level
;
; The code is optimized to fit at one page (256 addresses)
;
; MikroLeo VGA Timing:
; ---------------------------
; Horizontal        | Cycles
; ------------------+--------
; Visible Area (D): |  76
; Front Porch (E):  |   2
; Hsync Pulse (B):  |  12
; Back Porch (C):   |   6
; Total Line (A):   |  96
; ---------------------------
;
; ----------------------------------
; Vertical         | Lines | Cycles
; -----------------+-------+--------
; Front Porch (S): |   10  |   960
; VSync (P):       |    2  |   192
; Back Porch (Q):  |   33  |  3168
; Visible (R):     |  480  | 46080
; Total frame (O): |  525  | 50400
; ----------------------------------
;
; During blanking (Front and Back Porch), the RGB signals should be at 0V.
; During HSync or VSync the RGB signals should be at 0V.
;
; ----------------------------------------------------------------------------------
; = Cycles Count =
;
; The cycle count per line is set at 96 cycles across all paths, always occurring
; at the following label addresses:
; V_LOOP_RA:
; VFP_LOOP:
; VSYNC_LOOP:
; VBP_LOOP:
;
; The cycle count per frame is set at 50400 cycles, always occurring at the label
; address:
; VSYNC_SETUP: + 2
; ==================================================================================
; Code details:
; - Counters: Registers RA, RB and memory address 0x00 in page 0

;
; Code blocks:
; VFP_LOOP =>
;

; Definition of Constants
#DEFINE VSyncOff $0b0001
#DEFINE HSyncOff $0b0001
#DEFINE VSyncOn  $0b0000
#DEFINE HSyncOn  $0b0000

; Definition of variables in RAM
#DEFINE LoopOuter $0x00

INIT:
    OUTB HSyncOff ; Turn off the synchronization signals
    OUTC VSyncOff
    OUTD 0x0 ; RGB = black
    NOP ; Wait for signal stabilization
    NOP
    NOP
    NOP

START_FRAME:
; Prepare the Counters to draw 480 visible lines.
; Viseble lines = RA x RB x RAM = 10 x 16 x 3 = 480 lines
; Note that RB is initialized to 0. The trick here is that, since it subtracts 1
; immediately, the value underflows to 15. Therefore, counting from 15 to 0, we
; have 16 iterations.
; Code dynamics:
; - Path 1: For each line drawn, the RA register decreases by 1.
; - Path 2: When it reaches zero (after 10 lines), the code reloads RA with 10
; and decreases RB by 1.
; - Path 3: When RB reaches zero (after RA has reached zero 16 times), it reloads RB and
; decreases LoopOuter in RAM by 1. When LoopOuter reaches zero, the entire 480-line
; screen is finished!

    LDI ACC, 3
    STW @LoopOuter, ACC
    LDI ACC, 0
    LDR RB
    LDI ACC, 10
    LDR RA

; -----------------------------------------------------------------
; 1. VISIBLE AREA (480 Lines)
; -----------------------------------------------------------------
; Path 1: RA > 0
; -----------------
V_LOOP_RA:
    OUTB HSyncOn
    LDI ACC, 2          ; (Mini-loop de 11 ciclos de atraso)
d_hsh_v:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_hsh_v
    JPI d_hsh_v
e_hsh_v:
    NOP
    NOP
    NOP

    OUTB HSyncOff
    NOP
    NOP
    NOP
    NOP
    NOP

    OUTD 0x2 ; RGB = Green
    LDA RA
    SUB ACC, 1 ; Decreases RA counter
    LDR RA
    CMP ACC, 0 ; Test if RA=0
    JPZ CAMINHO_RA_ZERO
    LDI ACC, 0          ; Underflow: 16 iterations
delay_normal:
    SUB ACC, 1
    CMP ACC, 0
    JPZ sai_delay_normal
    JPI delay_normal
sai_delay_normal:
    NOP
    NOP
    NOP
    NOP
    NOP
    NOP
    OUTD 0x0
    JPI V_LOOP_RA

; ------------------
; Path 2: RA = 0
; ------------------
CAMINHO_RA_ZERO:
    LDA RB
    SUB ACC, 1
    LDR RB
    CMP ACC, 0
    JPZ RECARGA_MEMORIA
    LDI ACC, 10
    LDR RA
    LDI ACC, 15
delay2:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_delay2
    JPI delay2
end_delay2:
    NOP
    NOP
    NOP
    OUTD 0x0
    JPI V_LOOP_RA

; ---------------------------
; Path 3: RA = 0 e RB = 0
; ---------------------------
RECARGA_MEMORIA:
    LDW ACC, @LoopOuter
    SUB ACC, 1
    STW @LoopOuter, ACC
    CMP ACC, 0
    JPZ V_FRONT_PORCH
    LDI ACC, 10
    LDR RA
    LDI ACC, 0
    LDR RB
    LDI ACC, 13
delay3:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_delay3
    JPI delay3
end_delay3:
    NOP
    NOP
    NOP
    NOP
    OUTD 0x0
    JPI V_LOOP_RA

V_FRONT_PORCH:
    LDI ACC, 10
    LDR RA
    LDI ACC, 14
delay_exit:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_exit
    JPI delay_exit
end_exit:
    NOP
    NOP
    OUTD 0x0
    JPI VFP_LOOP

; -----------------------------------------------------------------
; 2. VERTICAL FRONT PORCH (10 Lines)
; -----------------------------------------------------------------
VFP_LOOP:
    OUTB HSyncOn
    LDI ACC, 2
d_hsh_f:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_hsh_f
    JPI d_hsh_f
e_hsh_f:
    NOP
    NOP
    NOP

    OUTB HSyncOff
    NOP
    NOP
    NOP
    NOP
    NOP

    LDA RA
    SUB ACC, 1
    LDR RA
    CMP ACC, 0
    JPZ VSYNC_SETUP
    LDI ACC, 0
delay_vfp:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vfp
    JPI delay_vfp
end_vfp:
    LDI ACC, 2          ; Pad de 8 ciclos (substitui 8 NOPs)
d_pad_f:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_pad_f
    JPI d_pad_f
e_pad_f:
    JPI VFP_LOOP

VSYNC_SETUP:
    LDI ACC, 2
    LDR RA
    OUTC VSyncOn
    LDI ACC, 0
delay_vfs:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vfs
    JPI delay_vfs
end_vfs:
    NOP
    NOP
    NOP
    NOP
    NOP
    JPI VSYNC_LOOP

; -----------------------------------------------------------------
; 3. VERTICAL SYNC (2 Lines)
; -----------------------------------------------------------------
VSYNC_LOOP:
    OUTB HSyncOn
    LDI ACC, 2
d_hsh_s:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_hsh_s
    JPI d_hsh_s
e_hsh_s:
    NOP
    NOP
    NOP

    OUTB HSyncOff
    NOP
    NOP
    NOP
    NOP
    NOP

    LDA RA
    SUB ACC, 1
    LDR RA
    CMP ACC, 0
    JPZ VBP_SETUP

    LDI ACC, 0
delay_vsn:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vsn
    JPI delay_vsn
end_vsn:
    LDI ACC, 2          ; Pad de 8 ciclos
d_pad_s:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_pad_s
    JPI d_pad_s
e_pad_s:
    JPI VSYNC_LOOP

VBP_SETUP:
    LDI ACC, 3
    LDR RB
    LDI ACC, 11
    LDR RA
    OUTC VSyncOff
    LDI ACC, 0
delay_vs_out:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vs_out
    JPI delay_vs_out
end_vs_out:
    NOP
    NOP
    NOP
    JPI VBP_LOOP

; -----------------------------------------------------------------
; 4. VERTICAL BACK PORCH (33 Lines)
; -----------------------------------------------------------------
VBP_LOOP:
    OUTB HSyncOn
    LDI ACC, 2
d_hsh_b:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_hsh_b
    JPI d_hsh_b
e_hsh_b:
    NOP
    NOP
    NOP

    OUTB HSyncOff
    NOP
    NOP
    NOP
    NOP
    NOP

    LDA RA
    SUB ACC, 1
    LDR RA
    CMP ACC, 0
    JPZ VBP_RA_ZERO
    LDI ACC, 0
delay_vbp:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vbp
    JPI delay_vbp
end_vbp:
    LDI ACC, 2          ; Pad de 8 ciclos
d_pad_b:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_pad_b
    JPI d_pad_b
e_pad_b:
    JPI VBP_LOOP

VBP_RA_ZERO:
    LDA RB
    SUB ACC, 1
    LDR RB
    CMP ACC, 0 ; Test if RB = 0
    JPZ FRAME_DONE ; If it is, prepare to do next frame
    LDI ACC, 11
    LDR RA
    LDI ACC, 15
delay_vbp2:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vbp2
    JPI delay_vbp2
end_vbp2:
    NOP
    NOP
    NOP
    NOP
    NOP
    JPI VBP_LOOP

FRAME_DONE:
    LDI ACC, 3 ; Reload the Counters (RA, RB and RAM) to do the next frame
    STW @LoopOuter, ACC
    LDI ACC, 0
    LDR RB
    LDI ACC, 10
    LDR RA
    LDI ACC, 14
delay_vbp_exit:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vbp_exit
    JPI delay_vbp_exit
end_vbp_exit:
    NOP
    NOP
    NOP
    NOP
    NOP
    JPI V_LOOP_RA
