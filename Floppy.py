import thumby
import random
import machine
import time

# BITMAP: width: 17, height: 12
bird_bitmap = bytearray([0,112,240,240,244,108,158,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,7,7,7,6,5,5,5,5,5,3,0,0])

display_dim = [72, 40] # x, y

bird = {
    "type": "bitmap",
    "bitmap": bird_bitmap,
    "pos": [5,16],
    "dim": [12, 17]
}

score_text = {
    "type": "text",
    "text": "0",
    "pos": [display_dim[0]-18, display_dim[1]-7],
    "dim": None
}

gameover = False

space_btw = bird["dim"][1] + 2

soundQueue = []

def playEnd():
    endMusic = [1108, 1108]
    
    for i in endMusic:
        thumby.audio.play(i, 110)
        time.sleep(0.1)
    

def drawObj(obj):
    if obj["type"] == "bitmap":
        thumby.display.blit(obj["bitmap"], obj["pos"][0], obj["pos"][1], obj["dim"][1], obj["dim"][0], -1, 0, 0)
        
    elif obj["type"] == "rectangle":
        thumby.display.drawFilledRectangle(obj["pos"][0], obj["pos"][1], obj["dim"][1], obj["dim"][0], 1)
        
    elif obj["type"] == "text":
        thumby.display.drawText(obj["text"], obj["pos"][0], obj["pos"][1], 1)
        
    else:
        thumby.display.fill(0)
        thumby.display.drawText("ERROR", 10, 15, 1)


def newPipe(x, y, h, w):
    return {
        "type": "rectangle",
        "pos": [x,y],
        "dim": [h, w]
    }

def generatePipe():
    
    y = random.randrange(0, display_dim[1]-space_btw)
    
    
    top = newPipe(display_dim[0], (y-40), 40, 10)
    bottom = newPipe(display_dim[0], y+space_btw, 40, 10)
    
    return [top, bottom]
    
def detectCollision(obj1, obj2):
    
    r_point1 = [obj1["pos"][0]+obj1["dim"][1], obj1["pos"][1]+obj1["dim"][0]]
    l_point1 = [obj1["pos"][0], obj1["pos"][1]]
    r_point2 = [obj2["pos"][0]+obj2["dim"][1], obj2["pos"][1]+obj2["dim"][0]]
    l_point2 = [obj2["pos"][0], obj2["pos"][1]]

    if (r_point1[0] <= l_point2[0] or l_point1[0] >= r_point2[0]):
        return False
    
    if (r_point1[1] <= l_point2[1] or l_point1[1] >= r_point2[1]):
        return False
    
    return True

thumby.display.fill(0)

drawObj(bird)

thumby.display.update()

pipes = generatePipe()

steps = 0

score = 0

while (not gameover):
    
    steps += 1
    
    if thumby.buttonA.pressed() and bird["pos"][1] > 0:
        bird["pos"][1] -= 3
    else:
        bird["pos"][1] += 1
        
    if (pipes[-1]["pos"][0]+pipes[-1]["dim"][0] < display_dim[0]):
        pipes += generatePipe()
    
    for p in pipes:
        p["pos"][0] -= 2
        
    if pipes[0]["pos"][0]+pipes[0]["dim"][1] < 0:
        del pipes[0]
        del pipes[0]
        
        soundQueue += [1046, 1396, 1396, 1396]
        
        score += 1
        
    if (bird["pos"][1] > 40-bird["dim"][0]
        or detectCollision(bird, pipes[0])
        or detectCollision(bird, pipes[1])):
        
        gameover = True
        
    else:
        
        # Rerender scene
        
        thumby.display.fill(0)
        
        drawObj(bird)
        
        for p in pipes:
            drawObj(p)
            
        # Write the score
        score_text["text"] = str(score)
        
        drawObj(score_text)
        
        # Update the display
        thumby.display.update()
        
        # Play sound
        
        if (len(soundQueue) > 0):
            thumby.audio.play(soundQueue[0], 110)
            del soundQueue[0]
        
        time.sleep(0.1)
        

thumby.display.fill(0)

bird["pos"][1] = display_dim[1]-bird["dim"][0]
drawObj(bird)

thumby.display.drawFilledRectangle(0, 2, display_dim[0], 9, 0)

thumby.display.drawText("Game Over", 10, 3, 1)

thumby.display.drawFilledRectangle(0, 14, display_dim[0], 9, 0)

thumby.display.drawText("Score %d" % score, 10, 15, 1)

thumby.display.update()

# Play end music
playEnd()
