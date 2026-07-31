; ======================================================================================
; MikroLeo Basic VGA Driver v0.1
; May 03, 2026
; Edson Junior Acordi
; This code fills the screen of a 640×480 VGA monitor with a single color
; ======================================================================================

; ======================================================================================
; MikroLeo VGA Specs
; Clock: 3MHz | HSync: 31.25 kHz | VSync: 59.52 Hz | MikroLeo Horizontal Pixel width: 8
; Effective horizontal visible pixels: 76
; Equivalent horizontal visible pixels: 608
; Total equivalent pixels per line: 608 + (E) + (B) + (C) = 768
;
; Front Porch Horizontal (E): 16
; HSync (B): 96
; Back Porch Horizontal (C): 48
; ======================================================================================

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
; HSync and VSync are active at low level (Negative sync pulse)
;
; The code is optimized to fit at one page (256 addresses, RC=0)
;
; MikroLeo VGA Timing (in MikroLeo, 1 cycle = 8 VGA pixel clocks):
; ---------------------------
; Horizontal        | Cycles
; ------------------+--------
; Visible Area (D): |  76
; Front Porch (E):  |   2
; HSync Pulse (B):  |  12
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
; - Nested loops: RA counts 10 lines, RB counts 16 groups, LoopOuter counts 3 groups.
;   Total visible lines = 10 × 16 × 3 = 480.
; - All arithmetic is 4‑bit (values 0–15), underflow is used deliberately.
;
; Code blocks:
; VFP_LOOP => Vertical Front Porch loop (10 lines)
; VSYNC_LOOP => Vertical Sync loop (2 lines)
; VBP_LOOP => Vertical Back Porch loop (33 lines)
; FRAME_DONE => Reset counters and start a new frame

; Definition of Constants
#DEFINE VSyncOff $0b0001   ; VSync inactive (high)
#DEFINE HSyncOff $0b0001   ; HSync inactive (high)
#DEFINE VSyncOn  $0b0000   ; VSync active (low)
#DEFINE HSyncOn  $0b0000   ; HSync active (low)

; Definition of variables in RAM
#DEFINE LoopOuter $0x00    ; Outer loop counter (visible lines), initialised to 3

; ---------------------------------------------------------------------
; INITIALISATION
; Turn off sync signals, set RGB to black, and wait for stabilisation.
; ---------------------------------------------------------------------
INIT:
    OUTB HSyncOff          ; HSync = high (inactive)
    OUTC VSyncOff          ; VSync = high (inactive)
    OUTD 0x0               ; RGB = 000 (black), ensure blanking
    NOP                    ; Wait for signal settling
    NOP
    NOP
    NOP

; ---------------------------------------------------------------------
; START OF A NEW FRAME
; Prepare the three nested counters for 480 visible lines.
; ---------------------------------------------------------------------
START_FRAME:
; Prepare the Counters to draw 480 visible lines.
; Visible lines = RA x RB x RAM = 10 x 16 x 3 = 480 lines
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

    LDI ACC, 3             ; Outer loop counter = 3
    STW @LoopOuter, ACC    ; Store in RAM
    LDI ACC, 0             ; RB = 0 (will underflow to 15 on first decrement)
    LDR RB
    LDI ACC, 10            ; RA = 10 (counts 10 lines per group)
    LDR RA

; -----------------------------------------------------------------
; 1. VISIBLE AREA (480 Lines)
; -----------------------------------------------------------------
; Each iteration of V_LOOP_RA draws one full visible line (96 cycles).
; The active pixel colour (0x2 = green) is output for exactly 76 cycles.
;
; Path 1: RA > 0
;   The inner loop. Draws 10 lines, decrementing RA each line.
;   When RA becomes 0 we jump to CAMINHO_RA_ZERO (Path 2).
; -----------------------------------------------------------------
V_LOOP_RA:
    ; --- HSync pulse (12 cycles) ---
    OUTB HSyncOn           ; HSync goes low (start of line)
    LDI ACC, 2             ; prepare mini‑loop for HSync width
d_hsh_v:
    SUB ACC, 1             ; decrement ACC
    CMP ACC, 0             ; test if zero
    JPZ e_hsh_v            ; exit loop when ACC=0
    JPI d_hsh_v            ; else continue
