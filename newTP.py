from cmu_graphics import *
import random
import math

def resetGame(app):
    app.currentScreen = 'start'  
    currentScreen = app.currentScreen if hasattr(app, 'currentScreen') else 'start'
    
    app.scrollX = 0
    app.curves = []  

    app.charWidth = 30
    app.charHeight = 40

    firstCurve = generateDiverseCurvePoints(0, 200)
    app.curves.append(firstCurve)

    for i in range(3):
        lastCurve = app.curves[-1]
        nextY = lastCurve[3][1]  
        nextY = min(max(nextY, 100), 350)  
        nextCurve = generateDiverseCurvePoints(lastCurve[3][0], nextY)
        app.curves.append(nextCurve)

    app.charX = 20
    app.charY = 150
    app.charAngle = 0  

    app.gravity = 0.4
    app.airGravity = 0.5
    app.friction = 0.001
    app.maxSpeed = 12
    app.baseSpeed = 8
    app.rampBoost = 1.2
    app.airControl = 0.95
    app.velocityX = app.baseSpeed
    app.velocityY = 0
    app.onCurve = False

    
    

    app.inTrick = False
    app.trickRotation = 0
    app.trickSpeed = 0.2
    app.score = 0

    app.snowboarderWidth = 40
    app.snowboarderHeight = 50

    app.clouds = []
    app.cloudSpeeds = [0.2, 0.4, 0.6]  
    app.cloudLayers = 3
    
    
    for layer in range(app.cloudLayers):
        for _ in range(4):  
            x = random.randint(0, 400)
            y = 30 + layer * 30  
            width = random.randint(60, 100)
            height = random.randint(30, 50)
            app.clouds.append([x, y, width, height, layer])


    app.dayTime = 0
    app.daySpeed = 0.5
    app.sunX = 400  
    app.sunY = 50
    app.isNight = False
    app.isRaining = False
    app.timeSinceNight = 0  
    app.nightDuration = 300  
    
    
    app.raindrops = []
    app.maxRaindrops = 100
    app.isRaining = False 

    app.trees = []
    app.treeSpacing = 100  
    app.treeChance = 0.3   
    app.treeWidth = 20
    app.treeHeight = 30
    
    app.buttonWidth = 200
    app.buttonHeight = 50    

    app.currentScreen = currentScreen   

def createRaindrop():
    x = random.randint(0, 400)
    y = random.randint(-50, 0)
    speed = random.randint(5, 10)
    return [x, y, speed]

def updateDayNightCycle(app):
    
    app.sunX -= app.daySpeed
    
    
    if app.sunX < -30:  
        app.isNight = True
        app.isRaining = True
        app.timeSinceNight += 1
        
        
        if app.timeSinceNight >= app.nightDuration:
            app.sunX = 430  
            app.isNight = False
            app.isRaining = False
            app.timeSinceNight = 0

def updateRain(app):
    if app.isRaining:
        
        if len(app.raindrops) < app.maxRaindrops:
            app.raindrops.append(createRaindrop())
        
        
        for drop in app.raindrops:
            drop[1] += drop[2]  
            
        
        app.raindrops = [drop for drop in app.raindrops if drop[1] < 400]
    
def generateTreesForCurve(app, curve):
    points = generateCurvePoints(curve)
    currentX = points[0][0]
    
    while currentX < points[-1][0]:
        if random.random() < app.treeChance:
            
            for i in range(len(points)-1):
                if points[i][0] <= currentX <= points[i+1][0]:
                    
                    t = (currentX - points[i][0]) / (points[i+1][0] - points[i][0])
                    y = points[i][1] + t * (points[i+1][1] - points[i][1])
                    app.trees.append([currentX, y])
                    break
        currentX += app.treeSpacing

