import vgamepad as vg 
import sys
from time import sleep
import math
import json

gamepad = vg.VX360Gamepad()
input("Press Enter When Controller is Selected on Cemu")

def getButton(key):
    if key == "KEY_A":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_B
    elif key == "KEY_B":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_A
    elif key == "KEY_X":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_Y
    elif key == "KEY_Y":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_X
    elif key == "KEY_ZL":
        return "ZL_FN"
    elif key == "KEY_ZR":
        return "ZR_FN"
    elif key == "KEY_L":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER
    elif key == "KEY_R":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER
    elif key == "KEY_PLUS":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_START
    elif key == "KEY_MINUS":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK
    elif key == "KEY_DUP":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP
    elif key == "KEY_DDOWN":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN
    elif key == "KEY_DRIGHT":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT
    elif key == "KEY_DLEFT":
        return vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT
    
f = None
try:
    f = open("./tas.txt")
except Exception as e:
    print("./tas.txt not found")
    sys.exit()
checker = []
x = 0
y = 0
rx = 0
ry = 0

currentKeys = []
keyB = []
thisO = {}
tas_split = f.read().split("\n")
for i in range(len(tas_split)):
    thisO = {
        "lstick": [x, y],
        "rstick": [rx, ry],
        "keys": currentKeys,
        "delay": 0
    }
    checker.append([])
    line = tas_split[i].split(" ")
    if line[0] == "+":
        line[0] = "0"
    thisO["delay"] = int(line[0])
    for cmd in line:
        if cmd.startswith("LSTICK{"):
            cmd = cmd.replace("LSTICK{", "").replace("}", "")
            v = int(cmd.split(",")[0])
            d = int(cmd.split(",")[1])
            
            y = math.floor(d * math.cos(math.radians(v)))
            x = math.floor(d * math.sin(math.radians(v)))
            thisO["lstick"] = [x,y]
            print("Setting LSTICK pos to (" + str(x) + ", " + str(y) + ")")
        elif cmd.startswith("RSTICK{"):
            cmd = cmd.replace("RSTICK{", "").replace("}", "")
            v = int(cmd.split(",")[0])
            d = int(cmd.split(",")[1])
            ry = math.floor(d * math.cos(math.radians(v)))
            rx = math.floor(d * math.sin(math.radians(v)))
            
            thisO["rstick"] = [rx, ry]
        elif cmd.startswith("ON{"):
            cmd = cmd.replace("ON{", "").replace("}", "").split(",")
            for key in cmd:
                if key not in currentKeys:
                    currentKeys.append(key)
                    thisO["keys"] = currentKeys
                    print("Adding " + key)
        elif cmd.startswith("OFF{"):
            cmd = cmd.replace("OFF{", "").replace("}", "").split(",")
            for key in cmd:
                if key == "ALL":
                    for _ in range(len(currentKeys)):
                        currentKeys.pop()
                        print("POP")
                    print("Removing ALL")
                if key in currentKeys:
                    currentKeys.remove(key)
                    thisO["keys"] = currentKeys
                    
    keyB.append(str(thisO).replace("'", "\""))
currentKeys = []
gamepad.reset()
for o in keyB:
    o = json.loads("{ \"code\": " + o + "}")["code"]
    print(o["delay"], o["keys"])
    gamepad.reset()
    for k in o["keys"]:
        k = getButton(k)
        if k == "ZL_FN":
            gamepad.left_trigger_float(value_float=1)
        elif k == "ZR_FN":
            gamepad.right_trigger_float(value_float=1)
        else:
            gamepad.press_button(button=k) 
    gamepad.left_joystick(x_value=o["lstick"][0], y_value=o["lstick"][1])
    gamepad.right_joystick(x_value=o["rstick"][0], y_value=o["rstick"][1])
    sleep(o["delay"]/60)
    gamepad.update()
