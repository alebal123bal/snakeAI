from enum import Enum
import random
import pygame
import numpy

RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
WHITE=(255,255,255)

#Change aspect of snake and window
SQUARE_SIZE=50
WINDOW_X=800
WINDOW_Y=800

#Lower value, easier game
DIFFICULTY = 1

class direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

class status():
    direction_right = 0
    direction_down = 0
    direction_left = 0
    direction_up = 0

    food_direction_right = 0
    food_direction_down = 0
    food_direction_left = 0
    food_direction_up = 0

    danger_ahead_sq = 0
    danger_right = 0
    danger_left = 0

class SnakeGame:
    #Snake variables
    snake_body = []
    snake_body_len = 0
    snake_curr_head = 0   #Array index of snake's head
    snake_do_mov = False  #If snake has eaten apple, it doesn't need to move: head grows towards eaten apple
    snake_direction = direction.RIGHT

    #Game variables
    score = 0
    controller = 1  #0: Keyboard controlled, 1: Automatic controlled. Never updated after init
    game_status = status()

    #Apple variables
    apple_eaten = False
    apple_x = 0
    apple_y = 0

    #Training variables
    done = False

    #Reset function
    def res_init(self):
        dis.fill(WHITE)
        self.snake_body = [(SQUARE_SIZE,0), (0,0)]
        self.snake_body_len = len(self.snake_body)
        self.score = self.snake_body_len
        self.snake_curr_head = 0
        self.apple_eaten = True
        self.snake_do_mov = True
        self.snake_direction = direction.RIGHT
        self.create_food()

    #Evaluate status function
    def status_eval(self):
        #Reset status
        self.game_status = status()

        #Get current head
        (x, y) = self.snake_body[self.snake_curr_head]
        curr_head = (x, y)

        #Calculate the 3 squares close to the head
        if self.snake_direction==direction.RIGHT:
            ahead_sq = (x+SQUARE_SIZE, y)
            right_sq = (x, y+SQUARE_SIZE)
            left_sq = (x, y-SQUARE_SIZE)
        elif self.snake_direction==direction.DOWN:
            ahead_sq = (x, y+SQUARE_SIZE)
            right_sq = (x-SQUARE_SIZE, y)
            left_sq = (x+SQUARE_SIZE, y)
        elif self.snake_direction==direction.LEFT:
            ahead_sq = (x-SQUARE_SIZE, y)
            right_sq = (x, y-SQUARE_SIZE)
            left_sq = (x, y+SQUARE_SIZE)
        elif self.snake_direction==direction.UP:
            ahead_sq = (x, y-SQUARE_SIZE)
            right_sq = (x+SQUARE_SIZE, y)
            left_sq = (x-SQUARE_SIZE, y)

        #Check if danger is wall
        if ahead_sq[0] == -SQUARE_SIZE or ahead_sq[1] == -SQUARE_SIZE or ahead_sq[0] == WINDOW_X or ahead_sq[1] == WINDOW_Y:
            self.game_status.danger_ahead_sq = 1

        if right_sq[0] == -SQUARE_SIZE or right_sq[1] == -SQUARE_SIZE or right_sq[0] == WINDOW_X or right_sq[1] == WINDOW_Y:
            self.game_status.danger_right = 1
            
        if left_sq[0] == -SQUARE_SIZE or left_sq[1] == -SQUARE_SIZE or left_sq[0] == WINDOW_X or left_sq[1] == WINDOW_Y:
            self.game_status.danger_left = 1
            
        #Check if danger is itself
        try:
            self.snake_body.index(ahead_sq, 1, self.snake_body_len)
            self.game_status.danger_ahead_sq = 1
        except ValueError:
            pass
        try:
            self.snake_body.index(right_sq, 1, self.snake_body_len)
            self.game_status.danger_right = 1
        except ValueError:
            pass
        try:
            self.snake_body.index(left_sq, 1, self.snake_body_len)
            self.game_status.danger_left = 1
        except ValueError:
            pass

        if self.snake_direction == direction.RIGHT:   
            self.game_status.direction_right = 1
        elif self.snake_direction == direction.DOWN:   
            self.game_status.direction_down = 1
        elif self.snake_direction == direction.LEFT:   
            self.game_status.direction_left = 1
        elif self.snake_direction == direction.UP:   
            self.game_status.direction_up = 1
        
        if self.apple_x > curr_head[0]:
            self.game_status.food_direction_right = 1
        if self.apple_x < curr_head[0]:
            self.game_status.food_direction_left = 1
        if self.apple_y > curr_head[1]:
            self.game_status.food_direction_down = 1
        if self.apple_y < curr_head[1]:
            self.game_status.food_direction_up = 1

        return [self.game_status.direction_right,
        self.game_status.direction_down,
        self.game_status.direction_left, 
        self.game_status.direction_up, 
        self.game_status.food_direction_right, 
        self.game_status.food_direction_down, 
        self.game_status.food_direction_left, 
        self.game_status.food_direction_up, 
        self.game_status.danger_ahead_sq, 
        self.game_status.danger_left, 
        self.game_status.danger_right]


    #Function to randomly create food
    def create_food(self):
        x = random.randrange(0,int(WINDOW_X/SQUARE_SIZE)-1)*SQUARE_SIZE
        y = random.randrange(0,int(WINDOW_X/SQUARE_SIZE)-1)*SQUARE_SIZE
        f=1
        while f!=0:
            try:
                f=self.snake_body.index((x,y))
                x = random.randrange(0,int(WINDOW_X/SQUARE_SIZE-1))*SQUARE_SIZE
                y = random.randrange(0,int(WINDOW_X/SQUARE_SIZE-1))*SQUARE_SIZE
            except ValueError:
                f=0    
        self.apple_eaten = False
        self.apple_x = x
        self.apple_y = y

    #Function for growing
    def grow(self):
        self.snake_body.insert(0,(self.apple_x,self.apple_y))   #Head grows towards eaten apple
        self.snake_body_len = len(self.snake_body)
        self.score = self.snake_body_len

    #Single loop iteration
    def play_step(self, action):
        #Clear display
        dis.fill(WHITE)

        #Setup flag
        self.snake_do_mov = True

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if self.controller == 0:
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        if self.snake_direction==direction.DOWN or self.snake_direction==direction.UP:
                            self.snake_direction = direction.RIGHT
                    elif event.key==pygame.K_LEFT:
                        if self.snake_direction==direction.DOWN or self.snake_direction==direction.UP:
                            self.snake_direction = direction.LEFT
                    elif event.key==pygame.K_UP:
                        if self.snake_direction==direction.RIGHT or self.snake_direction==direction.LEFT:
                            self.snake_direction = direction.UP
                    elif event.key==pygame.K_DOWN:
                        if self.snake_direction==direction.RIGHT or self.snake_direction==direction.LEFT:
                            self.snake_direction = direction.DOWN
                    break
            elif self.controller == 1:
                if action[0] == 1:
                    self.snake_direction = direction.RIGHT
                elif action[1] == 1:
                    self.snake_direction = direction.DOWN
                elif action[2] == 1:
                    self.snake_direction = direction.LEFT
                elif action[3] == 1:
                    self.snake_direction = direction.UP


        #Check if head appears twice: biting itself
        try :
            f = self.snake_body.index(self.snake_body[0], 1, self.snake_body_len)
            if f!=0:
                aux = self.score
                self.res_init()
                return aux
        except ValueError:
            pass

        #Checks if apple eaten
        if (self.snake_body[0][0]==self.apple_x-SQUARE_SIZE and self.snake_body[0][1]==self.apple_y and self.snake_direction==direction.RIGHT) or (self.snake_body[0][1]==self.apple_y-SQUARE_SIZE and self.snake_body[0][0]==self.apple_x and  self.snake_direction==direction.DOWN) or (self.snake_body[0][0]==self.apple_x+SQUARE_SIZE and self.snake_body[0][1]==self.apple_y and  self.snake_direction==direction.LEFT) or (self.snake_body[0][1]==self.apple_y+SQUARE_SIZE and self.snake_body[0][0]==self.apple_x and  self.snake_direction==direction.UP):
            self.apple_eaten = True
            self.grow()
            self.create_food()
            self.snake_do_mov = False

        #Performs movement
        if self.snake_do_mov:
            #Check if wall hit; if not, pop tail and push head
            if self.snake_direction==direction.RIGHT:
                if self.snake_body[self.snake_curr_head][0]==(WINDOW_X/SQUARE_SIZE-1)*SQUARE_SIZE:
                    aux = self.score
                    self.res_init()
                    return aux
                else:    
                    self.snake_body.pop()
                    self.snake_body.insert(0, (self.snake_body[0][0]+SQUARE_SIZE,self.snake_body[0][1]))
            elif self.snake_direction==direction.DOWN:
                if self.snake_body[self.snake_curr_head][1]==(WINDOW_Y/SQUARE_SIZE-1)*SQUARE_SIZE:
                    aux = self.score
                    self.res_init()
                    return aux
                else:
                    self.snake_body.pop()
                    self.snake_body.insert(0, (self.snake_body[0][0],self.snake_body[0][1]+SQUARE_SIZE))
            elif self.snake_direction==direction.LEFT:
                if self.snake_body[self.snake_curr_head][0]==0:
                    aux = self.score
                    self.res_init()
                    return aux
                else:
                    self.snake_body.pop()
                    self.snake_body.insert(0, (self.snake_body[0][0]-SQUARE_SIZE,self.snake_body[0][1]))
            elif self.snake_direction==direction.UP:
                if self.snake_body[self.snake_curr_head][1]==0:
                    aux = self.score
                    self.res_init()
                    return aux
                else:
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

        return self.score


