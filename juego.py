import pygame
pygame.init()
Ventana = pygame.display.set_mode((640,480))
ball = pygame.image.load("balón.png").convert_alpha()
ballrect = ball.get_rect()
speed = [4,4]
ballrect = ball.get_rect()
ballrect.move_ip(0,0)

bate = pygame.image.load("bate.png")
baterect = bate.get_rect()
baterect.move_ip(240,450)
pygame.display.set_caption("Mi primera ventana")
Juego = True
while Juego:

 ballrect = ballrect.move(speed)
 if ballrect.left < 0 or ballrect.right > Ventana.get_width():
        speed[0] = -speed[0]
            
 if ballrect.top < 0 or ballrect.bottom > Ventana.get_height():
        speed[1] = -speed[1]

 keys = pygame.key.get_pressed()
 if keys[pygame.K_LEFT]:
        baterect = baterect.move(-3,0)
 if keys[pygame.K_RIGHT]:
        baterect = baterect.move(3,0)
 
 if ballrect.colliderect(baterect) and speed[1] > 0:
    speed[1] = -speed[1]     
    ballrect.bottom = baterect.top 
   
 for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
     Juego = False
 
 Ventana.fill((255,255,255))
 Ventana.blit(ball, ballrect)
 Ventana.blit(bate, baterect)
 pygame.display.flip()          
 pygame.time.Clock().tick(60)

pygame.quit()
