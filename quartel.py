from utils import ler_imagem
from config_jogo import ConfigJogo
from fantasma import Fantasma
from alienigena import Alienigena
import pygame
import random   
import time
from mapa import Mapa
from personagem import Personagem
class Quartel:
    def __init__(self, mapa: Mapa, tela: pygame.Surface):
        self.img_quartel = ler_imagem('enemies/ship.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self.grama = mapa.grama
        self._x = ConfigJogo.QUARTEL_X
        self._y = ConfigJogo.QUARTEL_Y 
        self._vida = ConfigJogo.VIDA_QUARTEL
        self.inimigos = []
        self.fantasmas = []
        self._time_last_spawn = 0
        self.mapa = mapa
        self.tela = tela
        self.time_inalvejavel = 0
        self.colisao = self.img_quartel.get_rect(topleft=(self._x, self._y)) #atualiza a colisao


    def tratamento_eventos(self, bombaVetores):
        timeAtt = time.time()
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
                                    bomba.p.addPontos(ConfigJogo.PONTUACAO_QUARTEL)
                                    self.img_quartel = self.grama
                                    pass
        
        if ConfigJogo.INIMIGOS:
            if  time.time() - self._time_last_spawn > ConfigJogo.CD_SPAWN and len(self.inimigos) < ConfigJogo.MAX_INIMIGOS:
                if len(self.inimigos) < ConfigJogo.MAX_INIMIGOS:
                    rand = random.randint(0, 1)
                    if rand == 0:
                        self.inimigos.append(Fantasma(self.mapa, self.tela))
                        self.fantasmas.append(self.inimigos[-1])
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
    
    def testInimigos(self):
        al1 = Alienigena(self.mapa, self.tela)
        al1.setX(400)
        al1.setY(200)
        self.inimigos.append(al1)

        al2 = Alienigena(self.mapa, self.tela)
        al2.setX(150)
        al2.setY(100)
        self.inimigos.append(al2)

        al1 = Alienigena(self.mapa, self.tela)
        al1.setX(100)
        al1.setY(200)
        self.inimigos.append(al1)

        al1 = Alienigena(self.mapa, self.tela)
        al1.setX(150)
        al1.setY(400)
        self.inimigos.append(al1)
    
    def getVida(self):
        return self._vida
    
    def quartel_colisao(self, x, y):
        if self.colisao.collidepoint(x, y):
            return True
        return False

    def get_vida(self):
        return self._vida
    
    def set_vida(self, vida):
        self._vida = vida