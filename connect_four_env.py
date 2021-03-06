import pygame
import pygame.font
import time
import numpy as np
from simple_agent import SimpleAgent

class ConnectFourEnv:
    def __init__(self, display=False):
        self.display = display
        self.width = 7
        self.height = 6
        #self.width = 6
        #self.height = 5
        self.screenWidth = 640
        self.screenHeight = 480
        self.manualPos = -1
        self.winner = 0
        if self.display:
            self.initDisplay()
        self.reset()
        
    def initDisplay(self):
        pygame.init()
        self.screen=pygame.display.set_mode([self.screenWidth, self.screenHeight])
        self.fontobject = pygame.font.SysFont('Arial', 50)
        self.display = True
        print 'initDisplay()'
        
    def closeDisplay(self):
        self.display = False
        pygame.display.quit()
        
    def reset(self):
        self.state = np.zeros((self.height, self.width), dtype=np.int)
        self.state.fill(-1)
        self.gameOver = False
        self.winner = 0
        self.BLACK = (  0,   0,   0)
        self.WHITE = (255, 255, 255)
        self.BLUE =  (  0,   0, 255)
        self.GREEN = (  0, 255,   0)
        self.RED =   (255,   0,   0)
        self.oneGridWidth = self.screenWidth / self.width
        self.oneGridHeight = self.screenHeight / self.height
        
    def checkHorizontalStraight(self, state, x, y):
        if x > self.width - 4:
            return False, -1
        for player in [1, 2]:
            if state[y, x] == player and state[y, x+1] == player \
                    and state[y, x+2] == player and state[y, x+3] == player:
                return True, player
        return False, -1
        
    def checkVerticalStraight(self, state, x, y):
        if y > self.height - 4:
            return False, -1
        for player in [1, 2]:
            if state[y, x] == player and state[y+1, x] == player \
                    and state[y+2, x] == player and state[y+3, x] == player:
                return True, player
        return False, -1
        
    def checkDiagonalStraightDown(self, state, x, y):
        if x > self.width - 4 or y > self.height - 4:
            return False, -1
        for player in [1, 2]:
            if state[y, x] == player and state[y+1, x+1] == player \
                    and state[y+2, x+2] == player and state[y+3, x+3] == player:
                return True, player
        return False, -1
        
    def checkDiagonalStraightUp(self, state, x, y):
        if x > self.width - 4 or y < 3:
            return False, -1
        for player in [1, 2]:
            if state[y, x] == player and state[y-1, x+1] == player \
                    and state[y-2, x+2] == player and state[y-3, x+3] == player:
                return True, player
        return False, -1
    
    def checkGameOver(self, state=None):
        # Check game over
        
        if state == None:
            state = self.state

        gameDraw = True
        gameOver = False
        winner = -1
        for i in range(self.width):
            for j in range(self.height):
                gameOver, winner = self.checkHorizontalStraight(state, i, j)
                if gameOver:
                    break 
                gameOver, winner = self.checkVerticalStraight(state, i, j)
                if gameOver:
                    break 
                gameOver, winner = self.checkDiagonalStraightDown(state, i, j)
                if gameOver:
                    break 
                gameOver, winner = self.checkDiagonalStraightUp(state, i, j)
                if gameOver:
                    break 
            if gameOver:
                break
            
        if gameOver:
            return gameOver, winner
            
        # Check game draw        
        if gameOver == False:
            for i in range(self.width):
                for j in range(self.height):
                    if self.state[j, i] == -1:
                        gameDraw = False
                        break
                if gameDraw == False:
                    break

        if gameDraw == True:
            gameOver = True
            winner = -1
    
        return gameOver, winner 
    
    def availableActions(self, state):
        available = []
        for x in range(self.width):
            if state[0, x] == -1:
                available.append(x)
        return available
    
    def getState(self):
        return self.state.copy()
    
    def setState(self, state):
        self.state = state.copy()
    
    def isFull(self, state):
        if -1 in state:
            return False
        else:
            return True

    def getManualAction(self, state):
        availableActions = self.availableActions(state)
        pos = self.width / 2
        self.drawStage()
        
        while True:
            for event in pygame.event.get():
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_LEFT]:
                    pos -= 1
                    if pos == -1:
                        pos = 0
                if keystate[pygame.K_RIGHT]:
                    pos += 1
                    if pos == self.width:
                        pos = self.width - 1
                if keystate[pygame.K_DOWN] or keystate[pygame.K_RETURN]:
                    if pos in availableActions:
                        self.manualPos = -1
                        return pos
                self.manualPos = pos
                self.drawStage()

    def drawStage(self):
        self.screen.fill(self.WHITE)
        for x in range(self.width):
            pygame.draw.line(self.screen, self.BLACK, (x*self.oneGridWidth, 0), (x*self.oneGridWidth, self.screenHeight))
        for y in range(self.height):
            pygame.draw.line(self.screen, self.BLACK, (0, y*self.oneGridHeight), (self.screenWidth, y*self.oneGridHeight))
        for i in range(self.width):
            for j in range(self.height):
                if self.state[j, i] != -1:
                    color = self.BLUE if self.state[j, i] == 1 else self.RED
                    x = i * self.oneGridWidth + self.oneGridWidth / 2
                    y = j * self.oneGridHeight + self.oneGridHeight / 2
                    radius = self.oneGridWidth / 2 - 10
                    pygame.draw.circle(self.screen, color, [x ,y], radius, 0)

        if self.manualPos != -1:
            x = self.manualPos * self.oneGridWidth + self.oneGridWidth / 2
            y = self.oneGridHeight / 2
            radius = self.oneGridWidth / 2 - 10
            pygame.draw.circle(self.screen, self.RED, [x ,y], radius, 0)

        if self.winner == 1:
            message = 'You lost.'
        elif self.winner == 2:
            message = 'You won !!!'
        elif self.winner == -1:
            message = 'Game draws'
        else:
            message = None
        
        if message != None:
            print 'message : %s' % message
            self.screen.blit(self.fontobject.render(message, 1, self.GREEN),
                    ((self.screenWidth / 2) - 100, (self.screenHeight / 2) - 10))

        pygame.display.flip()
        
    def showWinner(self, winner):
        self.winner = winner
        self.drawStage()
        
        while True:
            for event in pygame.event.get():
                keystate = pygame.key.get_pressed()
                if keystate[pygame.K_RETURN]:
                    return
        
    def act(self, player, action, display=False):
        if self.gameOver == True:
            print 'This game is already over. Call reset() to restart the game.'
            return self.state.copy(), True, None

        x = action
        if self.state[0, x] != -1:
            print 'The action %s is not allowed.' % action
            print 'state: %s' % self.state
            return self.state.copy(), None, None
        
        for i in range(self.height-1, -1, -1):
            if self.state[i, x] == -1:
                self.state[i, x] = player
                break
        
        gameOver, winner = self.checkGameOver()

        if gameOver:
            self.gameOver = gameOver
            """
            if winner == -1:
                print 'Game draw'
            else:
                print 'Game over. winner : %s' % winner
            """
        
        if self.display and display:
            self.drawStage()
            #time.sleep(0.5)
            
        return self.state.copy(), gameOver, winner

