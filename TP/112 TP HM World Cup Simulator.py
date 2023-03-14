## 112 Term Project Hugo Martinez
## World Cup Simulator
import math, copy, random

from cmu_112_graphics import *
#Team class: Every nation will be of this class
class Team:
    def __init__(self, name, overall, flag, kit):
        self.name = name
        self.overall = overall
        self.flag = flag
        self.kit = kit
        #Keeps track of points in group stage
        self.points = 0
        #Boolean that will determine whether or not the team is in the next round
        self.qualified = False
        #gp == Games Played
        self.gp = 0
        self.players = dict()
        for position in ['gk', 'lb', 'lcb', 'rcb', 'rb', 'cm', 'cdm', 'cam', 'lw', 'st', 'rw']:
            self.players[position] = Player(position, (0,0))
        self.state = 0

    def win(self):
        self.points += 3
        self.gp += 1

    def draw(self):
        self.points += 1
        self.gp += 1

    def loss(self):
        self.gp += 1

#Player class so that I can draw them and also know if they have the ball
class Player:
    def __init__(self, position, coordinates):
        self.position = position
        self.coordinates = coordinates
        self.hasBall = False
        self.facing = 'a'
        self.selected = False

    def makePass(self, app, t = 0):
        if self.hasBall == False:
            return 
        if t == 0:
            team = app.team.players
        else:
            team = app.opposition.players
        selfX, selfY = self.coordinates
        bestDis = 100000
        bestPos = ''
        for position in team:
            teammateX, teammateY = team[position].coordinates
            d = distance(teammateX - selfX, teammateY - selfY)
            if self.facing == 'd':
                if teammateX > selfX and teammateY > selfY - 150 and teammateY < selfY + 150:
                    if d < bestDis:
                        bestDis = d
                        bestPos = position
                    self.hasBall = False
            elif self.facing == 'a':
                if teammateX < selfX and teammateY > selfY - 150 and teammateY < selfY + 150:
                    if d < bestDis:
                        bestDis = d
                        bestPos = position
                    self.hasBall = False
            elif self.facing == 's':
                if teammateY > selfY and teammateX > selfX - 150 and teammateX < selfX + 150:
                    if d < bestDis:
                        bestDis = d
                        bestPos = position
                    self.hasBall = False             
            elif self.facing == 'w':
                if teammateY < selfY and teammateX > selfX - 150 and teammateX < selfX + 150:
                    if d < bestDis:
                        bestDis = d
                        bestPos = position
                    self.hasBall = False

        if self.hasBall == False:
            clearBalls(app)
            app.ballPossessed = False
            app.passing = True
            app.ballTarget = team[bestPos].coordinates, team[bestPos]
            self.selected = False
            team[bestPos].selected = True
            switchPlayer(app, bestPos, t)
            return
        
    def shoot(self, app, t=0):
        if self.hasBall == False:
            return
        self.hasBall = False
        app.ballPossessed = False
        app.shooting = True
        if t == 1:
            n = random.randint(0, 7)
            app.shotColor = ['red', 'orange', 'orange', 'yellow','yellow','yellow','yellow','lime', 'lime'][n]
        if app.shotColor == 'red':
            timing = 200
        elif app.shotColor == 'orange':
            timing = 50
        elif app.shotColor == 'yellow':
            timing = 15
        elif app.shotColor == 'lime':
            timing = 5
        else:
            timing = 200
        if t == 0:
            distFactor = abs(app.width - app.margX - app.ballX) - 150
        else:
            distFactor = 0
        if distFactor <= 0:
            distFactor = 0
        else:
            distFactor = (distFactor//50)**2

        if t == 0:
            timing += distFactor
            off = random.randint(-timing, timing)
            if app.ballY > app.centerY + 50:
                app.ballTarget = (app.width - app.margX, app.centerY - 45 + off), ''
            elif app.ballY < app.centerY - 50:
                app.ballTarget = (app.width - app.margX, app.centerY + 45 + off), ''
            else:
                direction = random.randint(0, 1)
                if direction == 1:
                    app.ballTarget = (app.width - app.margX, app.centerY + 45 + off), ''
                else:
                    app.ballTarget = (app.width - app.margX, app.centerY - 45 + off), ''
        if t == 1:
            timing += distFactor
            off = random.randint(-timing, timing)
            direction = random.randint(0, 1)
            if direction == 1:
                app.ballTarget = (app.margX, app.centerY + 45 + off), ''
            else:
                app.ballTarget = (app.margX, app.centerY - 45 + off), ''        

def distance(x, y):
    return (x**2 + y**2)**0.5

def bound(n, maxi, mini):
    if n > maxi:
        return maxi
    elif n < mini:
        return mini
    else:
        return n

def appStarted(app):
    #Initializing Teams  
    qatar = Team('Qatar', 75, 
            'https://cdn.countryflags.com/thumbs/qatar/flag-square-250.png', 
            'brown')
    germany = Team('Germany', 88, 
            'https://cdn.countryflags.com/thumbs/germany/flag-square-250.png',
             'white')
    england = Team('England', 85, 
            'https://cdn.countryflags.com/thumbs/england/flag-square-250.png',
            'red')
    mexico = Team('Mexico', 80, 
            'https://cdn.countryflags.com/thumbs/mexico/flag-square-250.png', 
            'lime')
    serbia = Team('Serbia', 78,
            'https://cdn.countryflags.com/thumbs/serbia/flag-square-250.png',
            'dark red')
    france = Team('France', 90, 
            'https://cdn.countryflags.com/thumbs/france/flag-square-250.png', 
            'blue')
    usa = Team('USA', 80, 
            'https://cdn.countryflags.com/thumbs/united-states-of-america/flag-square-250.png', 
            'black')
    brazil = Team('Brazil', 88,
            'https://cdn.countryflags.com/thumbs/brazil/flag-square-250.png', 
            'light green')
    spain = Team('Spain', 87,
            'https://cdn.countryflags.com/thumbs/spain/flag-square-250.png',
            'yellow')
    argentina = Team('Argentina', 87, 
            'https://cdn.countryflags.com/thumbs/argentina/flag-square-250.png', 
            'light blue')
    netherlands = Team('Netherlands', 85,
            'https://cdn.countryflags.com/thumbs/netherlands/flag-square-250.png',
            'orange')
    app.mode = 'startMode'
    app.kickDelay = 0
    app.margX = 18
    app.margY = 25
    app.centerX = app.width/2
    app.centerY = app.height/2
    app.teamsList = [france, brazil, spain, argentina, qatar, germany, england, mexico, serbia, usa, netherlands]
    app.index = 0
    app.team = app.teamsList[app.index]
    app.teamFlag = app.loadImage(app.team.flag)
    app.randomIndex = random.randint(0, len(app.teamsList) - 1)
    app.opposition = app.teamsList[app.randomIndex]
    app.oppFlag = app.loadImage(app.opposition.flag)
    app.selectedPlayer = 'st'
    app.currBaller = ''
    app.currPX = 0
    app.currPY = 0
    app.currFacing = ''
    app.ballX = 0
    app.ballY = 0
    app.playerShooting = False
    app.shotTiming = 0
    app.shotTimingDelayed = 0
    app.shotColor = 'red'
    app.shooting = False
    app.passing = False
    app.ballPossessed = True
    app.ballTarget = 0, 0, ''
    app.teamScore = 0
    app.oppScore = 0
    app.clock = 0
    app.counter = 0
    app.shotBarAnimation = False
    app.shotBarAnimCount = 0
    app.possessCooldown = 0
    app.possessSwitch = False
    app.homePossession = True
    app.oppositionPossession = False
    app.kickoff = False
    app.speed = 5
    
def refreshBall(app):
    if app.ballPossessed == False:
        target, position = app.ballTarget
        targetX, targetY = target
        ballPos, done = adjust(targetX, targetY, app.ballX, app.ballY, 15)
        app.ballX, app.ballY = ballPos
        if done == True and app.passing == True:
            app.ballPossessed = True
            position.hasBall = True
            position.selected = True
            app.currBaller = position
            app.passing = False
            app.ballX, app.ballY = position.coordinates
        if done == True and app.shooting == True:
            app.ballPossessed = True
            app.shooting = False
            app.ballX, app.ballY = targetX, targetY
    else:
        for x in [0, 1]:
            if x == 0:
                t = app.team.players
            else:
                t = app.opposition.players
            for player in t:
                if t[player].hasBall == True:
                    x, y = t[player].coordinates
                    app.ballX, app.ballY = x, y

#Team refreshes on a key press on the start menu
def refreshTeams(app):
    app.team = app.teamsList[app.index]
    app.teamFlag = app.loadImage(app.team.flag)
    app.opposition = app.teamsList[app.randomIndex]
    app.oppFlag = app.loadImage(app.opposition.flag)

def startMode_redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill = app.team.kit)
    canvas.create_text(app.centerX, app.centerY - 200, text = 'Select Your Team!', fill = 'black', font = '20')
    canvas.create_text(app.centerX, app.centerY - 170, text = f'{app.team.name} Overall: {app.team.overall}', font = '20')
    canvas.create_image(app.centerX, app.centerY, image = ImageTk.PhotoImage(app.teamFlag))
    canvas.create_text(app.centerX, app.height - 25, text = 'Press Enter to Continue!', fill = 'black')

