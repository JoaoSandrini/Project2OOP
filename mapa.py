import sys
import pygame
import csv
from enum import Enum
from configJogo import ConfigJogo
from lerImagem import lerImagem

class TileType(Enum):
    GRAMA = 0 
    DESTRUTIVELC = 1
    DESTRUTIVELM = 2
    FIXA = 3
class Mapa:
    def __init__(self): 
        self.grama = lerImagem('map/grama.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.destrutivelC = lerImagem('map/parede-destruivel.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.destrutivelM = lerImagem('map/parede-destruivel-marrom.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.fixa = lerImagem('map/parede-fixa.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        self._mapMatrix = []
        with open('map/MapMatrix.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile)
            for linha in spamreader:
                linha = [int(valor) for valor in linha]
                self._mapMatrix.append(linha)
 
    def desenha(self, tela: pygame.Surface):
        for lin_idx in range(len(self._mapMatrix)):
            py = lin_idx * ConfigJogo.TAM_TILE
            for col_idx in range(len(self._mapMatrix[0])):
                px = col_idx * ConfigJogo.TAM_TILE

                if self._mapMatrix[lin_idx][col_idx] == TileType.GRAMA:
                    tela.blit(self.grama, (px, py))

                elif self._mapMatrix[lin_idx][col_idx] == TileType.DESTRUTIVELC:
                    tela.blit(self.destrutivelC, (px, py))

                elif self._mapMatrix[lin_idx][col_idx] == TileType.DESTRUTIVELM:
                    tela.blit(self.destrutivelM, (px, py))

                elif self._mapMatrix[lin_idx][col_idx] == TileType.FIXA:
                    tela.blit(self.fixa, (px, py))
                
        pygame.display.flip()
    """
    def is_wall(self, x, y):
        return self._grid[y][x] == TileType.WALL

    def eat(self, x, y):
        if self._grid[y][x] == TileType.WITH_FOOD:
            self._grid[y][x] = TileType.EMPTY
    """
