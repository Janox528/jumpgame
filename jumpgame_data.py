import objects_jumpgame
import pygame

player = objects_jumpgame.Player(500,0,100,25,60)

#draw constants
#floor = pygame.Rect(0,500,800,100)
#cloudimg = pygame.image.load('cloud.png')

game = objects_jumpgame.Game(player,[])