def startMode_keyPressed(app, event):
    if event.key == 'Left':
        app.index -= 1
        if app.index < 0:
            app.index = len(app.teamsList) - 1
    elif event.key == 'Right':
        app.index += 1
        if app.index >= len(app.teamsList):
            app.index = 0
    while app.index == app.randomIndex:
        app.randomIndex = random.randint(0, len(app.teamsList)-1)
    refreshTeams(app)
    if event.key == 'Enter':
        app.mode = 'gameMode'
        resetPositions(app, app.team.players, app.opposition.players)

#Game Mode
def refreshPlayerPos(app):
    app.team.players[app.selectedPlayer].coordinates = (app.currPX, app.currPY)
    app.team.players[app.selectedPlayer].facing = app.currFacing

    refreshGKs(app)
    refreshPlrs(app, app.team.players, app.opposition.players)

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
    y = round(dY/smallest)
    x = round(dX/smallest)
    return y, x

def pythag(d, y, x):
    signx = 1 if x >=0 else -1
    signy = 1 if y >=0 else -1

    if x == 0:
        y = d*signy
        x = 0
    elif y == 0:
        x = d*signx
        y = 0
    else:    
        m = abs(y/x)
        x = signx*(d**2/(1 + m**2))**0.5
        y = signy*abs(x)*abs(m)

    return round(x), round(y)

