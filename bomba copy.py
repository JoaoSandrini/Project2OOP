import pygame
from config_jogo import ConfigJogo
from utils import ler_imagem
from cronometro import Cronometro
import time
from mapa import Mapa, TileType

class Bomba:
    def __init__(self, pers, x: int, y: int, quartel) -> None:
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
        self.explosoes = []
        self.explosao = None
        self.pos = []
        self.diferencaTempo = 0
        self.tempoDaExplosao = 0
        self.inimigos = []
        self.quartel = quartel
        self.alcanceXP = self.alcance+1
        self.alcanceXN = self.alcance+1
        self.alcanceYP = self.alcance+1
        self.alcanceYN = self.alcance+1
        self.primeiraColisaoXP = False
        self.primeiraColisaoXN = False
        self.primeiraColisaoYP = False
        self.primeiraColisaoYN = False

    def verificarExplosao(self, tela: pygame.Surface, mapa: Mapa, p1, p2, alcance, primeiraColisao, direcao, direcao2, sentido, eixo):
        for i in range(alcance): 
            tileType = mapa.destrutivel(direcao+sentido*i*ConfigJogo.TAM_TILE if eixo == 1 else direcao, direcao2 if eixo == 1 else direcao+sentido*i*ConfigJogo.TAM_TILE)
            colisaoExplosao = pygame.Rect(direcao+sentido*i*ConfigJogo.TAM_TILE if eixo == 1 else direcao, direcao2 if eixo == 1 else direcao+sentido*i*ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
            if not primeiraColisao:
                if colisaoExplosao.colliderect(p1) or colisaoExplosao.colliderect(p2):
                    alcance = i+1
                    primeiraColisao = True
                for inimigo in self.inimigos:
                    if colisaoExplosao.colliderect(inimigo.colisao):
                        alcance = i+1
                        primeiraColisao = True
                        break

        if self.explosao:
            for i in range(alcance): 
                tileType = mapa.destrutivel(direcao+sentido*i*ConfigJogo.TAM_TILE if eixo == 1 else direcao, direcao2 if eixo == 1 else direcao+sentido*i*ConfigJogo.TAM_TILE)
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((direcao+sentido*i*ConfigJogo.TAM_TILE if eixo == 1 else direcao)//ConfigJogo.TAM_TILE)
                    lin = int((direcao2 - ConfigJogo.ALTURA_MENU if eixo == 1 else direcao+sentido*i*ConfigJogo.TAM_TILE)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                tela.blit(self.img_explosao, (direcao+sentido*i*ConfigJogo.TAM_TILE if eixo == 1 else direcao, direcao2 if eixo == 1 else direcao+sentido*i*ConfigJogo.TAM_TILE))
                self.explosoes.append(colisaoExplosao)

    def explodir(self, tela: pygame.Surface, mapa: Mapa, p1, p2):
        #VARER AREA, SE HOUVER ALGUEM - DELIMITAR, SE NAO EXPLODE TUDO.
        #DEPOIS LOOP COM PRINT DAS EXPLOSÕES, NAO É DIFICULT OK?
        self.verificarExplosao(tela, mapa, p1, p2, self.alcanceXP, self.primeiraColisaoXP, self._x, self._y, 1, 1)
        self.verificarExplosao(tela, mapa, p1, p2, self.alcanceXN, self.primeiraColisaoXN, self._x, self._y, -1, 1)
        self.verificarExplosao(tela, mapa, p1, p2, self.alcanceYP, self.primeiraColisaoYP, self._x, self._y, 1, 2)
        self.verificarExplosao(tela, mapa, p1, p2, self.alcanceYN, self.primeiraColisaoYN, self._x, self._y, -1, 2)
        """
        for i in range(self.alcanceXP): #X POS
            tileType = mapa.destrutivel(self._x+i*ConfigJogo.TAM_TILE, self._y)
            colisaoExplosao = pygame.Rect(self._x+i*ConfigJogo.TAM_TILE, self._y, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
            if not self.primeiraColisaoXP:
                if colisaoExplosao.colliderect(p1) or colisaoExplosao.colliderect(p2):
                    self.alcanceXP = i+1
                    self.primeiraColisaoXP = True
                for inimigo in self.inimigos:
                    print(colisaoExplosao.colliderect(p2))
                    if colisaoExplosao.colliderect(inimigo.colisao):
                        self.alcanceXP = i+1
                        self.primeiraColisaoXP = True
                        break

        if self.explosao:
            for i in range(self.alcanceXP): #X POS
                tileType = mapa.destrutivel(self._x+i*ConfigJogo.TAM_TILE, self._y)
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x+i*ConfigJogo.TAM_TILE)//ConfigJogo.TAM_TILE)
                    lin = int((self._y - ConfigJogo.ALTURA_MENU)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                tela.blit(self.img_explosao, (self._x+i*ConfigJogo.TAM_TILE, self._y))
                self.explosoes.append(colisaoExplosao)

            for i in range(self.alcanceXN): #X NEG
                tileType = mapa.destrutivel(self._x-i*ConfigJogo.TAM_TILE, self._y)
                colisaoExplosao = pygame.Rect(self._x-i*ConfigJogo.TAM_TILE, self._y, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
                if not self.primeiraColisaoXN:
                    for inimigo in self.inimigos:
                        if colisaoExplosao.colliderect(inimigo.colisao) or colisaoExplosao.colliderect(p1) or colisaoExplosao.colliderect(p2):
                            self.alcanceXN = i+1
                            self.primeiraColisaoXN = True
                            break
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x-(i)*ConfigJogo.TAM_TILE)//ConfigJogo.TAM_TILE)
                    lin = int((self._y - ConfigJogo.ALTURA_MENU)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                else:
                    tela.blit(self.img_explosao, (self._x-i*ConfigJogo.TAM_TILE, self._y))
                    self.explosoes.append(colisaoExplosao)

            for i in range(self.alcanceYP): #Y POS
                tileType = mapa.destrutivel(self._x, self._y+i*ConfigJogo.TAM_TILE)
                colisaoExplosao = pygame.Rect(self._x, self._y+i*ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
                if not self.primeiraColisaoYP:
                    for inimigo in self.inimigos:
                        if colisaoExplosao.colliderect(inimigo.colisao) or colisaoExplosao.colliderect(p1) or colisaoExplosao.colliderect(p2):
                            self.alcanceYP = i+1
                            self.primeiraColisaoYP = True
                            break
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x)//ConfigJogo.TAM_TILE)
                    lin = int(((self._y+(i)*ConfigJogo.TAM_TILE) - ConfigJogo.ALTURA_MENU) //ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                else:
                    tela.blit(self.img_explosao, (self._x, self._y+i*ConfigJogo.TAM_TILE))
                    self.explosoes.append(colisaoExplosao)

            for i in range(self.alcanceYN): #Y NEG
                tileType = mapa.destrutivel(self._x, self._y-i*ConfigJogo.TAM_TILE)
                colisaoExplosao = pygame.Rect(self._x, self._y-i*ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE)
                if not self.primeiraColisaoYN:
                    for inimigo in self.inimigos:
                        if colisaoExplosao.colliderect(inimigo.colisao) or colisaoExplosao.colliderect(p1) or colisaoExplosao.colliderect(p2):
                            self.alcanceYN = i+1
                            self.primeiraColisaoYN = True
                            break
                if tileType == TileType.DESTRUTIVEL_C.value or tileType == TileType.FIXA.value:
                    col = int((self._x)//ConfigJogo.TAM_TILE)
                    lin = int(((self._y-(i)*ConfigJogo.TAM_TILE) - ConfigJogo.ALTURA_MENU)//ConfigJogo.TAM_TILE)
                    if tileType == TileType.DESTRUTIVEL_C.value:
                        self.pos.append([lin, col])
                    break
                else:
                    tela.blit(self.img_explosao, (self._x, self._y-i*ConfigJogo.TAM_TILE))
                    self.explosoes.append(colisaoExplosao)
"""
    def verificar(self):
        #Verifica se existe alguma bomba na posicao, se existir retorna False
        for bomba in self.p.bombas:
            if bomba._x == self._x and bomba._y == self._y:
                return False
        self.verificada = True
        return True
            
    def atualizar(self, mapa: Mapa, bombasVetores):
        self.inimigos = self.quartel.getInimigos()
        tempo_atual = time.time()
        if not self.explodida:
            self.diferencaTempo  = tempo_atual - self.time_lancamento
        else:
            self.diferencaTempo  = tempo_atual - self.tempoDaExplosao

        for bombaVetor in bombasVetores:
            for bomba in bombaVetor:
                if bomba.explosao: # colisao com a explosao
                    for rect in bomba.explosoes:
                        if rect.colliderect(self.colisao):
                            self.diferencaTempo = self.duracao+0.1

        if not self.explodida and self.diferencaTempo > self.duracao:
            self.explodida = True
            self.colisao = pygame.Rect(self._x-1000, self._y-1000, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE) #Retira da tela
            self.tempoDaExplosao = time.time()
        elif self.explodida and self.diferencaTempo < 0.5:
            self.explosao = True
            for pos in self.pos:
                lin = pos[0]
                col = pos[1]
                mapa.explodirBloco(lin, col, 0)
        elif self.explodida and self.diferencaTempo > 0.5:
            for pos in self.pos:
                lin = pos[0]
                col = pos[1]
                mapa.explodirBloco(lin, col, 1)
            self.explosao = False
            self.p.bombas.remove(self)
            for bombasVetor in bombasVetores:
                if self in bombasVetor:
                    bombasVetor.remove(self)
            
    def desenha(self, tela: pygame.Surface, mapa: Mapa, bombasVetores, projeteis, p1, p2):
        self.atualizar(mapa, bombasVetores, projeteis)
        if not self.explodida and self.verificada:
            tela.blit(self.img_bomba, (self._x, self._y))
        if self.explodida:
            self.explodir(tela, mapa, p1, p2)

    def getX(self):
        return self._x
    
    def setX(self, x):
        self._x = x

    def getY(self):
        return self._y
    
    def setY(self, y):
        self._y = y