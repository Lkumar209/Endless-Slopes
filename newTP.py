from cmu_graphics import *
import random
import math

def resetGame(app):
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

    app.ballRadius = 10
    app.ballX = 20
    app.ballY = 150  

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

    app.trail = []
    app.trailLength = 20

def generateDiverseCurvePoints(startX, startY):
    minY = 100
    maxY = 350
    
    # More dramatic elevation changes
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
    
    # Create more pronounced hills and valleys
    curve = random.choice(curve_styles)()
    
    # Ensure more dramatic height differences
    endY = curve[3][1]
    if abs(endY - startY) < 40:  # If the change is too small
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
    app.curves = []  
    resetGame(app)

def onKeyPress(app, key):
    if key == 'space':

        app.ballX = 20
        app.ballY = 150
        app.velocityX = 0
        app.velocityY = 0
        app.onCurve = False
        app.trail = []
        app.scrollX = 0  

    if key == 'r':

        resetGame(app)

def onStep(app):

    if app.ballX > 100:  
        diff = app.ballX - 100
        app.scrollX += diff
        app.ballX = 100  

    lastCurve = app.curves[-1]
    if lastCurve[3][0] - app.scrollX < 800:  
        nextCurve = generateDiverseCurvePoints(lastCurve[3][0], lastCurve[3][1])
        app.curves.append(nextCurve)

    while app.curves and app.curves[0][3][0] < app.scrollX:
        app.curves.pop(0)

    app.trail.append((app.ballX, app.ballY))
    if len(app.trail) > app.trailLength:
        app.trail.pop(0)

    closestPoint, distance = findClosestPointOnCurve(app, app.ballX, app.ballY)

    if closestPoint is None:
        return

    if not app.onCurve:

        app.velocityY += app.airGravity
        app.ballX += app.velocityX
        app.ballY += app.velocityY

        app.velocityX = max(app.velocityX * app.airControl, app.baseSpeed)

        if distance <= app.ballRadius:
            app.onCurve = True
            app.ballX = closestPoint[0]
            app.ballY = closestPoint[1] - app.ballRadius
            app.velocityX = max(app.velocityX, app.baseSpeed)
            app.velocityY = 0
    else:
        nextPoint = findClosestPointOnCurve(app, app.ballX + 1, app.ballY)[0]
        if nextPoint is None:
            return

        dx = nextPoint[0] - closestPoint[0]
        dy = nextPoint[1] - closestPoint[1]
        slopeAngle = math.atan2(dy, dx)

        if dy > 0:  
            accelerationX = app.gravity * math.sin(slopeAngle) * 1.5
        else:  
            accelerationX = app.gravity * math.sin(slopeAngle) * 0.8

        app.velocityX += accelerationX
        app.velocityX *= (1 - app.friction)

        app.velocityX = max(app.velocityX, app.baseSpeed)

        if dy < -0.4 and app.velocityX > app.baseSpeed:  
            app.onCurve = False
            app.velocityY = -8  
            app.velocityX *= app.rampBoost

        if abs(app.velocityX) > app.maxSpeed:
            app.velocityX = app.maxSpeed * (app.velocityX / abs(app.velocityX))

        app.ballX += app.velocityX

        closestPoint = findClosestPointOnCurve(app, app.ballX, app.ballY)[0]
        if closestPoint is not None:
            app.ballY = closestPoint[1] - app.ballRadius
        else:
            app.onCurve = False

def redrawAll(app):
    drawRect(0, 0, 400, 400, fill='lightCyan')

    for curve in app.curves:
        points = generateCurvePoints(curve)
        for i in range(len(points)-1):
            p1 = points[i]
            p2 = points[i+1]

            x1 = p1[0] - app.scrollX
            x2 = p2[0] - app.scrollX
            if 0 <= x1 <= 400 or 0 <= x2 <= 400:  
                drawLine(x1, p1[1], x2, p2[1], fill='white', lineWidth=8)
                drawLine(x1, p1[1], x2, p2[1], fill='lightGray', lineWidth=4)

    for i, (trailX, trailY) in enumerate(app.trail):
        opacity = i / len(app.trail)
        blueValue = int(255 * opacity)
        drawCircle(trailX, trailY, app.ballRadius * 0.7, 
                  fill=rgb(0, 0, blueValue))
    velocity = rounded(((app.velocityX**2 + app.velocityY**2)**0.5))
    drawLabel(f'Speed: {velocity}', 200, 20, size=16, bold=True, fill='navy')    

    drawCircle(app.ballX, app.ballY, app.ballRadius, fill='blue')

    drawLabel('Press SPACE to reset ball', 200, 50, size=16, bold=True,
              fill='navy')
    drawLabel('Press R to reset game', 200, 70, size=16, bold=True,
              fill='navy')

def main():
    runApp()

main()