def findYIntersection(x, app, team):
    if team == 1:
        dY, dX = slope(app.ballX, app.ballY - app.centerY)
    else:
        dY, dX = slope(app.width - app.ballX, app.ballY - app.centerY)
        x = app.width - x
    if dX == 0 or dY == 0:
        m = 0
    else:
        m = dY/dX
    y = m*x + app.centerY
    return y

def adjust(targetX, targetY, x, y, v= 3):
        xTrue, yTrue, both = False, False, False
        sY, sX = slope(targetX - x, targetY - y)
        dX, dY = pythag(v, sY, sX)
        if x < targetX - dX or x > targetX + dX:
            x += dX
        else:
            xTrue = True
        if y < targetY - dY or y > targetY + dY:
            y += dY
        else:
            yTrue = True
        if xTrue and yTrue:
            both = True
        return (x, y), both

def nearBall(app, x, y):
    if distance(x - app.ballX, y - app.ballY) < 100:
        return True
    else:
        return False

def refreshGKs(app):
    ## Your GK
    x, y = app.team.players['gk'].coordinates
    factor = ((app.ballX - 125)/(650))
    targetX = round(10+135*(factor))
    targetY = round(findYIntersection(targetX, app, 1))
    app.team.players['gk'].coordinates, throwaway = adjust(targetX, targetY, x, y, 3)
    if app.ballX < 140:
        app.team.players['gk'].coordinates, throwaway = adjust(10, app.centerY, x, y, 3)
    ## Opposition gk
    x, y = app.opposition.players['gk'].coordinates
    factor = 1-((app.ballX - 750)/(650))
    targetX = round((app.width - 10)-135*(factor))
    targetY = round(findYIntersection(targetX, app, -1))
    app.opposition.players['gk'].coordinates, throwaway = adjust(targetX, targetY, x, y, 3)
    if app.ballX > app.width - 140:
        app.opposition.players['gk'].coordinates, throwaway = adjust(app.width - 10, app.centerY, x, y, 3)
    
