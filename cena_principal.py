import sys
import time
from typing import Tuple
from mapa import Mapa, TileType
from personagem import Personagem
from fantasma import Fantasma
from alienigena import Aienigena
import pygame
from cronometro import Cronometro
from config_jogo import ConfigJogo
from utils import ler_imagem
from quartel import Quartel
import random

class CenaPrincipal():
    def __init__(self, tela: pygame.display, num_jogadores: int):
        self.mapa = Mapa()
        self.tela = tela
        self.encerrada = False
        self.inimigos = []
        self.quartel = Quartel()
        self.cronometro = Cronometro()
        
        self._time_last_spawn = 0
        self.img_relogio = ler_imagem('telas/relogio.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        if num_jogadores == 1:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU, self.tela)
            self.p2 = False
        else:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU, self.tela)

            self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE), self.tela)
            while(self.p1.pIdx == self.p2.pIdx):
                self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE), self.tela)
                
    def rodar(self):
        while not self.encerrada:
            self.desenha_menu()
            self.mapa.desenha(self.tela)
            
            self.quartel.desenha(self.tela)

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
                """
                if inimigo.colidido:
                    self.inimigos.remove(inimigo)

                         
                for projetil in self.inimigos[i].projeteis:
                projetil.desenha(self.tela)
                projetil.tratamento_eventos()
                if projetil.colidido:
                    self.alien.projeteis.remove(projetil)
                    """

            self.p1.desenha()
            if self.p2!=False:
                self.p2.desenha()

            self.tratamento_eventos()


            for bomba in self.p1.bombas:
                bomba.desenha(self.tela, self.mapa)
            if self.p2:
                for bomba in self.p2.bombas:
                    bomba.desenha(self.tela, self.mapa)
       
            pygame.display.flip()

    def tratamento_eventos(self):            
        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.p1.soltar_bomba()
                if event.key == pygame.K_0 and self.p2:
                    self.p2.soltar_bomba()

        if  time.time() - self._time_last_spawn > 2:
            rand = random.randint(0, 1)
            if rand == 0:
                self.inimigos.append(Fantasma(self.mapa, self.tela))
            elif rand == 1:
                self.inimigos.append(Aienigena(self.mapa, self.tela))
            self._time_last_spawn = time.time()

        if self.p1 and time.time() - self.p1._time_last_move > 0.01:
            new_p1x = self.p1.getX()
            new_p1y = self.p1.getY()
        
            if pygame.key.get_pressed()[pygame.K_a]:
                new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_d]:
                new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_s]:
                #print(self.p1.getX()%ConfigJogo.TAM_TILE)
                #if (self.p1.getX()%ConfigJogo.TAM_TILE)<15 and (self.p1.getX()%ConfigJogo.TAM_TILE)!=0:
                 #   new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                #else:
                new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_w]:
                new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
            
            if not self.p1._mapa.is_any_wall(new_p1x, new_p1y):
                bombaColisao = False
                for bomba in self.p1.bombas:
                    if not bomba.explosao and not self.p1.colisao.colliderect(bomba.colisao): #Para não colidir após colocar a bomba
                        bomba_tile = (bomba.getX() // ConfigJogo.TAM_TILE, bomba.getY() // ConfigJogo.TAM_TILE)
                        new_p1_tile_left = (new_p1x // ConfigJogo.TAM_TILE, new_p1y // ConfigJogo.TAM_TILE)
                        new_p1_tile_right = ((new_p1x + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE, new_p1y // ConfigJogo.TAM_TILE)
                        new_p1_tile_down = (new_p1x // ConfigJogo.TAM_TILE, (new_p1y + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE)

                        if bomba_tile in [new_p1_tile_left, new_p1_tile_right, new_p1_tile_down]:
                            bombaColisao = True

                if not bombaColisao:
                    self.p1.setX(new_p1x)
                    self.p1.setY(new_p1y)
                    self.p1.colisao = self.p1.personagem.get_rect(topleft=(new_p1x, new_p1y))

                    self.p1._time_last_move = time.time()

        if self.p2 and time.time() - self.p2._time_last_move > 0.01: 
            new_p2x = self.p2.getX()
            new_p2y = self.p2.getY()

            if pygame.key.get_pressed()[pygame.K_LEFT]:
                new_p2x = self.p2.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                new_p2x = self.p2.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                new_p2y = self.p2.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
            if pygame.key.get_pressed()[pygame.K_UP]:
                new_p2y = self.p2.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
            
            if not self.p2._mapa.is_any_wall(new_p2x, new_p2y):
                bombaColisao = False
                for bomba in self.p2.bombas:
                    if not bomba.explosao and not self.p2.colisao.colliderect(bomba.colisao): #Para não colidir após colocar a bomba
                        bomba_tile = (bomba.getX() // ConfigJogo.TAM_TILE, bomba.getY() // ConfigJogo.TAM_TILE)
                        new_p2_tile_left = (new_p2x // ConfigJogo.TAM_TILE, new_p2y // ConfigJogo.TAM_TILE)
                        new_p2_tile_right = ((new_p2x + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE, new_p2y // ConfigJogo.TAM_TILE)
                        new_p2_tile_down = (new_p2x // ConfigJogo.TAM_TILE, (new_p2y + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE)

                        if bomba_tile in [new_p2_tile_left, new_p2_tile_right, new_p2_tile_down]:
                            bombaColisao = True

                if not bombaColisao:
                    self.p2.setX(new_p2x)
                    self.p2.setY(new_p2y)
                    self.p2.colisao = self.p2.personagem.get_rect(topleft=(new_p2x, new_p2y))

                    self.p2._time_last_move = time.time()

            #if pygame.key.get_pressed()[pygame.K_0]:
            #    self.soltar_bomba()

    def desenha_menu(self):
        pygame.draw.rect(self.tela, ConfigJogo.COR_HUD, (0, 0, ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_MENU))
        pygame.draw.rect(self.tela, ConfigJogo.COR_BORDA_HUD, (0, 0, ConfigJogo.LARGURA_TELA, ConfigJogo.ALTURA_MENU), 4)

        fonte_hud = pygame.font.SysFont(None, ConfigJogo.FONTE_HUD)
        tempo_restante = int(ConfigJogo.DURACAO_JOGO - self.cronometro.tempo_passado())
        minutos =  tempo_restante // 60
        segundos =  tempo_restante % 60

        if segundos >= 10:
            mostra_tempo = fonte_hud.render(f'{minutos:.0f}:{segundos:.0f}', True, ConfigJogo.COR_FONTE_HUD)
        else:
            mostra_tempo = fonte_hud.render(f'{minutos:.0f}:0{segundos:.0f}', True, ConfigJogo.COR_FONTE_HUD)
        self.tela.blit(mostra_tempo, (ConfigJogo.LARGURA_TELA * .12, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
        self.tela.blit(self.img_relogio, (ConfigJogo.LARGURA_TELA * .05, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))


        if not self.p2:
            self.tela.blit(self.p1.personagem, (ConfigJogo.LARGURA_TELA * .5, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            mostra_pont_p1 = fonte_hud.render(f'{self.p1.pontos}', True, ConfigJogo.COR_FONTE_HUD)
            self.tela.blit(mostra_pont_p1, (ConfigJogo.LARGURA_TELA * .57, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            self.tela.blit(self.img_relogio, (ConfigJogo.LARGURA_TELA * .05, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            
        
        else:
            mostra_pont_p1 = fonte_hud.render(f'{self.p1.pontos}', True, ConfigJogo.COR_FONTE_HUD)
            mostra_pont_p2 = fonte_hud.render(f'{self.p2.pontos}', True, ConfigJogo.COR_FONTE_HUD)

            self.tela.blit(mostra_pont_p1, (ConfigJogo.LARGURA_TELA * .57, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            self.tela.blit(mostra_pont_p2, (ConfigJogo.LARGURA_TELA * .82, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            self.tela.blit(self.p1.personagem, (ConfigJogo.LARGURA_TELA * .5, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            self.tela.blit(self.p2.personagem, (ConfigJogo.LARGURA_TELA * .75, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