def test1():
    env = ConnectFourEnv(display=True)
    state, gameOver, winner = env.act(1, 0)
    time.sleep(1)
    state, gameOver, winner = env.act(2, 0)
    time.sleep(1)
    state, gameOver, winner = env.act(1, 1)
    time.sleep(1)
    state, gameOver, winner = env.act(2, 0)
    time.sleep(1)
    state, gameOver, winner = env.act(1, 2)
    time.sleep(1)
    state, gameOver, winner = env.act(2, 0)
    time.sleep(1)
    state, gameOver, winner = env.act(1, 3)
    time.sleep(1)
    state, gameOver, winner = env.act(2, 0)
    time.sleep(5)

def test2():
    env = ConnectFourEnv(display=True)
    simpleAgent = SimpleAgent(env, 2, 1)
    
    state, gameOver, winner = env.act(1, 0)
    state, gameOver, winner = env.act(2, 6)
    time.sleep(0.5)
    
    state, gameOver, winner = env.act(1, 1)
    state, gameOver, winner = env.act(2, 5)
    time.sleep(0.5)
    
    state, gameOver, winner = env.act(1, 2)
    acttion = simpleAgent.getAction(env.state)
    state, gameOver, winner = env.act(2, acttion)
    time.sleep(5)

def test3():
    env = ConnectFourEnv(display=True)
    simpleAgent = SimpleAgent(env, 2, 1)
    
    state, gameOver, winner = env.act(1, 0)
    state, gameOver, winner = env.act(2, 6)
    time.sleep(0.5)
    
    state, gameOver, winner = env.act(1, 1)
    state, gameOver, winner = env.act(2, 5)
    time.sleep(0.5)
    
    state, gameOver, winner = env.act(1, 3)
    acttion = simpleAgent.getAction(env.state)
    state, gameOver, winner = env.act(2, acttion)
    time.sleep(5)

def test4():
    env = ConnectFourEnv(display=True)
    simpleAgent1 = SimpleAgent(env, 1, 2)
    simpleAgent2 = SimpleAgent(env, 2, 1)
    
    state = env.getState()
    while True:
        acttion1 = simpleAgent1.getAction(state)
        state, gameOver, winner = env.act(1, acttion1, True)
        time.sleep(0.3)
        if gameOver:
            break
        acttion2 = simpleAgent2.getAction(state)
        state, gameOver, winner = env.act(2, acttion2, True)
        time.sleep(0.3)
        if gameOver:
            break
    
    if winner == -1:
        print 'Game draw'
    else:
        print 'Player %s won' % winner
    time.sleep(5)
    
if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    test4()
