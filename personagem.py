import pygame
import random
from mapa import Mapa
from config_jogo import ConfigJogo
from utils import ler_imagem
import time
from bomba import Bomba
class Personagem:
    def __init__(self, mapa: Mapa, x: int, y: int,  tela: pygame.Surface) -> None:
        self._bomberman_b = ler_imagem('chars/bomberman-white.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._bomberman_l = ler_imagem('chars/bomberman-orange.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._bomberman_p = ler_imagem('chars/bomberman-black.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._bomberman_a = ler_imagem('chars/bomberman-blue.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._sprites = [self._bomberman_a, self._bomberman_b, self._bomberman_l, self._bomberman_p]

        self.pIdx = random.randint(0, 3)
        self.personagem = self._sprites[self.pIdx]
        self._mapa = mapa
        self._x = x
        self._y = y

        self.tela = tela
        
        self._time_last_move = 0
        
        self.bombas = []

    def desenha(self):
        self.tela.blit(self.personagem, (self._x, self._y))

    def tratamento_eventos(self, jogador: int):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.soltar_bomba()
                    print(len(self.bombas))

        #if time.time() - self._time_last_move > 0.01:
            new_y = self._y
            new_x = self._x

            if jogador == 1:
                if pygame.key.get_pressed()[pygame.K_a]:
                    new_x = self._x - ConfigJogo.VELOCIDADE_PERSONAGEM
                if pygame.key.get_pressed()[pygame.K_d]:
                    new_x = self._x + ConfigJogo.VELOCIDADE_PERSONAGEM
                if pygame.key.get_pressed()[pygame.K_s]:
                    new_y = self._y + ConfigJogo.VELOCIDADE_PERSONAGEM
                if pygame.key.get_pressed()[pygame.K_w]:
                    new_y = self._y - ConfigJogo.VELOCIDADE_PERSONAGEM
                
                if not self._mapa.is_wall(new_x, new_y):
                    self._x = new_x
                    self._y = new_y
                    self._time_last_move = time.time()


            if jogador == 2: 
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    new_x = self._x - ConfigJogo.VELOCIDADE_PERSONAGEM
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    new_x = self._x + ConfigJogo.VELOCIDADE_PERSONAGEM
                if pygame.key.get_pressed()[pygame.K_DOWN]:
                    new_y = self._y + ConfigJogo.VELOCIDADE_PERSONAGEM
                if pygame.key.get_pressed()[pygame.K_UP]:
                    new_y = self._y - ConfigJogo.VELOCIDADE_PERSONAGEM
                
                if not self._mapa.is_wall(new_x, new_y):
                    self._x = new_x
                    self._y = new_y
                    self._time_last_move = time.time()

                if pygame.key.get_pressed()[pygame.K_0]:
                    self.soltar_bomba()

    def soltar_bomba(self):
        if len(self.bombas) < ConfigJogo.MAX_BOMBA:
            bomba = Bomba(self._x, self._y)
            self.bombas.append(bomba)