import os.path
import pygame


audio_file = os.path.join(os.path.dirname(__file__), 'backsound.ogg')
pygame.mixer.init()
pygame.mixer.music.load(audio_file)
pygame.mixer.music.play(-1)
while pygame.mixer.music.get_busy() == True:
        continue