def drawTree(x, y):
    
    drawRect(x - 3, y - app.treeHeight, 6, app.treeHeight/3, 
            fill='saddleBrown')
    
    
    for i in range(3):
        points = [
            (x, y - app.treeHeight + i * app.treeHeight/4),  
            (x - app.treeWidth/2, y - app.treeHeight/2 + i * app.treeHeight/4),  
            (x + app.treeWidth/2, y - app.treeHeight/2 + i * app.treeHeight/4)   
        ]
        drawPolygon(*points, fill='darkGreen')

def drawStartScreen(app):
    skyColor = rgb(200, 220, 235)  
    drawRect(0, 0, 400, 400, fill=skyColor)
    
    drawLabel('Endless Slopes', 200, 120, size=40, bold=True, fill='white')
    
    drawRect(100, 180, app.buttonWidth, app.buttonHeight, fill=None, 
            border='white', borderWidth=2)
    drawLabel('PLAY', 200, 205, size=24, bold=True, fill='white')
    
    drawRect(100, 240, app.buttonWidth, app.buttonHeight, fill=None, 
            border='white', borderWidth=2)
    drawLabel('HELP', 200, 265, size=24, bold=True, fill='white')
    
    drawRect(100, 300, app.buttonWidth, app.buttonHeight, fill=None, 
            border='white', borderWidth=2)
    drawLabel('QUIT', 200, 325, size=24, bold=True, fill='white')
    
    for x in range(-20, 420, 40):
        drawPolygon(x, 400, x+20, 350, x+40, 400, fill='darkGreen')

def drawMenuScreen(app):
    skyColor = rgb(200, 220, 235)
    drawRect(0, 0, 400, 400, fill=skyColor)
    
    drawLabel('Endless Slopes', 200, 120, size=40, bold=True, fill='white')
    
    drawRect(100, 180, app.buttonWidth, app.buttonHeight, fill=None, 
            border='white', borderWidth=2)
    drawLabel('BEGIN GAME', 200, 205, size=24, bold=True, fill='white')
    
    drawRect(100, 240, app.buttonWidth, app.buttonHeight, fill=None, 
            border='white', borderWidth=2)
    drawLabel('MODES ', 200, 265, size=24, bold=True, fill='white')
    
    drawRect(100, 300, app.buttonWidth, app.buttonHeight, fill=None, 
            border='white', borderWidth=2)
    drawLabel('BACK', 200, 325, size=24, bold=True, fill='white')
    
    for x in range(-20, 420, 40):
        drawPolygon(x, 400, x+20, 350, x+40, 400, fill='darkGreen')

def onKeyHold(app, keys):
    if app.inTrick and not app.onCurve:
        if 'left' in keys:
            app.trickRotation -= app.trickSpeed
        if 'right' in keys:
            app.trickRotation += app.trickSpeed
#I got external help from the internet(redit and stack overflow) to understand the bezier curve and how to implement it in my code below.

def generateDiverseCurvePoints(startX, startY):
    minY = 100
    maxY = 350

    curve_styles = [
        lambda: (
            (startX, startY),
            (startX + random.randint(80, 120), startY - random.randint(50, 90)),
            (startX + random.randint(200, 250), startY + random.randint(70, 120)),
            (startX + 400, min(maxY, max(minY, startY - random.randint(40, 80))))
        ),
        lambda: (
            (startX, startY),
            (startX + random.randint(100, 150), startY + random.randint(60, 100)),
            (startX + random.randint(250, 300), startY - random.randint(80, 120)),
            (startX + 400, min(maxY, max(minY, startY + random.randint(50, 90))))
        )
    ]

    curve = random.choice(curve_styles)()

    endY = curve[3][1]
    if abs(endY - startY) < 40: 
        heightChange = random.randint(60, 100)
        if random.random() < 0.5:
            endY = startY + heightChange
        else:
            endY = startY - heightChange

        endY = min(maxY, max(minY, endY))
        curve = (curve[0], curve[1], curve[2], (curve[3][0], endY))

    return curve

def getBezierPoint(t, p0, p1, p2, p3):
    x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
    y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
    return (x, y)

