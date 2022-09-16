import random
import pygame

#Faccio codesta prova
#Riproviamo a moddare


RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

#Change aspect of snake and window
SQUARE_SIZE=50
WINDOW_X=800
WINDOW_Y=800

#Lower value, easier game
DIFFICULTY=10

class SnakeGame:
    snake_body = []
    body_len = 0
    score = 0
    curr_head = 0
    do_mov = False
    direction = 0
    apple_x = 0
    apple_y = 0

    #Training variables
    eaten = False
    reward  = 0
    done = False


    #Reset function
    def res_init(self):
        #global snake_body,body_len,score,curr_head,eaten,do_mov,direction
        #global apple_x,apple_y,reward
        dis.fill(WHITE)
        self.snake_body = [(SQUARE_SIZE,0), (0,0)]
        self.body_len = len(self.snake_body)
        self.score = self.body_len
        self.curr_head = 0
        self.eaten = True
        #reward doesn't have to be reset to 0
        self.do_mov = True
        #0 RIGHT
        #1 DOWN
        #2 LEFT
        #3 UP
        self.direction = 0
        self.create_food()

    #Function to randomly create food
    def create_food(self):
        x = random.randrange(0,WINDOW_X/SQUARE_SIZE-1)*SQUARE_SIZE
        y = random.randrange(0,WINDOW_X/SQUARE_SIZE-1)*SQUARE_SIZE
        f=1
        while f!=0:
            try:
                f=self.snake_body.index((x,y))
                x = random.randrange(0,WINDOW_X/SQUARE_SIZE-1)*SQUARE_SIZE
                y = random.randrange(0,WINDOW_X/SQUARE_SIZE-1)*SQUARE_SIZE
            except ValueError:
                f=0    
        self.eaten=False
        self.apple_x = x
        self.apple_y = y

    #Function for growing
    def grow(self):
        self.snake_body.insert(0,(self.apple_x,self.apple_y))
        self.body_len = len(self.snake_body)
        self.score = self.body_len

    #Single loop iteration
    #action param used only if controlled by computer, not keyboard
    def play_step(self, action):
        #Clear display
        dis.fill(WHITE)

        #Setup flag
        self.do_mov = True

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    if self.direction==1 or self.direction==3:
                        self.direction = 0
                elif event.key==pygame.K_LEFT:
                    if self.direction==1 or self.direction==3:
                        self.direction = 2
                elif event.key==pygame.K_UP:
                    if self.direction==0 or self.direction==2:
                        self.direction = 3
                elif event.key==pygame.K_DOWN:
                    if self.direction==0 or self.direction==2:
                        self.direction = 1
                break

        #Check if head appears twice: biting itself
        try :
            f = self.snake_body.index(self.snake_body[0], 1, self.body_len)
            if f!=0:
                self.reward = self.reward - 10
                aux = self.score
                self.res_init()
                return aux
        except ValueError:
            pass

        #Checks if apple eaten
        if (self.snake_body[0][0]==self.apple_x-SQUARE_SIZE and self.snake_body[0][1]==self.apple_y and self.direction==0) or (self.snake_body[0][1]==self.apple_y-SQUARE_SIZE and self.snake_body[0][0]==self.apple_x and  self.direction==1) or (self.snake_body[0][0]==self.apple_x+SQUARE_SIZE and self.snake_body[0][1]==self.apple_y and  self.direction==2) or (self.snake_body[0][1]==self.apple_y+SQUARE_SIZE and self.snake_body[0][0]==self.apple_x and  self.direction==3):
            self.eaten = True
            self.reward = self.reward + 10
            self.grow()
            self.create_food()
            self.do_mov = False


        if self.do_mov:
            #Performs movement
            if self.direction==0:
                if self.snake_body[self.curr_head][0]==(WINDOW_X/SQUARE_SIZE-1)*SQUARE_SIZE:
                    self.reward = self.reward - 10
                    aux = self.score
                    self.res_init()
                    return aux
                self.snake_body.pop()
                self.snake_body.insert(0, (self.snake_body[0][0]+SQUARE_SIZE,self.snake_body[0][1]))
            elif self.direction==1:
                if self.snake_body[self.curr_head][1]==(WINDOW_Y/SQUARE_SIZE-1)*SQUARE_SIZE:
                    self.reward = self.reward - 10
                    aux = self.score
                    self.res_init()
                    return aux
                self.snake_body.pop()
                self.snake_body.insert(0, (self.snake_body[0][0],self.snake_body[0][1]+SQUARE_SIZE))
            elif self.direction==2:
                if self.snake_body[self.curr_head][0]==0:    
                    self.reward = self.reward - 10
                    aux = self.score
                    self.res_init()
                    return aux
                self.snake_body.pop()
                self.snake_body.insert(0, (self.snake_body[0][0]-SQUARE_SIZE,self.snake_body[0][1]))
            elif self.direction==3:
                if self.snake_body[self.curr_head][1]==0:    
                    self.reward = self.reward - 10
                    aux = self.score
                    self.res_init()
                    return aux
                self.snake_body.pop()
                self.snake_body.insert(0, (self.snake_body[0][0],self.snake_body[0][1]-SQUARE_SIZE))


        #Draws every square of the snake
        i=0
        for (a,b) in self.snake_body:
            pygame.draw.rect(dis,GREEN,[self.snake_body[i][0],self.snake_body[i][1],SQUARE_SIZE,SQUARE_SIZE])
            i=i+1

        #Draws apple
        pygame.draw.rect(dis,RED,[self.apple_x,self.apple_y,SQUARE_SIZE,SQUARE_SIZE])

        #Prints score
        score_str = "Current score: %d" %self.score
        text_surface = my_font.render(score_str, False, BLUE)
        dis.blit(text_surface,(0,0))

        pygame.display.update()
        clock.tick(DIFFICULTY)

        print("Reward is: ", self.reward)

        return self.reward ,self.done, self.score


#Init window
pygame.init()
dis=pygame.display.set_mode((WINDOW_X,WINDOW_Y))

#Init fonts
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock=pygame.time.Clock()

my_snake = SnakeGame()

my_snake.res_init()
while True:
    caught = my_snake.play_step(0)

pygame.quit()
quit()
