import sys
import pygame
import csv
from enum import Enum
from config_jogo import ConfigJogo
from utils import ler_imagem

class TileType(Enum):
    GRAMA = 0 
    DESTRUTIVEL_C = 1
    DESTRUTIVEL_M = 2
    FIXA = 3
class Mapa:
    def __init__(self): 
        self.grama = ler_imagem('map/grama.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.destrutivel_c = ler_imagem('map/parede-destruivel.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.destrutivel_m = ler_imagem('map/parede-destruivel-marrom.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.fixa = ler_imagem('map/parede-fixa.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        self.map_matrix = []
        with open('map/mapMatrix.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for linha in spamreader:
                linha = [int(valor) for valor in linha]
                self.map_matrix.append(linha)
 
    def desenha(self, tela: pygame.Surface):
        for lin_idx in range(len(self.map_matrix)):
            py = lin_idx * ConfigJogo.TAM_TILE
            for col_idx in range(len(self.map_matrix[0])):
                px = col_idx * ConfigJogo.TAM_TILE

                if self.map_matrix[lin_idx][col_idx] == TileType.GRAMA.value:
                    tela.blit(self.grama, (px, py))

                elif self.map_matrix[lin_idx][col_idx] == TileType.DESTRUTIVEL_C.value:
                    tela.blit(self.destrutivel_c, (px, py))

                elif self.map_matrix[lin_idx][col_idx] == TileType.DESTRUTIVEL_M.value:
                    tela.blit(self.destrutivel_m, (px, py))

                elif self.map_matrix[lin_idx][col_idx] == TileType.FIXA.value:
                    tela.blit(self.fixa, (px, py))

    def is_wall(self, x, y):

        lin_idx_c_e = y // ConfigJogo.TAM_TILE
        col_idx_c_e = x // ConfigJogo.TAM_TILE
        lin_idx_b_d = (y + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE
        col_idx_b_d = (x + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE

        for lin_idx in range(lin_idx_c_e, lin_idx_b_d + 1):
            for col_idx in range(col_idx_c_e, col_idx_b_d + 1):
                if 0 <= lin_idx < len(self.map_matrix) and 0 <= col_idx < len(self.map_matrix[0]):
                    tile_type = self.map_matrix[lin_idx][col_idx]
                    if tile_type != TileType.GRAMA.value:
                        return True

