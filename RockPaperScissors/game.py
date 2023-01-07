from microbit import *
import music
import random
import time

def poll():
    if button_a.is_pressed():
        a = pin1.read_analog()
        display.scroll(a)
    elif button_b.is_pressed():
        Reset()

display.show(Image.HAPPY)

MODE_NONE = 0
MODE_GAME1 = 1
MODE_GAME2 = 2
MODE_DONE = 3
MODE_RESET = 4

mode = MODE_NONE
now_ms = time.ticks_ms()
dark_start_ms = -1
prev_stage_ms = now_ms

def Reset():
    global mode, prev_stage_ms, dark_start_ms
    mode = MODE_RESET
    dark_start_ms = time.ticks_ms()
    prev_stage_ms = -1
    display.clear()

def NextStage():
    global mode, prev_stage_ms
    now_ms = time.ticks_ms()
    if now_ms - prev_stage_ms < 500:
        # Too fast, ignore
        return
    prev_stage_ms = now_ms
    if mode == MODE_NONE:
        mode = MODE_GAME1
        display.show(1)
        return
    if mode == MODE_GAME1:
        mode = MODE_GAME2
        display.show(2)
        return
    if mode == MODE_GAME2:
        mode = MODE_NONE
        result = random.randint(0, 2)
        if result == 0:
            display.show(Image.SCISSORS)
        elif result == 1:
            display.show(Image("09990:99999:99999:99999:09990"))
        elif result == 2:
            display.show(Image("88888:99999:99999:99999:88888"))
        music.play(music.BA_DING, wait=True)
        return

    

N_UPDATE = 50
average = pin1.read_analog()  # Normal light level

count = 0
while True:
    poll()
    count += 1
    a = pin1.read_analog()
    now_ms = time.ticks_ms()
    if a > average + 20:
        if dark_start_ms < 0:
            NextStage()
            dark_start_ms = now_ms
            continue
        else:
            dark_ms = now_ms - dark_start_ms
            if dark_ms > 3000:
                Reset()
                continue
    elif a < average+1:
        if mode == MODE_RESET:
            display.show(Image.HAPPY)
            mode = MODE_NONE
            continue
        dark_start_ms = -1
        if prev_stage_ms > 0 and now_ms - prev_stage_ms > 5000:
            prev_stage_ms = -1
            display.show(Image.HAPPY)
            continue
        
        

