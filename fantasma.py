import pygame
import random
from mapa import Mapa
from config_jogo import ConfigJogo
from utils import ler_imagem
import time
from enum import Enum

class Direcao(Enum):
    ESQUERDA = 0
    DIREITA = 1
    BAIXO = 2
    CIMA = 3
class Fantasma:
    def __init__(self, mapa: Mapa, tela: pygame.Surface) -> None:
        self.img_fantasma= ler_imagem('enemies/enemy-fantasma.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        self.vida = ConfigJogo.VIDA_INIMIGO
        self._mapa = mapa
        self._x = ConfigJogo.QUARTEL_X
        self._y = ConfigJogo.QUARTEL_Y
        self._idx_movimento = random.randint(Direcao.ESQUERDA.value, Direcao.CIMA.value)
        self.time_inalvejavel = time.time()
        self.colisao = self.img_fantasma.get_rect(topleft=(self._x, self._y))
        
        self.tela = tela

        self._time_last_move = 0
        
    def desenha(self):
        #superficie_circulo = pygame.Surface((ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_TELA), pygame.SRCALPHA)
        #pygame.draw.circle(superficie_circulo, ConfigJogo.COR_AURA, (self._x + ConfigJogo.TAM_TILE/2, self._y + ConfigJogo.TAM_TILE/2), ConfigJogo.RAIO_AURA)
        #self.tela.blit(superficie_circulo, ConfigJogo.ORIGEM)
        pygame.draw.circle(self.tela, ConfigJogo.COR_AURA, (self._x+ ConfigJogo.TAM_TILE/2, self._y + ConfigJogo.TAM_TILE/2), ConfigJogo.RAIO_AURA, ConfigJogo.ESPESSURA_AURA)
        self.tela.blit(self.img_fantasma, (self._x, self._y))

    def tratamento_eventos(self, bombaVetores, inimigos):
        timeAtt = time.time()
        self.colisao = self.img_fantasma.get_rect(topleft=(self._x, self._y)) #atualiza a colisao
        for bombaVetor in bombaVetores:
            for bomba in bombaVetor:  
                if bomba.explosao: # colisao com a explosao
                    for rect in bomba.explosoes:
                        if rect.colliderect(self.colisao):
                            if timeAtt - self.time_inalvejavel > 5:
                                self.time_inalvejavel = timeAtt
                                self.vida -= 1
                                if self.vida == 0:
                                    inimigos.remove(self)
                                else:
                                    self.setX(ConfigJogo.QUARTEL_X)
                                    self.setY(ConfigJogo.QUARTEL_Y)



        if time.time() - self._time_last_move > ConfigJogo.CD_FANTASMA:

            new_x = self._x
            new_y = self._y

            if self._idx_movimento == Direcao.ESQUERDA.value:
                new_x -= ConfigJogo.VELOCIDADE_FANTASMA
            elif self._idx_movimento == Direcao.DIREITA.value:
                new_x += ConfigJogo.VELOCIDADE_FANTASMA
            elif self._idx_movimento == Direcao.BAIXO.value:
                new_y += ConfigJogo.VELOCIDADE_FANTASMA
            elif self._idx_movimento == Direcao.CIMA.value:
                new_y -= ConfigJogo.VELOCIDADE_FANTASMA

            if not self._mapa.is_fixed_wall(new_x, new_y):
                self._x = new_x
                self._y = new_y
                self._time_last_move = time.time()
            else:
                self._idx_movimento = random.randint(0, 3)

    def getX(self):
        return self._x
    
    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y
    
    def setY(self, y):
        self._y = y