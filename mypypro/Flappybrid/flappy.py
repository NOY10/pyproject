import pygame 
import neat
import time
import os
import random
pygame.font.init()
DIR = os.path.dirname(os.path.realpath(__file__))
IMGS_DIR = os.path.join(DIR, "imgs")
WIN_WIDTH=500
WIN_HEIGHT=700
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"bird1.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"bird2.png"))),
 pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"bird3.png")))]
PIPE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"pipe.png")))
BG_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"bg.png")))
BASE_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join(IMGS_DIR,"base.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

class Bird:
    IMGS=BIRD_IMGS
    MAX_ROTATION=25
    ROT_VAL=20
    ANIMATION_TIME=5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    def jump(self):
        """
        make the bird jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    def move(self):
        """
        make the bird move
        :return: None
        """
        self.tick_count += 1

        # for downward acceleration
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  # calculate displacement

        # terminal velocity
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    def draw(self, win):
        """
        draw the bird
        :param win: pygame window or surface
        :return: None
        """
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # tilt the bird
        rotated_image=pygame.transform.rotate(self.img,self.tilt)
        new_rect=rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        win.blit(rotated_image,new_rect.topleft)
    def get_mask(self):
        """
        gets the mask for the current image of the bird
        :return: None
        """
        return pygame.mask.from_surface(self.img)
class Pipe:
    GAP=200
    VEL=5
    def __init__(self,x):
        self.x=x
        self.height=0
        self.gap=100
        self.top=0
        self.buttom=0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False

        self.set_height()
    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    def move(self):
        """
        move pipe based on vel
        :return: None
        """
        self.x -= self.VEL
    def draw(self, win):
        """
        draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return: None
        """
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    def collide(self, bird):
        """
        returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False
class Base:
    """
    Represnts the moving floor of the game
    """
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self, win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
    






def draw_window(win,bird,pipes, base, score):
    win.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    bird.draw(win)
    pygame.display.update()

def main():
    bird=Bird(230,250)
    base=Base(600)
    pipes=[Pipe(570)]
    run=True
    score=0
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        base.move()
        rem = []
        add_pipe = False
        for pipe in pipes:
            # check for collision
            # for bird in birds:
            #     if pipe.collide(bird, win):
            #         ge[birds.index(bird)].fitness -= 1
            #         nets.pop(birds.index(bird))
            #         ge.pop(birds.index(bird))
            #         birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            # can add this line to give more reward for passing through a pipe (not required)
            # for genome in ge:
            #     genome.fitness += 5
            pipes.append(Pipe(WIN_WIDTH))
        for r in rem:
            pipes.remove(r)

        
        draw_window(win,bird,pipes,base,score)
    pygame.quit()
    quit()
   
main()   



