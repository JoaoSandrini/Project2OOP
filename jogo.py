import pygame
from configJogo import ConfigJogo
from cenaInicial import CenaInicial

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))
    
    def rodar(self):
        cena = CenaInicial(self.tela)
        cena.rodar()
        
        '''
        while True:
            cenaPrincipal = CenaPrincipal(self.tela)
            cenaPrincipal.rodar()

            cenaFinal = CenaWin(self.tela, cenaPrincipal)
            cenaFinal.rodar()
        '''