class NeuralNetwork():
    in_neurons_value = [0]*11
    hidden_neurons_value = [0]*4
    hidden_neurons_bias = [0]*4
    out_neurons_value = [0]*4
    out_neurons_bias = [0]*4

    weights_first = [[0]*11]*4      #[4][11]
    weights_second = [[0]*4]*4

    def print_network(self):            
        print("in_neurons_value: ", numpy.array(self.in_neurons_value))
        print("hidden_neurons_value: ", numpy.array(self.hidden_neurons_value))
        print("hidden_neurons_bias: ", numpy.array(self.hidden_neurons_bias))
        print("out_neurons_value: ", numpy.array(self.out_neurons_value))
        print("out_neurons_bias: ", numpy.array(self.out_neurons_bias))
        print("weights_first: \n", numpy.matrix(self.weights_first))
        print("weights_second: \n", numpy.matrix(self.weights_second))



    #Called once at the start
    def randomize(self):
        self.in_neurons_value = numpy.random.randint(0, 2, 11)   #Non serve
        self.hidden_neurons_value = numpy.random.randint(0, 2, 4)
        self.hidden_neurons_bias = numpy.random.randint(0, 101, 4)*0.01
        self.out_neurons_value = numpy.random.randint(0, 2, 4)
        self.out_neurons_bias = numpy.random.randint(0, 101, 4)*0.01
        self.weights_first = numpy.random.randint(-100, 101, size = (4, 11))*0.01
        self.weights_second = numpy.random.randint(-100, 101, size = (4, 4))*0.01

    def feed_forward(self, in_vector):
        #First feed-forward
        curr = 0
        for i in range(0, 4, 1):
            for j in range(0, 11, 1):
                curr = curr + self.weights_first[i][j] * in_vector[j]
            if curr > self.hidden_neurons_bias[i]:
                self.hidden_neurons_value[i] = 1
            else: 
                self.hidden_neurons_value[i] = 0
            curr = 0
        #Second feed-forward
        for i in range(0, 4, 1):
            for j in range(0, 4, 1):
                curr = curr + self.weights_second[i][j] * self.hidden_neurons_value[j]
            if curr > self.out_neurons_bias[i]:
                self.out_neurons_value[i] = 1
            else:
                self.out_neurons_value[i] = 0
            curr = 0
        
        return self.out_neurons_value

#Init window
pygame.init()
dis = pygame.display.set_mode((WINDOW_X,WINDOW_Y))

#Init fonts
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

#Init snake
my_snake = SnakeGame()
my_snake.res_init()

#Init neural network
my_neural_network = NeuralNetwork()
my_neural_network.randomize()

while True:
    curr_status = my_snake.status_eval()
    print(numpy.array(curr_status))
    final_move = my_neural_network.feed_forward(curr_status)
    print(numpy.array(final_move))
    #Update window with moves calculated last loop iteration
    pygame.display.update()
    clock.tick(DIFFICULTY)
    my_snake.play_step(final_move)