def refreshPlrs(app, home, away):
    #ballstuff
    if app.ballX < app.centerX - 50:
        offX = bound((app.ballX - app.centerX), 100, 0)
        offY = bound(app.ballY - app.centerY, 80, -80)
    else:
        offX = bound((app.ballX - app.centerX)*4, 700, 0)
        offY = bound(app.ballY - app.centerY, 80, -80)
    ## You
    lbx, lby = home['lb'].coordinates
    if home['lb'].hasBall == True or home['lb'].selected:
        pass
    elif nearBall(app, lbx, lby) and app.homePossession == False:
        home['lb'].coordinates, t = adjust(app.ballX, app.ballY, lbx, lby)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['lb'].coordinates, t = adjust(276 + offX, 140 + offY, lbx, lby)

    lcbx, lcby = home['lcb'].coordinates
    if home['lcb'].hasBall == True or home['lcb'].selected:
        pass
    elif nearBall(app, lcbx, lcby) and app.homePossession == False:
        home['lcb'].coordinates, t = adjust(app.ballX, app.ballY, lcbx, lcby)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['lcb'].coordinates, t = adjust(256 + offX, 320 + offY, lcbx, lcby)

    rcbx, rcby = home['rcb'].coordinates
    if home['rcb'].hasBall == True or home['rcb'].selected:
        pass
    elif nearBall(app, rcbx, rcby) and app.homePossession == False:
        home['rcb'].coordinates, t = adjust(app.ballX, app.ballY, rcbx, rcby)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['rcb'].coordinates, t = adjust(256 + offX, 480 + offY, rcbx, rcby)

    rbx, rby = home['rb'].coordinates
    if home['rb'].hasBall == True or home['rb'].selected:
        pass
    elif nearBall(app, rbx, rby) and app.homePossession == False:
        home['rb'].coordinates, t = adjust(app.ballX, app.ballY, rbx, rby)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['rb'].coordinates, t = adjust(276 + offX, 660 + offY, rbx, rby)

    cmx, cmy = home['cm'].coordinates
    if home['cm'].hasBall == True or home['cm'].selected:
        pass
    elif nearBall(app, cmx, cmy) and app.homePossession == False:
        home['cm'].coordinates, t = adjust(app.ballX, app.ballY, cmx, cmy)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['cm'].coordinates, t = adjust(462 + offX, 200 + offY, cmx, cmy)

    camx, camy = home['cam'].coordinates
    if home['cam'].hasBall == True or home['cam'].selected:
        pass
    elif nearBall(app, camx, camy) and app.homePossession == False:
        home['cam'].coordinates, t = adjust(app.ballX, app.ballY, camx, camy)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['cam'].coordinates, t = adjust(562 + offX, 400 + offY, camx, camy)

    cdmx, cdmy = home['cdm'].coordinates
    if home['cdm'].hasBall == True or home['cdm'].selected:
        pass
    elif nearBall(app, cdmx, cdmy) and app.homePossession == False:
        home['cdm'].coordinates, t = adjust(app.ballX, app.ballY, cdmx, cdmy)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['cdm'].coordinates, t = adjust(462 + offX, 600 + offY, cdmx, cdmy)

    lwx, lwy = home['lw'].coordinates
    if home['lw'].hasBall == True or home['lw'].selected:
        pass
    elif nearBall(app, lwx, lwy) and app.homePossession == False:
        home['lw'].coordinates, t = adjust(app.ballX, app.ballY, lwx, lwy)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['lw'].coordinates, t = adjust(668 + offX, 135 + offY, lwx, lwy)

    stx, sty = home['st'].coordinates
    if home['st'].hasBall == True or home['st'].selected:
        pass
    elif nearBall(app, stx, sty) and app.homePossession == False:
        home['st'].coordinates, t = adjust(app.ballX, app.ballY, stx, sty)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['st'].coordinates, t = adjust(718 + offX, 400 + offY, stx, sty)

    rwx, rwy = home['rw'].coordinates  
    if home['rw'].hasBall == True or home['rw'].selected:
        pass
    elif nearBall(app, rwx, rwy) and app.homePossession == False:
        home['rw'].coordinates, t = adjust(app.ballX, app.ballY, rwx, rwy)
    else:
        if random.randint(0, (app.team.overall - 75)) != 1:
            home['rw'].coordinates, t = adjust(668 + offX, 665 + offY, rwx, rwy)

    ##Opposition
    if app.ballX > app.centerX + 50:
        offX = bound((app.ballX - app.centerX), 200, 0)
        offY = bound(app.ballY - app.centerY, 80, -80)
    else:
        offX = bound((app.ballX - app.centerX)*4, 0, -700)
        offY = bound(app.ballY - app.centerY, 80, -80)

    if away['gk'].hasBall == True or away['gk'].selected == True:
        oppAI(app, 'gk')
    lbx, lby = away['lb'].coordinates
    if nearBall(app, lbx, lby) and app.homePossession == True:
        away['lb'].coordinates, t = adjust(app.ballX, app.ballY, lbx, lby)
    elif away['lb'].hasBall == True or away['lb'].selected == True:
        oppAI(app, 'lb')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['lb'].coordinates, t = adjust(app.width - 276 + offX, 140 + offY, lbx, lby)
    lcbx, lcby = away['lcb'].coordinates
    if nearBall(app, lcbx, lcby) and app.homePossession == True:
        away['lcb'].coordinates, t = adjust(app.ballX, app.ballY, lcbx, lcby)
    elif away['lcb'].hasBall == True or away['lcb'].selected == True:
        oppAI(app, 'lcb')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['lcb'].coordinates, t = adjust(app.width - 256 + offX, 320 + offY, lcbx, lcby)
    rcbx, rcby = away['rcb'].coordinates
    if nearBall(app, rcbx, rcby) and app.homePossession == True:
        away['rcb'].coordinates, t = adjust(app.ballX, app.ballY, rcbx, rcby)
    elif away['rcb'].hasBall == True or away['rcb'].selected == True:
        oppAI(app, 'rcb')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['rcb'].coordinates, t = adjust(app.width - 256 + offX, 480 + offY, rcbx, rcby)
    rbx, rby = away['rb'].coordinates
    if nearBall(app, rbx, rby) and app.homePossession == True:
        away['rb'].coordinates, t = adjust(app.ballX, app.ballY, rbx, rby)
    elif away['rb'].hasBall == True or away['rb'].selected == True:
        oppAI(app, 'rb')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['rb'].coordinates, t = adjust(app.width - 276 + offX, 660 + offY, rbx, rby)
    cmx, cmy = away['cm'].coordinates
    if nearBall(app, cmx, cmy) and app.homePossession == True:
        away['cm'].coordinates, t = adjust(app.ballX, app.ballY, cmx, cmy)
    elif away['cm'].hasBall == True or away['cm'].selected == True:
        oppAI(app, 'cm')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['cm'].coordinates, t = adjust(app.width - 462 + offX, 200 + offY, cmx, cmy)
    camx, camy = away['cam'].coordinates
    if nearBall(app, camx, camy) and app.homePossession == True:
        away['cam'].coordinates, t = adjust(app.ballX, app.ballY, camx, camy)
    elif away['cam'].hasBall == True or away['cam'].selected == True:
        oppAI(app, 'cam')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['cam'].coordinates, t = adjust(app.width - 562 + offX, 400 + offY, camx, camy)
    cdmx, cdmy = away['cdm'].coordinates
    if nearBall(app, cdmx, cdmy) and app.homePossession == True:
        away['cdm'].coordinates, t = adjust(app.ballX, app.ballY, cdmx, cdmy)
    elif away['cdm'].hasBall == True or away['cdm'].selected == True:
        oppAI(app, 'cdm')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['cdm'].coordinates, t = adjust(app.width - 462 + offX, 600 + offY, cdmx, cdmy)
    lwx, lwy = away['lw'].coordinates
    if nearBall(app, lwx, lwy) and app.homePossession == True:
        away['lw'].coordinates, t = adjust(app.ballX, app.ballY, lwx, lwy)
    elif away['lw'].hasBall == True or away['lw'].selected == True:
        oppAI(app, 'lw')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['lw'].coordinates, t = adjust(app.width - 668 + offX, 135 + offY, lwx, lwy)
    stx, sty = away['st'].coordinates   
    if nearBall(app, stx, sty) and app.homePossession == True:
        away['st'].coordinates, t = adjust(app.ballX, app.ballY, stx, sty)
    elif away['st'].hasBall == True or away['st'].selected == True:
        oppAI(app, 'st')
    else:
        if random.randint(0, (app.opposition.overall - 75)) != 1:
            away['st'].coordinates, t = adjust(app.width - 718 + offX, 400 + offY, stx, sty)
    rwx, rwy = away['rw'].coordinates
    if nearBall(app, rwx, rwy) and app.homePossession == True:
        away['rw'].coordinates, t = adjust(app.ballX, app.ballY, rwx, rwy)
    elif away['rw'].hasBall == True or away['rw'].selected == True:
        oppAI(app, 'rw')
    else:
        if random.randint(0, (93 - app.opposition.overall)) != 1:
            away['rw'].coordinates, t = adjust(app.width - 668 + offX, 665 + offY, rwx, rwy)

