import thumby
import random
import machine
import time

# BITMAP: width: 17, height: 12
bird_bitmap = bytearray([0,112,240,240,244,108,158,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,7,7,7,6,5,5,5,5,5,3,0,0])


bird = {
    "type": "bitmap",
    "bitmap": bird_bitmap,
    "pos": [5,16],
    "dim": [12, 17],
}

pipes = []

gameover = False

space_btw = bird["dim"][1] + 6

def drawObj(obj):
    if obj["type"] == "bitmap":
        thumby.display.blit(obj["bitmap"], obj["pos"][0], obj["pos"][1], obj["dim"][1], obj["dim"][0], -1, 0, 0)
    elif obj["type"] == "rectangle":
        thumby.display.drawFilledRectangle(obj["pos"][0], obj["pos"][1], obj["dim"][1], obj["dim"][0], 1)
    else:
        thumby.display.fill(0)
        thumby.display.drawText("ERROR", 10, 15, 1)


def newPipe(x, y, h, w):
    return {
        "type": "rectangle",
        "pos": [x,y],
        "dim": [h, w]
    }

thumby.display.fill(0)

drawObj(bird)

thumby.display.update()

steps = 0

pipe_space = 15 # Space between each set of pipes

while (not gameover):
    
    steps += 1
    
    if thumby.buttonA.pressed():
        bird["pos"][1] -= 3
    else:
        bird["pos"][1] += 1
        
    if (steps%pipe_space == 0):
        pipes.append(newPipe(72, 20, 40, 10))
        pipes.append(newPipe(72, (-20)-15, 40, 10))
        
    for p in pipes:
        p["pos"][0] -= 2
    
    if bird["pos"][1] < 0 or bird["pos"][1] > 40-bird["dim"][1]:
        
        gameover = True
        
    else:
        thumby.display.fill(0)
        
        drawObj(bird)
        
        for p in pipes:
            drawObj(p)
        
        thumby.display.update()
        
        time.sleep(0.1)
        
thumby.display.drawText("Game Over", 10, 15, 1)

thumby.display.update()
