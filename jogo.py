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
        self.bombas = [[] for _ in range(2)]

    def rodar(self):
        cena = CenaInicial(self.tela)
        cena.rodar()
        
        while True:
            cena_principal = CenaPrincipal(self.tela, cena.num_jogadores)
            cena_principal.rodar()

            self.bombas.append(cena_principal.p1.bombas)
            self.bombas.append(cena_principal.p2.bombas)

            for bomba in cena_principal.p1.bombas:
                if len(self.bombas[0]) < 4:  # Limit to 4 bombs per player
                    self.bombas[0].append(bomba)

            if cena_principal.p2:
                for bomba in cena_principal.p2.bombas:
                    if len(self.bombas[1]) < 4:
                        self.bombas[1].append(bomba)
                



            #cenaFinal = CenaWin(self.tela, cenaPrincipal)
            #cenaFinal.rodar()

