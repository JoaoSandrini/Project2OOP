from utils import ler_imagem
from config_jogo import ConfigJogo
from fantasma import Fantasma
from alienigena import Alienigena
import pygame
import random   
import time
from mapa import Mapa
class Quartel:
    def __init__(self, mapa: Mapa, tela: pygame.Surface):
        self.img_quartel = ler_imagem('enemies/ship.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._x = ConfigJogo.QUARTEL_X
        self._y = ConfigJogo.QUARTEL_Y 
        self._vida = ConfigJogo.VIDA_QUARTEL
        self.inimigos = []
        self._time_last_spawn = 0
        self.mapa = mapa
        self.tela = tela
        
    def tratamento_eventos(self):
        if  time.time() - self._time_last_spawn > 2:
            rand = random.randint(0, 1)
            if rand == 0:
                self.inimigos.append(Fantasma(self.mapa, self.tela))
            elif rand == 1:
                self.inimigos.append(Alienigena(self.mapa, self.tela))
            self._time_last_spawn = time.time()

    def desenha(self):
        self.tela.blit(self.img_quartel, (self._x, self._y))
        for inimigo in self.inimigos:
            if type(inimigo) == Fantasma:
                inimigo.desenha()
                inimigo.tratamento_eventos()
            else:
                for projetil in inimigo.projeteis:
                    projetil.desenha(self.tela)
                    projetil.tratamento_eventos()
                    if projetil.colidido:
                        inimigo.projeteis.remove(projetil)
                inimigo.desenha()
                inimigo.tratamento_eventos()