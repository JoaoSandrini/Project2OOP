import pygame
from config_jogo import ConfigJogo
from cena_inicial import CenaInicial
from cena_principal import CenaPrincipal

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))
    
    def rodar(self):
        cena = CenaInicial(self.tela)
        cena.rodar()
        
        while True:
            cena_principal = CenaPrincipal(self.tela, cena.num_jogadores)
            cena_principal.rodar()

            #cenaFinal = CenaWin(self.tela, cenaPrincipal)
            #cenaFinal.rodar()