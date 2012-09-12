"""This is a test pygame application.
Python Version: 2.7.3
Author: Matthew McMullan

Description: This template was made using best practices from...
http://www.python.org/dev/peps/pep-0008/
http://www.python.org/dev/peps/pep-0257/

"""
#------------------------------------------------------------------------------
# Standard Library Imports ------------------------------------------
import sys

# 3'rd Party Imports ------------------------------------------------
import pygame

# Local Application/Library Specific Imports ----------------------------
import terrain
#------------------------------------------------------------------------------
# Global Variables for Export ---------------------------------------

# Global Variables for use Inside the Module ------------------------

parent_folder = '../assets/terrain'
background = 'test.txt'
overlays = ['overlay.txt']
inifile = 'terrainObjects.ini'

#------------------------------------------------------------------------------

pygame.init()
screen = pygame.display.set_mode((800,600), pygame.DOUBLEBUF+pygame.HWSURFACE)
lettermap = terrain.createLetterMap(parent_folder,inifile)
tilemap = terrain.createTiledMap(lettermap, parent_folder,background,overlays)
try:
    while True:
        # process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    print "reloading"
                    lettermap = terrain.createLetterMap(parent_folder,inifile)
                    tilemap = terrain.createTiledMap(lettermap, parent_folder,background,overlays)
        # draw
        screen.blit(tilemap.surface,(0,0))
        pygame.display.flip()
except SystemExit:
    pygame.quit()
except:
    pygame.quit()
    raise
