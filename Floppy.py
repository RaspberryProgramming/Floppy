import thumby
import random
import machine
import time

"""
                Global Vars
"""

# Device Specific
display_dim = [72, 40] # w, h

# Display Objects

"""
Example

obj = {
    "type": "bitmap" | "text" | "rectangle",
    "text" | "bitmap": bytearray | "",
    "pos": [x,y],
    "dim": [w,h]
}

"""

bird = {
    "type": "bitmap",
    "bitmap": bytearray([0,112,240,240,244,108,158,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,7,7,7,6,5,5,5,5,5,3,0,0]),
    "pos": [5,16],
    "dim": [17, 12]
}

score_text = {
    "type": "text",
    "text": "0",
    "pos": [display_dim[0]-18, display_dim[1]-7],
    "dim": None
}

# Dictates the space between each pipe (Should be bird's height + 2)
space_btw = bird["dim"][0] + 3


"""
                Functions
"""

def playEnd():
    """
    playEnd: Plays music at the end of the game
    """
    
    # Notes based on frequency
    endMusic = [1108, 1108]
    
    # Play each note
    for i in endMusic:
        thumby.audio.play(i, 110)
        time.sleep(0.1)
    

def drawObj(obj):
    """
    drawObj: Draws and object (Stored in dictionary format).
             Should be defined like display object above
    """
    if obj["type"] == "bitmap":
        thumby.display.blit(obj["bitmap"], obj["pos"][0], obj["pos"][1], obj["dim"][0], obj["dim"][1], -1, 0, 0)
        
    elif obj["type"] == "rectangle":
        thumby.display.drawFilledRectangle(obj["pos"][0], obj["pos"][1], obj["dim"][0], obj["dim"][1], 1)
        
    elif obj["type"] == "text":
        thumby.display.drawText(obj["text"], obj["pos"][0], obj["pos"][1], 1)
        
    else:
        thumby.display.fill(0)
        thumby.display.drawText("ERROR", 10, 15, 1)


def newPipe(x, y, w, h):
    return {
        "type": "rectangle",
        "pos": [x,y],
        "dim": [w, h]
    }

def generatePipe():
    
    y = random.randrange(0, display_dim[1]-space_btw)
    
    
    top = newPipe(display_dim[0], (y-display_dim[1]), 10, 40)
    bottom = newPipe(display_dim[0], y+space_btw, 10, 40)
    
    return [top, bottom]
    
def detectCollision(obj1, obj2):
    
    # Generate a set of points
    
    r_point1 = [obj1["pos"][0]+obj1["dim"][0], obj1["pos"][1]+obj1["dim"][1]]
    l_point1 = [obj1["pos"][0], obj1["pos"][1]]
    r_point2 = [obj2["pos"][0]+obj2["dim"][0], obj2["pos"][1]+obj2["dim"][1]]
    l_point2 = [obj2["pos"][0], obj2["pos"][1]]

    # Check if the objects are right/left of the other
    if (r_point1[0] <= l_point2[0] or l_point1[0] >= r_point2[0]):
        return False
    
    # Check if objects are on top/below each other
    if (r_point1[1] <= l_point2[1] or l_point1[1] >= r_point2[1]):
        return False
    
    # Return True for collision
    return True

def game():
    # Controls whether the game is over
    gameover = False
    
    soundQueue = [] # Queue for storing sound notes

    pipes = generatePipe()
    
    steps = 0
    
    score = 0
    
    while (not gameover):
        
        steps += 1
        
        if thumby.buttonA.pressed() and bird["pos"][1] > 0:
            bird["pos"][1] -= 3
        else:
            bird["pos"][1] += 1
            
        if (pipes[-1]["pos"][0]+pipes[-1]["dim"][0] < display_dim[0]-26):
            pipes += generatePipe()
        
        for p in pipes:
            p["pos"][0] -= 2
            
        if pipes[0]["pos"][0]+pipes[0]["dim"][0] < 0:
            del pipes[0]
            del pipes[0]
            
            soundQueue += [1046, 1396, 1396, 1396]
            
            score += 1
            
        if (bird["pos"][1] > 40-bird["dim"][1]
            or detectCollision(bird, pipes[0])
            or detectCollision(bird, pipes[1])):
            
            # End Game
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
            
    return score

def main():
    
    score = game()
    
    # End Screen
    
    # Clear Screen
    thumby.display.fill(0)

    # Render bird in new pos
    bird["pos"][1] = display_dim[1]-bird["dim"][1]
    drawObj(bird)
    
    # Render Text
    thumby.display.drawText("Game Over", 10, 3, 1)
    
    thumby.display.drawText("Score %d" % score, 10, 15, 1)
    
    # Update Screen
    thumby.display.update()
    
    # Play end music
    playEnd()


main()