def oppAI(app, pos):
    pX, pY = app.opposition.players[pos].coordinates
    n = random.randint(0, 11)
    app.opposition.players[pos].facing = ['a', 'a', 'a', 'a', 'w', 's', 'w', 's', 'w', 's', 'd', 'd'][n]
    if oppositionNearby(pX, pY, app):
        overallEffect = app.opposition.overall - 80
        overallEffect = bound(overallEffect, 1, 10)
        if random.randint(0,overallEffect) != 1:
            app.opposition.players[pos].makePass(app, 1)
            if app.passing == True:
                return
    else:
        if (app.ballX, app.ballY) != app.opposition.players[pos].coordinates:
            pass
        else:
            if pX > 300:
                app.opposition.players[pos].coordinates = pX - app.speed, pY
            else:
                app.opposition.players[pos].coordinates, t = adjust(app.margX, app.centerY, pX, pY)
            if pX < 100:
                app.opposition.players[pos].shoot(app, 1)

def oppositionNearby(x, y, app):
    for player in app.team.players:
        oppX, oppY = app.team.players[player].coordinates
        if distance(oppX - x, oppY - y) <= 50:
            return True
    return False

def resetPositions(app, home, away, offX = 0, offXA = 0, pos = 'st'):
    if app.oppositionPossession == True:
        app.homePossession = False
        away[pos].hasBall = True
        app.currBaller = app.opposition.players[pos]
        stAX, stAY = 768, 400
        stHX, stHY = app.centerX - 30, app.centerY - 130
    else:
        app.oppositionPossession = False
        app.selectedPlayer = pos
        home[pos].hasBall = True
        home[pos].selected = True
        app.currBaller = app.team.players[pos]
        stHX, stHY = 768, 400
        stAX, stAY = app.centerX + 30, app.centerY + 130
    home['gk'].coordinates = (35 + offX, 400)
    home['lb'].coordinates = (276 + offX, 140)
    home['lcb'].coordinates = (256 + offX, 320)
    home['rcb'].coordinates = (256 + offX, 480)
    home['rb'].coordinates = (276 + offX, 660)
    home['cm'].coordinates = (462 + offX, 200)
    home['cam'].coordinates = (562 + offX, 400)
    home['cdm'].coordinates = (462 + offX, 600)
    home['lw'].coordinates = (668 + offX, 135)
    home['st'].coordinates = (stHX + offX, stHY)
    home['rw'].coordinates = (668 + offX, 665)

    away['gk'].coordinates = (app.width - 35 + offXA, app.centerY)
    away['lb'].coordinates = (app.width - 276 + offXA, app.height/5 - 20)
    away['lcb'].coordinates = (app.width - 256 + offXA, app.height*(2/5))
    away['rcb'].coordinates = (app.width - 256 + offXA, app.height*(3/5))
    away['rb'].coordinates = (app.width - 276 + offXA, app.height*(4/5) + 20)
    away['cm'].coordinates = (app.width - 462 + offXA, app.height/4)
    away['cam'].coordinates = (app.width - 562 + offXA, app.centerY)
    away['cdm'].coordinates = (app.width - 462 + offXA, app.height*(3/4))
    away['lw'].coordinates = (app.width -  668 + offXA, app.height / 6)
    away['st'].coordinates = (stAX + offXA, stAY)
    away['rw'].coordinates = (app.width - 668 + offXA, app.height*(5/6))

    app.currPX, app.currPY = app.team.players[app.selectedPlayer].coordinates
    app.currFacing = app.team.players[app.selectedPlayer].facing

def resetBall(app):
    app.ballX = app.centerX
    app.ballY = app.centerY
    app.shooting = False
    app.passing = False
    app.ballPossessed = True
    app.ballTarget = 0, 0, ''

def switchPlayer(app, bestPos = None, t = 0):
    if t == 0:
        team = app.team.players
        if bestPos == None:
            bestDis = 100000
            bestPos = ''
            for position in team:
                if position == app.selectedPlayer or position == 'gk':
                    continue
                teammateX, teammateY = team[position].coordinates
                d = distance(teammateX - app.ballX, teammateY - app.ballY)
                if d < bestDis:
                    bestDis = d
                    bestPos = position
        team[app.selectedPlayer].selected = False
        app.selectedPlayer = bestPos
        team[bestPos].selected = True
        app.currPX, app.currPY = team[bestPos].coordinates
    else:
        return

