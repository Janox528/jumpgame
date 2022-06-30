import pygame
import objects_jumpgame
from jumpgame_data import *

 
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pygame-Tutorial: Grundlagen")
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)
 
    clock = pygame.time.Clock()


 
    running = True
    while running:
        clock.tick(30)
 
        screen.fill((121,222,240))

        

        

        game.draw(screen)
        game.nextState()

        #player.draw(screen)




        #execute movement
        #game.player.move()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_w:
                    #jump
                    if game.player.isOnFloor():
                        game.player.jump()
 
        
        #print("y_pos =",game.player.y_pos,game.counter,game.obstacles)
        

        for i in game.items:
            print(game.player.x_pos,game.player.y_pos,i.x_pos,i.y_pos)



        pygame.display.flip()
 
 
if __name__ == '__main__':
    main()




#if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
#if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')
