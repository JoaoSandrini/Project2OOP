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
        self.time_inalvejavel = 0

    def tratamento_eventos(self, bombaVetores):
        timeAtt = time.time()
        self.colisao = self.img_quartel.get_rect(topleft=(self._x, self._y)) #atualiza a colisao
        for bombaVetor in bombaVetores:
            for bomba in bombaVetor:  
                if bomba.explosao: # colisao com a explosao
                    for rect in bomba.explosoes:
                        if rect.colliderect(self.colisao):
                            if timeAtt - self.time_inalvejavel > 0.5:
                                self.time_inalvejavel = timeAtt
                                self._vida -= 1
                                print(self._vida)
                                if self._vida == 0:
                                    pass


        if  time.time() - self._time_last_spawn > 2:
            rand = random.randint(0, 1)
            if rand == 0:
                self.inimigos.append(Fantasma(self.mapa, self.tela))
            elif rand == 1:
                self.inimigos.append(Alienigena(self.mapa, self.tela))
            self._time_last_spawn = time.time()

    def desenha(self, bombaVetores):
        self.tela.blit(self.img_quartel, (self._x, self._y))
        for inimigo in self.inimigos:
            if type(inimigo) == Fantasma:
                inimigo.desenha()
                inimigo.tratamento_eventos(bombaVetores, self.inimigos)
            else:
                for projetil in inimigo.projeteis:
                    projetil.desenha(self.tela)
                    projetil.tratamento_eventos()
                    if projetil.colidido:
                        inimigo.projeteis.remove(projetil)
                inimigo.desenha()
                inimigo.tratamento_eventos(bombaVetores, self.inimigos)

    def getInimigos(self):
        return self.inimigos