# Collision / Event Checks
def checkGoal(app):
    if app.ballX >= app.width - app.margX:
        if app.ballY < app.centerY + 50 and app.ballY > app.centerY - 50:
            app.teamScore += 1
            app.oppositionPossession = True
            app.homePossession = False
            resetPositions(app, app.team.players, app.opposition.players)
            resetBall(app)
        else:
            return False
    elif app.ballX <= app.margX:
        if app.ballY < app.centerY + 50 and app.ballY > app.centerY - 50:
            app.oppScore += 1
            app.homePossession = True
            app.oppositionPossession = False
            resetPositions(app, app.team.players, app.opposition.players)
            resetBall(app)
        else:
            return False
    else:
        return False
    app.kickoff = False

def checkPBCollision(app):
    for n in [0, 1]:
        if n == 0:
            t = app.team.players
        else:
            t = app.opposition.players
        if app.possessSwitch == False:
            for player in t:
                if t[player].hasBall == True:
                    continue
                else:
                    x, y = t[player].coordinates
                    if x > app.ballX - 10 and x < app.ballX + 10 and y > app.ballY - 10 and y < app.ballY + 10:
                        if app.currBaller != None:
                            app.currBaller.hasBall = False
                        if n == 0:
                            switchPlayer(app, player)
                        clearBalls(app)
                        t[player].hasBall = True
                        t[player].selected = True
                        app.currBaller = t[player]
                        app.ballX = x
                        app.ballY = y
                        app.shooting = False
                        app.passing = False
                        app.ballPossessed = True
                        app.ballTarget = 0, 0, ''
                        app.possessSwitch = True

def checkOOB(app):
    if app.ballX < app.centerX:
        offXH = bound((app.ballX - app.centerX), 200, 0)
        offXA = bound((app.ballX - app.centerX), 0, -350)
    else:
        offXH = bound((app.ballX - app.centerX), 350, 0)
        offXA = bound((app.ballX - app.centerX), -200, 0)

    if app.ballX <= app.margX and checkGoal(app) == False:
        app.kickoff = False
        app.homePossession = True
        app.oppositionPossession = False
        app.team.players[app.selectedPlayer].hasBall = False
        app.team.players[app.selectedPlayer].selected = False
        clearBalls(app)
        app.team.players['gk'].facing = 'd'
        resetPositions(app, app.team.players, app.opposition.players, offXH, offXA, 'gk')
        app.team.players['gk'].coordinates = app.margX + 50, app.centerY

    elif app.ballX >= app.width - app.margX and checkGoal(app) == False:
        app.kickoff = False
        app.team.players[app.selectedPlayer].hasBall = False
        app.team.players[app.selectedPlayer].selected = False
        app.oppositionPossession = True
        app.homePossession = False
        clearBalls(app)
        resetPositions(app, app.team.players, app.opposition.players, offXH, offXA)
        app.opposition.players['gk'].coordinates = app.width - app.margX - 50, app.centerY
        app.opposition.players['gk'].hasBall = True
        app.ballX, app.ballY = app.opposition.players['gk'].coordinates
        app.currBaller = app.team.players['gk']


    elif app.ballY < app.margY:
        x, y = app.ballX, app.ballY
        if app.homePossession:
            team = app.opposition.players
            app.homePossession = False
            app.oppositionPossession = True
        else:
            team = app.team.players
            app.homePossession = True
            app.oppositionPossession = False
        resetBall(app)
        resetPositions(app, app.team.players, app.opposition.players, offXH, offXA)
        app.ballX, app.ballY = x, y
        bestDis = 100000
        bestPos = ''
        for position in team:
            if position == 'gk':
                continue
            teammateX, teammateY = team[position].coordinates
            d = distance(teammateX - app.ballX, teammateY - app.ballY)
            if d < bestDis:
                bestDis = d
                bestPos = position
        clearBalls(app)
        team[bestPos].coordinates = app.ballX, app.margY
        team[bestPos].hasBall = True
        team[bestPos].facing = 's'
        app.currBaller = team[bestPos]
        app.kickoff = False

    elif app.ballY > app.height - app.margY:
        x, y = app.ballX, app.ballY
        if app.homePossession:
            team = app.opposition.players
            app.homePossession = False
            app.oppositionPossession = True
        else:
            team = app.team.players
            app.homePossession = True
            app.oppositionPossession = False
        resetBall(app)
        resetPositions(app, app.team.players, app.opposition.players, offXH, offXA)
        app.ballX, app.ballY = x, y
        bestDis = 100000
        bestPos = ''
        for position in team:
            if position == 'gk':
                continue
            teammateX, teammateY = team[position].coordinates
            d = distance(teammateX - app.ballX, teammateY - app.ballY)
            if d < bestDis:
                bestDis = d
                bestPos = position
        clearBalls(app)
        team[bestPos].coordinates = app.ballX, app.height - app.margY
        team[bestPos].hasBall = True
        team[bestPos].facing = 'w'
        app.currBaller = team[bestPos]
        app.kickoff = False

