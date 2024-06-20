import random 
import pygame # type: ignore
from sys import exit
#going through documentation helps a lot
pygame.init()
screen = pygame.display.set_mode((572,432)) #display surface (x,y)
pygame.display.set_caption("SpaceInvaders") #you could also change the icon
clock = pygame.time.Clock() #introduces time to the object

#importing image
bg_surface = pygame.image.load('R.jpeg').convert_alpha() #this is a new surface
bg_rect = bg_surface.get_rect(center = (286,216))


steve_surf = pygame.image.load('player1.png').convert_alpha() #generally good practice to add alpha - turns the object something that pygame can work with
#creating a rectangle
steve_rect = steve_surf.get_rect(center = (270,400))#steve_rectangle = pygame.Rect() #left,top,width,height

steve_pos = 286
bullet_surf = pygame.image.load('B.png').convert_alpha()
bullet_rect = bullet_surf.get_rect()

barriers = []
barriers_rect = []
barx = []
bary = []
damage = []
b_num = 4

for i in range(b_num):
    barriers.append(pygame.image.load('barrier.png').convert_alpha())
    barx.append(150+110*i)
    bary.append(350)
    damage.append(0)
    barriers_rect.append(barriers[i].get_rect(center = (barx[i],bary[i])))

barriers2 = []
barriers2_rect = []
bar2x = []
bar2y = []

for i in range(b_num):
    barriers2.append(pygame.image.load('barrier2.png').convert_alpha())
    bar2x.append(150+110*i)
    bar2y.append(350)
    barriers2_rect.append(barriers2[i].get_rect(center = (barx[i],bary[i])))

#creating multiple enemy surfaces/objects
enemy = []
e_rect = []
enx = []
eny = []
alive = []
shoot_times = []
active = []

num = 15
j=0


for i in range(num):
     enemy.append(pygame.image.load('enemy.png').convert_alpha())
     alive.append(1)
     active.append(0)
     shoot_times.append(120*random.randrange(1,5))
     if i%5 == 0:
          j+=1
     enx.append(120+80*(i%5))
     eny.append(50*j)
     e_rect.append(enemy[i].get_rect(center = (enx[i],eny[i])))

bullet = []
benx = []
beny = []
b_rect = []
j2 = 0
for i in range(num):
     bullet.append(pygame.image.load('B.png').convert_alpha())
     if i%5 == 0:
          j2+=1
     benx.append(120+80*(i%5)+9)
     beny.append(50*j2)
     b_rect.append(bullet[i].get_rect(center = (benx[i],beny[i])))

trigger = 0
p_alive = 1
collision = 0
shoots = []
counter = 0
fire = []
fire_rect = []
score = 0
ml = 1
mr = 0
for i in range(num):
     shoots.append(1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #this is a constant
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN: #motion of player
            if event.key == pygame.K_RIGHT:
                steve_rect.x +=10
            if event.key == pygame.K_LEFT: #previous frames are getting overlapped
                steve_rect.x -=10
            if event.key == pygame.K_SPACE: #create a bullet
                trigger = 1
                fire.append(pygame.image.load('B.png').convert_alpha())
                fire_rect.append(fire[counter].get_rect(center = (steve_rect.x,steve_rect.y)))
                #fire_rect.x = steve_rect.x
                #fire_rect.y = steve_rect.y 
                counter += 1
    for i in range(num):
         if shoot_times[i] == 0:
              shoots[i] = 0
              shoot_times[i] = 120*random.randrange(1,5)
              b_rect[i].y = e_rect[i].y

    screen.blit(bg_surface,bg_rect)
    for i in range(num):
        if ml:
            e_rect[i].x -= 1
        if mr:
            e_rect[i].x += 1 
        if alive[i]: # and alive[i+5]
            if i<5:
                if alive[i+5] == 0:
                    if shoots[i] == 0 and collision == 0:
                        b_rect[i].x = e_rect[i].x
                        screen.blit(bullet[i],b_rect[i])
                        active[i] = 1
                        b_rect[i].y +=7
            if (i>=5 and i<10):
                if alive[i+5] == 0:
                    if shoots[i] == 0 and collision == 0:
                        b_rect[i].x = e_rect[i].x
                        screen.blit(bullet[i],(b_rect[i].x,b_rect[i].y))
                        active[i] = 1
                        b_rect[i].y +=7
            if i>=10:
                if shoots[i] == 0 and collision == 0:
                    b_rect[i].x = e_rect[i].x
                    screen.blit(bullet[i],(b_rect[i].x,b_rect[i].y))
                    active[i] = 1
                    b_rect[i].y +=7
            if e_rect[i].left<0:
                ml = 0 
                mr = 1
            if e_rect[i].right>572: # the right boundary is not acccurate
                ml = 1
                mr = 0
            screen.blit(enemy[i],e_rect[i])
        if alive[i] == 0 and active [i] == 1:
            b_rect[i].x = e_rect[i].x
            screen.blit(bullet[i],(b_rect[i].x,b_rect[i].y))
            b_rect[i].y +=7 
    
    for i in range(counter):
        if trigger == 1:
            screen.blit(fire[i],fire_rect[i])
            fire_rect[i].y -= 4
    #if trigger == 1:
     #   screen.blit(bullet_surf,bullet_rect)
      #  bullet_rect.y -= 2.5

    for i in range(num):
         for j in range(counter):
            if e_rect[i].colliderect(fire_rect[j]):
                alive[i] = 0
                score += 5
                e_rect[i].center = (0,0)
                fire_rect[j].x +=1000
              
    for i in range(num):
         shoot_times[i] -= 1
    for i in range(num):
         if steve_rect.colliderect(b_rect[i]):
            collision = 1
            p_alive = 0
    
    #pygame.draw.line('Gold',0,0,mouse.pos,10) #- line that foll0ws a mouse
    if p_alive:
        screen.blit(steve_surf,steve_rect)

    for i in range(b_num):
        if damage[i] == 0:
            screen.blit(barriers[i],(barriers_rect[i].x,barriers_rect[i].y))
        if damage[i] == 1:
            screen.blit(barriers2[i],(barriers2_rect[i].x,barriers2_rect[i].y))
    h = 0
    for i in range(b_num):
        for j in range(num):
            if damage[i] == 0:
                if barriers_rect[i].colliderect(b_rect[j]):
                    b_rect[j].x += 1000
                    barriers_rect[i].x += 20
                    print(i)
                    damage[i] = 1
                    h = 1
            if damage[i] == 1 and h == 0:
                if barriers2_rect[i].colliderect(b_rect[j]):
                    b_rect[j].x += 1000
                    damage[i] = 2
            h = 0       
                    
    for i in range(b_num):
        for j in range(counter):
            if damage[i] == 0:
                if barriers_rect[i].colliderect(fire_rect[j]):
                    fire_rect[j].x += 1000
            if damage[i] == 1:
                if barriers2_rect[i].colliderect(fire_rect[j]):
                    fire_rect[j].x += 1000

    for i in range(num): #this gets rid of heavenly fire but kills bullets once they are back
       if b_rect[i].y>432:
            active[i] = 0

            
    pygame.display.update() #make it the last line
    clock.tick(60) #sets max frame rate



#write comments
#getting rid of rects
#making masks
#make different start pages
#let the target shoot multiple bullets and don't remove the bullet once target gets destroyed
#display scores
#holding key moves it as well, make it so player can't move out of screen
#optimize the code once it is finished
#Add more features as time goes on
#fix some bugs -why does the third one not shoot anymore