def generateCurvePoints(curve):
    points = []
    for t in range(101):
        t = t / 100
        point = getBezierPoint(t, curve[0], curve[1], curve[2], curve[3])
        points.append(point)
    return points

def findClosestPointOnCurve(app, x, y):
    minDist = float('inf')
    closestPoint = None

    for curve in app.curves:
        points = generateCurvePoints(curve)
        for point in points:
            adjustedX = point[0] - app.scrollX
            dist = ((x - adjustedX)**2 + (y - point[1])**2)**0.5
            if dist < minDist:
                minDist = dist
                closestPoint = (adjustedX, point[1])

    return closestPoint, minDist

def onAppStart(app):
    
    resetGame(app)

def onKeyPress(app, key):
    if key == 'r':
        resetGame(app)

    if key == 'space' and app.onCurve:
        app.velocityY = -12  
        app.onCurve = False  
        app.charAngle = 0  



def lerp(start, end, t):
    """Linear interpolation between start and end values"""
    return start + (end - start) * t


def onStep(app):
    if not app.onCurve:
        app.velocityY += app.airGravity
        app.charY += app.velocityY
        app.charX += app.velocityX

        
        targetAngle = math.atan2(app.velocityY, app.velocityX)
        app.charAngle = lerp(app.charAngle, targetAngle, 0.1)

        closestPoint, distance = findClosestPointOnCurve(app, app.charX, app.charY + app.charHeight / 2)
        if distance <= app.charHeight / 2:
            app.onCurve = True
            app.charX = closestPoint[0]
            app.charY = closestPoint[1] - app.charHeight / 2
            app.velocityY = 0
    else:
        closestPoint, distance = findClosestPointOnCurve(app, app.charX, app.charY + app.charHeight / 2)
        if closestPoint is not None:
            nextPoint = findClosestPointOnCurve(app, app.charX + app.velocityX, app.charY + app.charHeight / 2)[0]
            if nextPoint:
                dx = nextPoint[0] - closestPoint[0]
                dy = nextPoint[1] - closestPoint[1]
                targetAngle = math.atan2(dy, dx)
                
                
                app.charAngle = lerp(app.charAngle, targetAngle, 0.15)

                if dy > 0:
                    accelerationX = app.gravity * math.sin(app.charAngle) * 1.2
                else:
                    accelerationX = app.gravity * math.sin(app.charAngle) * 0.8

                app.velocityX += accelerationX
                app.velocityX *= (1 - app.friction)
                app.velocityX = max(min(app.velocityX, app.maxSpeed), app.baseSpeed)

                app.charX += app.velocityX
                app.charY = closestPoint[1] - app.charHeight / 2

    
    if app.charX > 100:
        diff = app.charX - 100
        app.scrollX += diff
        app.charX = 100

    lastCurve = app.curves[-1]
    if lastCurve[3][0] - app.scrollX < 800:
        nextCurve = generateDiverseCurvePoints(lastCurve[3][0], lastCurve[3][1])
        app.curves.append(nextCurve)

    
    while app.curves and app.curves[0][3][0] < app.scrollX:
        app.curves.pop(0)

    for cloud in app.clouds:
        
        cloud[0] -= app.cloudSpeeds[cloud[4]] * app.velocityX
        
        
        if cloud[0] + cloud[2] < 0:
            cloud[0] = 400 + cloud[2]
            cloud[1] = 30 + cloud[4] * 30 + random.randint(-10, 10)
            cloud[2] = random.randint(60, 100)
            cloud[3] = random.randint(30, 50)
    updateDayNightCycle(app)
    updateRain(app)       

    lastCurve = app.curves[-1]
    if lastCurve[3][0] - app.scrollX < 800:
        nextCurve = generateDiverseCurvePoints(lastCurve[3][0], lastCurve[3][1])
        app.curves.append(nextCurve)
        generateTreesForCurve(app, nextCurve)
    
    
    app.trees = [tree for tree in app.trees if tree[0] - app.scrollX > -50]     