def clearBalls(app):
    for player in app.team.players:
        app.team.players[player].hasBall = False
        app.team.players[player].selected = False
    for player in app.opposition.players:
        app.opposition.players[player].hasBall = False
        app.opposition.players[player].selected = False

def findBaller(app):
    for pos in app.opposition.players:
        if app.opposition.players[pos].hasBall == True:
            return pos

def gameMode_timerFired(app):
    #AI restart play
    if app.kickoff == False and app.oppositionPossession == True:
        app.kickDelay += 1
        if app.kickDelay == 10:
            pos = findBaller(app)
            app.opposition.players[pos].facing = 'd'
            app.opposition.players[pos].makePass(app, 1)
            app.kickoff = True

    #Check for possession
    if app.ballPossessed == True and app.team.players[app.selectedPlayer].hasBall == True:
        app.homePossession = True
        app.oppositionPossession = False
    elif app.ballPossessed == True:
        app.homePossession = False
        app.oppositionPossession = True
    
    #Possession Cooldown
    if app.possessSwitch == True:
        app.possessCooldown += 1
        if app.possessCooldown == 10:
            app.possessSwitch = False
            app.possessCooldown = 0

    #Current Baller update
    if app.ballPossessed == False:
        app.currBaller = None
    
    #Timed finishing
    if app.playerShooting == True:
        app.shotTiming += 3
        if app.shotTiming == 60:
            app.playerShooting = False
            app.shotTiming = 0

    #Timed finishing score
    elif app.playerShooting == False and app.shotTiming != 0:
        app.shotBarAnimation = True
        if app.shotTiming < 20:
            app.shotColor = 'red'
        elif app.shotTiming < 35:
            app.shotColor = 'orange'
        elif app.shotTiming < 40:
            app.shotColor = 'yellow'
        elif app.shotTiming < 45:
            app.shotColor = 'lime'
        elif app.shotTiming < 50:
            app.shotColor = 'yellow'
        elif app.shotTiming < 60:
            app.shotColor = 'orange'
        else:
            app.shotColor = 'red'
        app.team.players[app.selectedPlayer].shoot(app)
        app.shotTiming = 0

    #Shotbar
    if app.shotBarAnimation == True:
        app.shotBarAnimCount += 1

    if app.shotBarAnimCount == 5:
        app.shotBarAnimation = False
        app.shotColor = 'red'
        app.shotBarAnimCount = 0

    if app.kickoff == True:
        refreshPlayerPos(app)
        app.counter += 1
    refreshBall(app)

    if app.counter == 7:
        app.clock += 1
        app.counter = 0
    if app.clock == 45:
        app.mode = 'halfTime'
        app.kickoff = False
        app.homePossession = False
        app.oppositionPossession = True
        clearBalls(app)
        resetPositions(app, app.team.players, app.opposition.players)
        resetBall(app)
    if app.clock == 90:
        app.mode = 'gameOver'
        if app.teamScore > app.oppScore:
            app.winner = f'{app.team.name} wins!'
        elif app.teamScore < app.oppScore:
            app.winner = f'{app.opposition.name} wins'
        else:
            app.winner = 'Draw!'
        
    checkGoal(app)
    checkPBCollision(app)
    checkOOB(app)

def gameMode_keyPressed(app, event):
    if app.kickoff == True:
        if event.key == 'Escape':
            appStarted(app)
        elif event.key == 'Backspace':
            resetPositions(app, app.team.players, app.opposition.players)
        elif event.key == ';':
            switchPlayer(app)
        elif event.key == 'w':
            app.currPY -= 1
            app.currFacing = event.key
        elif event.key == 'a':
            app.currPX -= 1
            app.currFacing = event.key
        elif event.key == 's':
            app.currPY += 1
            app.currFacing = event.key
        elif event.key == 'd':
            app.currPX += 1
            app.currFacing = event.key
        elif event.key == 'j':
            app.team.players[app.selectedPlayer].makePass(app)
        elif event.key == 'k':
            if app.team.players[app.selectedPlayer].hasBall == True:
                if app.playerShooting == True:
                    app.playerShooting = False
                else:
                    app.playerShooting = True
    else:
        if event.key == 'j':
            app.team.players[app.selectedPlayer].makePass(app)
            app.kickoff = True

def drawPitchLines(app, canvas):
    centerCircRad = 100
    #field
    canvas.create_rectangle(0, 0, app.width, app.height, fill = 'green')
    #midfield
    canvas.create_rectangle(app.margX, app.margY, app.centerX, app.height - app.margY, outline = 'white', 
                            width = '3')
    canvas.create_rectangle(app.centerX, app.margY, app.width - app.margX, app.height - app.margY, 
                            outline = 'white', width = '3')
    #center circle
    canvas.create_oval(app.centerX - centerCircRad, app.centerY - centerCircRad, 
                            app.centerX + centerCircRad, 
                            app.centerY + centerCircRad, outline = 'white', 
                            width = '3')
    # 6 yard box
    canvas.create_rectangle(app.margX, app.centerY - 75, app.margX + 50, app.centerY + 75, 
                            outline = 'white', width = '3')
    canvas.create_rectangle(app.width - app.margX - 50, app.centerY - 75, app.width - app.margX, app.centerY + 75, 
                            outline = 'white', width = '3')
    # 18 yard box
    canvas.create_rectangle(app.margX, app.centerY - 125, app.margX + 125, app.centerY + 125, 
                            outline = 'white', width = '3')
    canvas.create_rectangle(app.width - app.margX - 125, app.centerY - 125, app.width - app.margX, app.centerY + 125, 
                            outline = 'white', width = '3')
    # Goals
    canvas.create_rectangle(7, app.centerY - 50, app.margX, app.centerY + 50, outline = 'white', width = '2')
    canvas.create_rectangle(app.width - app.margX, app.centerY - 50, app.width - 7, app.centerY + 50, outline = 'white', width = '2')

