import thumby
import random
import machine
import time

# BITMAP: width: 17, height: 12
bird_bitmap = bytearray([0,112,240,240,244,108,158,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,7,7,7,6,5,5,5,5,5,3,0,0])

bird = {
    "bitmap": bird_bitmap,
    "pos": [5,16],
    "dim": [17, 12],
}

gameover = False

def drawObj(obj):
    thumby.display.blit(obj["bitmap"], obj["pos"][0], obj["pos"][1], obj["dim"][0], obj["dim"][1], -1, 0, 0)

thumby.display.fill(0)

drawObj(bird)

thumby.display.update()

while (not gameover):
    if thumby.buttonA.pressed():
        bird["pos"][1] -= 3
    else:
        bird["pos"][1] += 1
    
    if bird["pos"][1] < 0 or bird["pos"][1] > 40-bird["dim"][1]:
        
        gameover = True
        
    else:
        thumby.display.fill(0)
        
        drawObj(bird)
        
        thumby.display.update()
        
        time.sleep(0.1)
        
thumby.display.drawText("Game Over", 10, 15, 1)

thumby.display.update()