e_hsh_v:
    NOP                    ; fine‑tune HSync width to exactly 12 cycles
    NOP
    NOP
    OUTB HSyncOff          ; HSync goes high (end of pulse, back porch starts)

    ; --- Back porch (6 cycles) ---
    NOP                    ; 5 NOPs + the OUTB HSyncOff cycle itself = 6 cycles of HSync high before video
    NOP
    NOP
    NOP
    NOP

    ; --- Start of visible area (76 cycles) ---
    OUTD 0x2               ; RGB = 010 (green), first pixel of the line

    ; Decrement RA and check if it became 0
    LDA RA                 ; ACC = RA
    SUB ACC, 1             ; RA = RA - 1
    LDR RA
    CMP ACC, 0             ; did RA transition from 1 to 0?
    JPZ CAMINHO_RA_ZERO    ; yes -> Path 2

    ; RA still > 0 -> complete the line with a long delay (visible area + front porch)
    LDI ACC, 0             ; ACC = 0 (underflow to 15 after first SUB)
delay_normal:
    SUB ACC, 1             ; 4‑bit underflow gives 15 on first pass
    CMP ACC, 0
    JPZ sai_delay_normal
    JPI delay_normal
sai_delay_normal:
    NOP                    ; padding to align total line length to 96 cycles
    NOP
    NOP
    NOP
    NOP
    NOP
    OUTD 0x0               ; RGB = 000 (black) => end of visible area, start of front porch
    JPI V_LOOP_RA          ; next line (front porch continues with this JPI and the next HSync)

; --------------------------
; Path 2: RA = 0 and RB > 0
; --------------------------
; Reloads RA with 10 and decreases RB by 1.
; Path 2 is the medium loop, controlled by RB.
; This line is still a full visible line (76 green cycles, 96 total cycles).
; --------------------------
CAMINHO_RA_ZERO:
    LDA RB                 ; ACC = RB
    SUB ACC, 1             ; RB = RB - 1
    LDR RB
    CMP ACC, 0             ; if RB became 0, go to Path 3
    JPZ RECARGA_MEMORIA    ; RB = 0, go to outer loop

    ; RB > 0: reload RA = 10 and finish the line
    LDI ACC, 10            ; RA = 10
    LDR RA
    LDI ACC, 15            ; set up a delay that, together with the rest of the line,
delay2:                    ; gives 76 visible cycles and 96 total cycles
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_delay2
    JPI delay2
end_delay2:
    NOP                    ; padding
    NOP
    NOP
    OUTD 0x0               ; end of visible area
    JPI V_LOOP_RA          ; start next visible line

; ---------------------------
; Path 3: RA = 0 and RB = 0
; ---------------------------
; Reloads RB and decreases LoopOuter in RAM by 1.
; Path 3 is the external loop, controlled by variable LoopOuter.
; ---------------------------
RECARGA_MEMORIA:
    LDW ACC, @LoopOuter    ; ACC = outer counter
    SUB ACC, 1             ; decrement it
    STW @LoopOuter, ACC
    CMP ACC, 0             ; if LoopOuter reached 0, all 480 lines are done
    JPZ V_FRONT_PORCH      ; yes => go to vertical front porch

    ; LoopOuter still > 0: reload RA = 10, RB = 0 and continue visible lines
    LDI ACC, 10
    LDR RA
    LDI ACC, 0
    LDR RB
    LDI ACC, 13            ; delay to complete the line (96 cycles)
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

; -----------------------------------------------------------------
; Vertical Front Porch – 10 lines
; After the last visible line, this small setup finishes the current
; 96‑cycle line and then enters the VFP_LOOP.
; -----------------------------------------------------------------
V_FRONT_PORCH:
    LDI ACC, 10            ; RA = 10 (number of front porch lines)
    LDR RA
    LDI ACC, 14            ; delay to align the end of the last visible line
delay_exit:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_exit
    JPI delay_exit
end_exit:
    NOP
    NOP
    OUTD 0x0               ; ensure RGB = black
    JPI VFP_LOOP           ; start the first front porch line

; -----------------------------------------------------------------
; 2. VERTICAL FRONT PORCH (10 Lines)
; Each line is 96 cycles, RGB is kept black, HSync is generated normally.
; -----------------------------------------------------------------
VFP_LOOP:
    ; --- HSync pulse (12 cycles) ---
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

    ; --- Back porch (6 cycles) ---
    NOP
    NOP
    NOP
    NOP
    NOP

    ; --- Decrement line counter RA ---
    LDA RA
    SUB ACC, 1
    LDR RA
    CMP ACC, 0             ; 10 lines done?
    JPZ VSYNC_SETUP        ; yes => prepare vertical sync

    ; RA > 0 => complete the 96‑cycle line with blanking
    LDI ACC, 0
