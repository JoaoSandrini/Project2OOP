import pygame
from config_jogo import ConfigJogo
from cena_inicial import CenaInicial
from cena_principal import CenaPrincipal

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA))
        pygame.display.set_caption('Bomberman')
        icone = pygame.image.load('items/bomba.png')  # Replace with the path to your icon image
        pygame.display.set_icon(icone)

        self.bombas = [[],[]]
        self.projeteis = []

    def rodar(self):
        cena = CenaInicial(self.tela)
        cena.rodar()
        
        while True:
            cena_principal = CenaPrincipal(self.tela, cena.num_jogadores, self.bombas, self.projeteis)
            cena_principal.rodar()
            self.projeteis = cena_principal.alien.projeteis
"""
            for bomba in cena_principal.p1.bombas:
                if len(self.bombas[0]) < 4:  # Limit to 4 bombs per player
                    self.bombas[0].append(bomba)

            if cena_principal.p2:
                for bomba in cena_principal.p2.bombas:
                    if len(self.bombas[1]) < 4:
                        self.bombas[1].append(bomba)
                



            #cenaFinal = CenaWin(self.tela, cenaPrincipal)
            #cenaFinal.rodar()
"""
