import pygame
from config_jogo import ConfigJogo
from cena_inicial import CenaInicial
from cena_principal import CenaPrincipal
from bomba import Bomba
from time import time

class Jogo:
    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))
        self.bombas = [[],[]]
        self.projeteis = []

    def rodar(self):
        cena = CenaInicial(self.tela)
        cena.rodar()
        
        while True:
            cena_principal = CenaPrincipal(self.tela, cena.num_jogadores)
            cena_principal.rodar()

            self.bombas[0] = cena_principal.p1.bombas
            self.bombas[1] = cena_principal.p2.bombas
            self.projeteis = cena_principal.alien.projeteis
""" 
            
            #cenaFinal = CenaWin(self.tela, cenaPrincipal)
            #cenaFinal.rodar()
"""
