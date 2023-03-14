def appStarted(app):
    #Initializing Teams  
    qatar = Team('Qatar', 50, 
            'https://cdn.countryflags.com/thumbs/qatar/flag-square-250.png', 
            'maroon')
    germany = Team('Germany', 88, 
            'https://cdn.countryflags.com/thumbs/germany/flag-square-250.png',
             'white')
    denmark = Team('Denmark', 78, 
            'https://cdn.countryflags.com/thumbs/denmark/flag-square-250.png',
            'red')
    mexico = Team('Mexico', 80, 
            'https://cdn.countryflags.com/thumbs/mexico/flag-square-250.png', 
            'green')
    serbia = Team('Serbia', 78,
            'https://cdn.countryflags.com/thumbs/serbia/flag-square-250.png',
            'dark red')
        
    app.mode = 'startMode'
    app.centerX = app.width/2
    app.centerY = app.height/2
    app.teamsList = [qatar, germany, denmark, mexico, serbia]
    app.index = 0
    app.team = app.teamsList[app.index]
    app.teamFlag = app.loadImage(app.team.flag)
    app.opposition = app.teamsList[1]
    app.selectedPlayer = 'st'
    app.currPX = 0
    app.currPY = 0
    app.currFacing = ''
    app.ballX = 0
    app.ballY = 0
    app.clock = 0
    app.counter = 0
    app.timerDelay = 10

def slope(dX, dY):
    if dX == 0:
        smallest = abs(dY)
    elif dY == 0:
        smallest = abs(dX)
    elif abs(dX) > abs(dY):
        smallest = abs(dY)
    else:
        smallest = abs(dX)
    if smallest == 0:
        return 0, 0
    return round(dX/smallest), round(dY/smallest)

def adjust(targetX, targetY, x, y):
        dX, dY = slope(targetX - x, targetY - y)
        if x != targetX:
            x += dX
        if y != targetY:
            y += dY
        return x, y

# print(adjust(100, 100, 120, 120))

# print(adjust(100, 100, 0, 100))

def findYIntersection(x, app):
    dx, dy = slope(app.ballX, app.ballY - app.centerY)
    m = dy/dx
    y = m*x + app.centerY
    return y

print(findYIntersection(6, 10, 5, 0))




