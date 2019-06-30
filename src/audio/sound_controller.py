'''
    Channel Info:
        -1: Music
        -2: Player 1 attack
        -3: Player 2 attack
        -4: Player 1 take damage
        -5: Player 2 take damage

        -10: Enemy attack
        -11: Enemy take damage
        -12: Enemy death
        -13: Enemy misc
'''

import pygame;

class Sound_Controller:
    def __init__(self):
        # Mixer initialization
        pygame.mixer.pre_init(44100, 16, 2, 4096);
        pygame.init();
        pygame.mixer.set_num_channels(20);


    def play_music(self, music_file):
        pygame.mixer.music.load(music_file);
        pygame.mixer.music.play(-1); # -1 loop infinite times


    def pause_music(self):
        pygame.mixer.music.pause();


    def resume_music(self):
        pygame.mixer.music.unpause();


    def stop_music(self):
        pygame.mixer.music.stop();


    def play_sfx(self, channel, sfx_file):
        # For some reason the channel number keeps getting reduced to 10
        # so it needs to be reset when the channel number is over 10
        if(channel > 10):
            pygame.mixer.set_num_channels(20);
        pygame.mixer.Channel(channel).play(pygame.mixer.Sound(sfx_file));