def drawPlayers(app, canvas):
    i = 1
    for position in app.team.players:
        x, y = app.team.players[position].coordinates
        if position == app.selectedPlayer:
            if position == 'gk':
                canvas.create_oval(x-25, y-25, x+25, y+25, fill = 'pink', outline = 'white', width = '2')
            else:
                canvas.create_oval(x-25, y-25, x+25, y+25, fill = app.team.kit, outline = 'white', width = '2')
        else: 
            if position == 'gk':
                canvas.create_oval(x-25, y-25, x+25, y+25, fill = 'pink')
            else:
                canvas.create_oval(x-25, y-25, x+25, y+25, fill = app.team.kit)
        canvas.create_text(x, y, text = f'{i}', fill = 'gray', font = 'Times 20 bold')
        i += 1
    i = 1
    for position in app.opposition.players:
        x, y = app.opposition.players[position].coordinates
        if position == 'gk':
            canvas.create_oval(x-25, y-25, x+25, y+25, fill = 'pink')
        else:
            canvas.create_oval(x-25, y-25, x+25, y+25, fill = app.opposition.kit)
        canvas.create_text(x, y, text = f'{i}', fill = 'gray', font = 'Times 20 bold')
        i += 1

def drawBall(app, canvas):
    canvas.create_oval(app.ballX - 5, app.ballY - 5, app.ballX + 5, app.ballY + 5, fill = 'white')

def drawScoreboard(app, canvas):
    canvas.create_rectangle(app.centerX - 30, 3, app.centerX + 30, 20, fill = 'gray', outline = 'black')
    canvas.create_text(app.centerX + 20, 10, text = f'{app.clock}', fill = 'black')
    canvas.create_text(app.centerX - 15, 10, text = f'{app.teamScore} - {app.oppScore}', fill = 'black')

def drawShotBar(app, canvas):
    playerX, playerY = app.team.players[app.selectedPlayer].coordinates
    if app.shotBarAnimation:
        canvas.create_rectangle(playerX - 30, playerY - 35, playerX + 30, playerY - 30, fill = app.shotColor)
    else:
        canvas.create_rectangle(playerX - 30, playerY - 35, playerX - 10, playerY - 30, fill = 'red')
        canvas.create_rectangle(playerX - 10, playerY - 35, playerX + 5, playerY - 30, fill = 'orange')
        canvas.create_rectangle(playerX + 5, playerY - 35, playerX + 10, playerY - 30, fill = 'yellow')
        canvas.create_rectangle(playerX + 10, playerY - 35, playerX + 15, playerY - 30, fill = 'lime')
        canvas.create_rectangle(playerX + 15, playerY - 35, playerX + 20, playerY - 30, fill = 'yellow')
        canvas.create_rectangle(playerX + 20, playerY - 35, playerX + 30, playerY - 30, fill = 'orange')
        canvas.create_rectangle(playerX - 30, playerY - 35, playerX + 30, playerY - 30, outline = 'black')
        
        timing = playerX - 30 + app.shotTiming
        canvas.create_rectangle(timing, playerY - 35, timing + 1, playerY - 30, fill = 'white')

def gameMode_redrawAll(app, canvas):
    drawPitchLines(app, canvas)
    drawPlayers(app, canvas)
    drawScoreboard(app, canvas)
    drawBall(app, canvas)
    if app.playerShooting or app.shotBarAnimation:
        drawShotBar(app, canvas)

## Half Time

def halfTime_redrawAll(app, canvas):
    canvas.create_text(app.centerX, app.height - 25, text = 'HT, Press Enter to Continue!', fill = 'black')
    canvas.create_text(app.centerX, app.height/2, text = f'{app.team.name} {app.teamScore} - {app.oppScore} {app.opposition.name}', fill = 'black', font = '60')

def halfTime_keyPressed(app, event):
    if event.key == 'Enter':
        app.mode = 'gameMode'
        pos = findBaller(app)
        app.opposition.players[pos].facing = 'd'
        app.clock += 1

## Full Time

def gameOver_redrawAll(app, canvas):
    canvas.create_text(app.centerX, app.height - 25, text = 'FT, Press Enter to Continue!', fill = 'black')
    canvas.create_text(app.centerX, app.height/2, text = f'{app.winner}!', fill = 'black', font = '80')
    canvas.create_text(app.centerX, app.height / 2 + 50, text = f'Final Score: \n {app.teamScore}-{app.oppScore}')
def gameOver_keyPressed(app, event):
    if event.key == 'Enter':
        app.mode = 'startMode'
        app.clock = 0

runApp(width=1536, height=800)