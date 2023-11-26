import pygame
from config_jogo import ConfigJogo
from utils import ler_imagem
from cronometro import Cronometro
import time
from mapa import Mapa, TileType

class Bomba:
    def __init__(self, pers, x: int, y: int, ) -> None:
        self.img_bomba = ler_imagem('items/bomba.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.img_explosao = ler_imagem('items/fogo.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.duracao = ConfigJogo.DURACAO_BOMBA
        self.alcance = ConfigJogo.ALCANCE_BOMBA
        self._x = x-x%ConfigJogo.TAM_TILE
        self.p = pers
        self._y = y-y%ConfigJogo.TAM_TILE
        self.time_lancamento = time.time()  
        self.explodida = False
        self.verificada = False
        self.colisao = self.img_bomba.get_rect(topleft=(self._x, self._y))
        self.explosao = None
        self.pos = []

    def explodir(self, tela: pygame.Surface, mapa: Mapa):
        if self.explosao:
            for i in range(self.alcance+1): #X POS
                tileType = mapa.destrutivel(self._x+i*ConfigJogo.TAM_TILE, self._y)
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x+(i)*ConfigJogo.TAM_TILE)//ConfigJogo.TAM_TILE)
                    lin = int((self._y - ConfigJogo.ALTURA_MENU)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                tela.blit(self.img_explosao, (self._x+i*ConfigJogo.TAM_TILE, self._y))
                
            for i in range(self.alcance+1): #X NEG
                tileType = mapa.destrutivel(self._x-i*ConfigJogo.TAM_TILE, self._y)
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x-(i)*ConfigJogo.TAM_TILE)//ConfigJogo.TAM_TILE)
                    lin = int((self._y - ConfigJogo.ALTURA_MENU)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                else:
                    tela.blit(self.img_explosao, (self._x-i*ConfigJogo.TAM_TILE, self._y))

            for i in range(self.alcance+1): #Y POS
                tileType = mapa.destrutivel(self._x, self._y+i*ConfigJogo.TAM_TILE)
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x)//ConfigJogo.TAM_TILE)
                    lin = int(((self._y+(i)*ConfigJogo.TAM_TILE) - ConfigJogo.ALTURA_MENU) //ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                else:
                    tela.blit(self.img_explosao, (self._x, self._y+i*ConfigJogo.TAM_TILE))

            for i in range(self.alcance+1): #Y NEG
                tileType = mapa.destrutivel(self._x, self._y-i*ConfigJogo.TAM_TILE)
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x)//ConfigJogo.TAM_TILE)
                    lin = int(((self._y-(i)*ConfigJogo.TAM_TILE) - ConfigJogo.ALTURA_MENU)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                else:
                    tela.blit(self.img_explosao, (self._x, self._y-i*ConfigJogo.TAM_TILE))
                #tela.blit(self.img_explosao, (self._x, self._y-i*ConfigJogo.TAM_TILE))
                #tela.blit(self.img_explosao, (self._x, self._y+i*ConfigJogo.TAM_TILE))
            

    def verificar(self):
        #Verifica se existe alguma bomba na posicao, se existir retorna False
        for bomba in self.p.bombas:
            if bomba._x == self._x and bomba._y == self._y:
                return False
        self.verificada = True
        return True
            
    def atualizar(self, mapa: Mapa):
        tempo_atual = time.time()

        if not self.explodida and tempo_atual - self.time_lancamento > self.duracao:
            self.explodida = True
        elif self.explodida and tempo_atual - self.time_lancamento < self.duracao+0.5:
            self.explosao = True
            for pos in self.pos:
                lin = pos[0]
                col = pos[1]
                mapa.explodirBloco(lin, col, 0)
        elif self.explodida and tempo_atual - self.time_lancamento > self.duracao+0.5:
            for pos in self.pos:
                lin = pos[0]
                col = pos[1]
                mapa.explodirBloco(lin, col, 1)
            self.explosao = False
            self.p.bombas.remove(self)
            
    def desenha(self, tela: pygame.Surface, mapa: Mapa):
        self.atualizar(mapa)
        if not self.explodida and self.verificada:
            tela.blit(self.img_bomba, (self._x, self._y))
        if self.explodida:
            self.explodir(tela, mapa)

    def getX(self):
        return self._x
    
    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y
    
    def setY(self, y):
        self._y = y