def onMousePress(app, mouseX, mouseY):
    if app.currentScreen == 'start':
        if (100 <= mouseX <= 300 and 
            180 <= mouseY <= 230):
            app.currentScreen = 'menu'
        # help button
        elif (100 <= mouseX <= 300 and 
              240 <= mouseY <= 290):
            pass  #add the functionality for help
        elif (100 <= mouseX <= 300 and 
              300 <= mouseY <= 350):
            pass  # add the quit functionality 
    
    elif app.currentScreen == 'menu':
        # 
        if (100 <= mouseX <= 300 and 
            180 <= mouseY <= 230):
            app.currentScreen = 'game'
            # initalizing the game state
            app.scrollX = 0
            app.curves = []
            
            firstCurve = generateDiverseCurvePoints(0, 200)
            app.curves.append(firstCurve)
            
            for i in range(3):
                lastCurve = app.curves[-1]
                nextY = lastCurve[3][1]
                nextY = min(max(nextY, 100), 350)
                nextCurve = generateDiverseCurvePoints(lastCurve[3][0], nextY)
                app.curves.append(nextCurve)
            
            # Reset character position and physics
            app.charX = 20
            app.charY = 150
            app.charAngle = 0
            app.velocityX = app.baseSpeed
            app.velocityY = 0
            app.onCurve = False
            
        #  modes button
        elif (100 <= mouseX <= 300 and 
              240 <= mouseY <= 290):
            pass  #add the functionality for modes
        # the back button
        elif (100 <= mouseX <= 300 and 
              300 <= mouseY <= 350):
            app.currentScreen = 'start'

def redrawAll(app):
    if app.currentScreen == 'start':
        drawStartScreen(app)
    elif app.currentScreen == 'menu':
        drawMenuScreen(app)
    else:
        # here is the existing code for the game screen
        skyColor = rgb(
            max(50, min(135, 135 - (app.isNight * 85))),
            max(50, min(206, 206 - (app.isNight * 156))),
            max(100, min(235, 235 - (app.isNight * 135)))
        )
        drawRect(0, 0, 400, 400, fill=skyColor)

        for tree in app.trees:
            treeX = tree[0] - app.scrollX
            if 0 <= treeX <= 400:  
                drawTree(treeX, tree[1])
    
    
    
        if not app.isNight:
            drawCircle(app.sunX, app.sunY, 30, 
                    fill='yellow')
    
        for cloud in app.clouds:
            x, y, width, height, layer = cloud
            drawOval(x, y, width, height, fill='white')


        
        for curve in app.curves:
            points = generateCurvePoints(curve)
            for i in range(len(points)-1):
                p1 = points[i]
                p2 = points[i+1]
                x1 = p1[0] - app.scrollX
                x2 = p2[0] - app.scrollX
                if 0 <= x1 <= 400 or 0 <= x2 <= 400:
                    
                    drawPolygon(x1, p1[1],    
                            x2, p2[1],      
                            x2, 400,        
                            x1, 400,        
                            fill='white')   
                    
                    drawLine(x1, p1[1], x2, p2[1], 
                            fill=rgb(230, 230, 230), lineWidth=2)

        
        
        if app.isRaining:
            for drop in app.raindrops:
                drawLine(drop[0], drop[1], 
                        drop[0], drop[1] + 10, 
                        fill='lightBlue', 
                        lineWidth=1)
                
        drawImage('newSnowboarder.png', 
                app.charX - app.snowboarderWidth/2, 
                app.charY - app.snowboarderHeight/2 + 22, 
                width=app.snowboarderWidth, 
                height=app.snowboarderHeight,
                align='center',
                rotateAngle=math.degrees(app.charAngle))

        velocity = rounded(((app.velocityX**2 + app.velocityY**2)**0.5))
        drawLabel(f'Speed: {velocity}', 200, 20, size=16, bold=True, fill='navy')

def main():
    runApp()

main()