delay_vfp:
    SUB ACC, 1             ; 16‑iteration loop (same as delay_normal)
    CMP ACC, 0
    JPZ end_vfp
    JPI delay_vfp
end_vfp:
    LDI ACC, 2             ; pad of exactly 8 cycles (replaces 8 NOPs)
d_pad_f:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_pad_f
    JPI d_pad_f
e_pad_f:
    JPI VFP_LOOP           ; next front porch line

; -----------------------------------------------------------------
; Transition to Vertical Sync
; Finishes the last front porch line and enables VSync (active low).
; -----------------------------------------------------------------
VSYNC_SETUP:
    LDI ACC, 2             ; RA = 2 (vertical sync lasts 2 lines)
    LDR RA
    OUTC VSyncOn           ; VSync goes low
    LDI ACC, 0             ; delay to complete the 96‑cycle line
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
    JPI VSYNC_LOOP         ; enter vertical sync loop

; -----------------------------------------------------------------
; 3. VERTICAL SYNC (2 Lines)
; VSync stays low for two full lines, RGB = black.
; -----------------------------------------------------------------
VSYNC_LOOP:
    ; --- HSync pulse ---
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

    ; --- Back porch (6 cycles) ---
    NOP
    NOP
    NOP
    NOP
    NOP

    ; --- Decrement line counter ---
    LDA RA
    SUB ACC, 1
    LDR RA
    CMP ACC, 0             ; both VSync lines done?
    JPZ VBP_SETUP          ; yes => prepare vertical back porch

    ; RA > 0 => complete the line
    LDI ACC, 0
delay_vsn:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vsn
    JPI delay_vsn
end_vsn:
    LDI ACC, 2             ; 8‑cycle pad
d_pad_s:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_pad_s
    JPI d_pad_s
e_pad_s:
    JPI VSYNC_LOOP

; -----------------------------------------------------------------
; Transition to Vertical Back Porch
; Finishes the last VSync line, turns off VSync, and sets up
; counters for 33 back porch lines (RA=11, RB=3, total 33).
; -----------------------------------------------------------------
VBP_SETUP:
    LDI ACC, 3             ; RB = 3 (outer count for back porch)
    LDR RB
    LDI ACC, 11            ; RA = 11 (inner count per RB)
    LDR RA
    OUTC VSyncOff          ; VSync goes high (inactive)
    LDI ACC, 0             ; delay to complete the 96‑cycle line
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
    ; --- HSync pulse ---
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

    ; --- Back porch (6 cycles) ---
    NOP
    NOP
    NOP
    NOP
    NOP

    ; --- Decrement inner counter RA ---
    LDA RA
    SUB ACC, 1
    LDR RA
    CMP ACC, 0
    JPZ VBP_RA_ZERO        ; RA became 0 => decrement RB

    ; RA > 0 => complete the line
    LDI ACC, 0
delay_vbp:
    SUB ACC, 1
    CMP ACC, 0
    JPZ end_vbp
    JPI delay_vbp
end_vbp:
    LDI ACC, 2             ; 8‑cycle pad
d_pad_b:
    SUB ACC, 1
    CMP ACC, 0
    JPZ e_pad_b
    JPI d_pad_b
e_pad_b:
    JPI VBP_LOOP

; RA reached 0, now decrement RB and reload RA=11 (if RB still > 0)
VBP_RA_ZERO:
    LDA RB
    SUB ACC, 1
    LDR RB
    CMP ACC, 0             ; if RB became 0, all 33 back porch lines done
    JPZ FRAME_DONE         ; yes => reset everything for next frame

    ; RB > 0 => reload RA = 11 and complete the line
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

; -----------------------------------------------------------------
; FRAME DONE
; The entire frame (525 lines) has been output. Reload all counters
; to start the next frame seamlessly.
; -----------------------------------------------------------------
FRAME_DONE:
    LDI ACC, 3             ; restore outer loop counter (visible lines)
    STW @LoopOuter, ACC
    LDI ACC, 0             ; RB = 0
    LDR RB
    LDI ACC, 10            ; RA = 10
    LDR RA
    LDI ACC, 14            ; delay to complete the final 96‑cycle line
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
    JPI V_LOOP_RA          ; start the next frame!
