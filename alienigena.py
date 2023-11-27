import pygame
import random
from mapa import Mapa
from config_jogo import ConfigJogo
from utils import ler_imagem
import time
from enum import Enum
from projetil import Projetil

class Direcao(Enum):
    ESQUERDA = 0
    DIREITA = 1
    BAIXO = 2
    CIMA = 3
class Alienigena:
    def __init__(self, mapa: Mapa, tela: pygame.Surface) -> None:
        self.img_alien= ler_imagem('enemies/enemy-alien.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.time_inalvejavel = 6
        self.vida = ConfigJogo.VIDA_INIMIGO
        self._mapa = mapa
        self._x = ConfigJogo.QUARTEL_X
        self._y = ConfigJogo.QUARTEL_Y
        self._idx_movimento = random.randint(Direcao.ESQUERDA.value, Direcao.CIMA.value)
        
        self.colisao = pygame.Rect(self._x, self._y, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
        self.tela = tela

        self._time_last_move = 0
        self._time_last_shot = 0

        self.projeteis = []
        
    def desenha(self):
        self.tela.blit(self.img_alien, (self._x, self._y))

    def tratamento_eventos(self, bombaVetores, inimigos):
        self.colisao = pygame.Rect(self._x, self._y, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
        pygame.draw.rect(self.tela, (255,255,0), self.colisao)

        bombaColisao = False
        timeAtt = time.time()

        for bombaVetor in bombaVetores:
            for bomba in bombaVetor:  
                if bomba.explosao: # colisao com a explosao
                    for rect in bomba.explosoes:
                        pygame.draw.rect(self.tela, (255,0,0), rect)
                        if rect.colliderect(self.colisao):
                            if timeAtt - self.time_inalvejavel > 5:
                                self.time_inalvejavel = timeAtt
                                self.vida -= 1
                                if self.vida == 0:
                                    inimigos.remove(self)
                                else:
                                    self.setX(ConfigJogo.QUARTEL_X)
                                    self.setY(ConfigJogo.QUARTEL_Y)

        if time.time() - self._time_last_shot >= ConfigJogo.CD_SHOT_ALIEN:
            self.atira()
            self._time_last_shot = time.time()

        if time.time() - self._time_last_move > ConfigJogo.CD_ALIEN:
            new_x = self._x
            new_y = self._y

            for bombaVetor in bombaVetores:
                for bomba in bombaVetor:
                    if bomba.colisao.colliderect(self.colisao):
                        bombaColisao = True

            if self._idx_movimento == Direcao.ESQUERDA.value:
                new_x -= ConfigJogo.VELOCIDADE_ALIEN
            elif self._idx_movimento == Direcao.DIREITA.value:
                new_x += ConfigJogo.VELOCIDADE_ALIEN
            elif self._idx_movimento == Direcao.BAIXO.value:
                new_y += ConfigJogo.VELOCIDADE_ALIEN
            elif self._idx_movimento == Direcao.CIMA.value:
                new_y -= ConfigJogo.VELOCIDADE_ALIEN

            if not self._mapa.is_any_wall(new_x, new_y) and not bombaColisao:
                self._x = new_x
                self._y = new_y
                self._time_last_move = time.time()
            else:
                self._idx_movimento = random.randint(0, 3)

        
    def atira(self):
            projetil = Projetil(self._x, self._y, self._mapa)
            self.projeteis.append(projetil)
