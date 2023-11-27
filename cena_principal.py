import sys
import time
from typing import Tuple
from bomba import Bomba
from mapa import Mapa, TileType
from personagem import Personagem
import pygame
from cronometro import Cronometro
from config_jogo import ConfigJogo
from utils import ler_imagem
from quartel import Quartel
import random
from pygame import gfxdraw
from fantasma import Fantasma
import math
import numpy as np


class CenaPrincipal():
    def __init__(self, tela: pygame.display, num_jogadores: int, bombas: list[list[Bomba], list[Bomba]]):
        self.mapa = Mapa()
        self.tela = tela
        self.encerrada = False
        self.inimigos = []
        self.quartel = Quartel(self.mapa, self.tela)
        self.cronometro = Cronometro()
        self.bombas = bombas
        self.cd_personagem = ConfigJogo.CD_PERSONAGEM
        self.cooldown_adjusted = False
        self.closest_ghost_type = None
        
        self._time_last_spawn = 0
        self.img_relogio = ler_imagem('telas/relogio.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))

        if num_jogadores == 1:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU, self.tela, self.quartel)
            self.p2: Personagem = False
        else:
            self.p1 = Personagem(self.mapa, ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU, self.tela, self.quartel)

            self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE), self.tela, self.quartel)
            while(self.p1.pIdx == self.p2.pIdx):
                self.p2 = Personagem(self.mapa, (ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE), (ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE), self.tela, self.quartel)
                
    def rodar(self):
        while not self.encerrada:
            self.mapa.desenha(self.tela)
            
            """
                if inimigo.colidido:
                    self.inimigos.remove(inimigo)

                         
                for projetil in self.inimigos[i].projeteis:
                projetil.desenha(self.tela)
                projetil.tratamento_eventos()
                if projetil.colidido:
                    self.alien.projeteis.remove(projetil)
                    """

            for bomba in self.p1.bombas:
                print(self.p1.colisao)
                bomba.desenha(self.tela, self.mapa, self.bombas, self.p1.colisao, self.p1.colisao)
            if self.p2:
                for bomba in self.p2.bombas:
                    bomba.desenha(self.tela, self.mapa, self.bombas, self.p1.colisao, self.p2.colisao)
            
            self.p1.desenha()
            if self.p2:
                self.p2.desenha()

            if ConfigJogo.INIMIGOS:
                self.quartel.desenha(self.bombas)
                self.quartel.tratamento_eventos(self.bombas)
            self.tratamento_eventos()
            self.desenha_menu()
       
            pygame.display.flip()

    def tratamento_eventos(self):
        #gfxdraw.pixel(self.tela, self.p1.getX()-1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2), (255,0,0))
        #if self.p1._mapa.destrutivel(self.p1.getX()-1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
        #    print("colidiu")
        tempo = time.time()
        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)
            
        if len(self.quartel.fantasmas) > 0:
            ghost_positions = np.array([(float(inimigo.getX()), float(inimigo.getY()), inimigo.get_tipo_aura()) for inimigo in self.quartel.fantasmas])
            ghost_positions = np.atleast_2d(ghost_positions)
            distances = np.sqrt((self.p1.getX() - ghost_positions[:, 0])**2 + (self.p1.getY() - ghost_positions[:, 1])**2)
            closest_ghost_index = np.argmin(distances)

            # Check if the character is currently within a ghost aura and the adjustment has not been made yet
            if distances[closest_ghost_index] <= ConfigJogo.RAIO_AURA:
                closest_ghost_type_aura = ghost_positions[closest_ghost_index, 2]

                # Check if the closest ghost or aura type has changed
                if not self.cooldown_adjusted or self.closest_ghost_type != closest_ghost_type_aura:
                    if closest_ghost_type_aura == 0:
                        self.cd_personagem = self.cd_personagem * ConfigJogo.COEFICIENTE_AURA
                    elif closest_ghost_type_aura == 1:
                        self.cd_personagem = self.cd_personagem / ConfigJogo.COEFICIENTE_AURA

                    # Set the flag to indicate that the adjustment has been made
                    self.cooldown_adjusted = True
                    self.closest_ghost_type = closest_ghost_type_aura

            # Check if the character is outside the ghost aura, reset the flag
            elif distances[closest_ghost_index] > ConfigJogo.RAIO_AURA:
                self.cooldown_adjusted = False
                self.cd_personagem = ConfigJogo.CD_PERSONAGEM
        else:
            # Handle the case when there are no ghosts
            self.cooldown_adjusted = False
            self.cd_personagem = ConfigJogo.CD_PERSONAGEM

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.p1.soltar_bomba(self.bombas, 1)
                if event.key == pygame.K_0 and self.p2:
                    self.p2.soltar_bomba(self.bombas, 2)

        if self.p1 and tempo - self.p1._time_last_move > self.cd_personagem:
            if tempo - self.p1.time_inalvejavel < 5:
                if ((tempo - self.p1.time_inalvejavel) % 0.5) < 0.25:
                    self.p1.personagem.set_alpha(100)
                else:
                    self.p1.personagem.set_alpha(190)
            else:
                self.p1.personagem.set_alpha(255)

            new_p1x = self.p1.getX()
            new_p1y = self.p1.getY()
        
            if pygame.key.get_pressed()[pygame.K_a]:
                if (self.p1.getY()%ConfigJogo.TAM_TILE)<15 and (self.p1.getY()%ConfigJogo.TAM_TILE)!=0 and self.p1._mapa.destrutivel(self.p1.getX()-1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                    new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                elif (self.p1.getY()%ConfigJogo.TAM_TILE)>17 and self.p1._mapa.destrutivel(self.p1.getX()-1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                    new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                else:
                    new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                                
            if pygame.key.get_pressed()[pygame.K_d]:
                if (self.p1.getY()%ConfigJogo.TAM_TILE)<15 and (self.p1.getY()%ConfigJogo.TAM_TILE)!=0 and self.p1._mapa.destrutivel(self.p1.getX()+ConfigJogo.TAM_TILE+1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                    new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                elif (self.p1.getY()%ConfigJogo.TAM_TILE)>17 and self.p1._mapa.destrutivel(self.p1.getX()+ConfigJogo.TAM_TILE+1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                    new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                else:
                    new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        
            if pygame.key.get_pressed()[pygame.K_s]:
                if (self.p1.getX()%ConfigJogo.TAM_TILE)<15 and (self.p1.getX()%ConfigJogo.TAM_TILE)!=0 and self.p1._mapa.destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()+ConfigJogo.TAM_TILE+1)==TileType.GRAMA.value:
                   new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                elif (self.p1.getX()%ConfigJogo.TAM_TILE)>17 and self.p1._mapa.destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()+ConfigJogo.TAM_TILE+1)==TileType.GRAMA.value:
                    new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                else:
                    new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM

            if pygame.key.get_pressed()[pygame.K_w]:
                if (self.p1.getX()%ConfigJogo.TAM_TILE)<15 and (self.p1.getX()%ConfigJogo.TAM_TILE)!=0 and self.p1._mapa.destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()-1)==TileType.GRAMA.value:
                   new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                elif (self.p1.getX()%ConfigJogo.TAM_TILE)>17 and self.p1._mapa.destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()-1)==TileType.GRAMA.value:
                    new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                else:
                    new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
            
            if not self.p1._mapa.is_any_wall(new_p1x, new_p1y):

                bombaColisao = False

                for bombaVetor in self.bombas:
                    for bomba in bombaVetor:  
                        if not bomba.explosao and not self.p1.colisao.colliderect(bomba.colisao): #Para não colidir após colocar a bomba
                            bomba_tile = (bomba.getX() // ConfigJogo.TAM_TILE, bomba.getY() // ConfigJogo.TAM_TILE)
                            new_p1_tile_left = (new_p1x // ConfigJogo.TAM_TILE, new_p1y // ConfigJogo.TAM_TILE)
                            new_p1_tile_right = ((new_p1x + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE, new_p1y // ConfigJogo.TAM_TILE)
                            new_p1_tile_down = (new_p1x // ConfigJogo.TAM_TILE, (new_p1y + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE)

                            if bomba_tile in [new_p1_tile_left, new_p1_tile_right, new_p1_tile_down]:
                                bombaColisao = True
                        if bomba.explosao: # colisao com a explosao
                            for rect in bomba.explosoes:
                                if rect.colliderect(self.p1.colisao):
                                    if time.time() - self.p1.time_inalvejavel > 5:
                                        print(self.p1.vida)
                                        self.p1.vida -= 1
                                        if self.p1.vida == 0:
                                            self.encerrada = True
                                            print("GAME OVER")
                                            sys.exit(0)
                                        else:
                                            new_p1x = ConfigJogo.TAM_TILE
                                            new_p1y = ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU
                                            self.p1.time_inalvejavel=time.time()

                if not bombaColisao:
                    self.p1.setX(new_p1x)
                    self.p1.setY(new_p1y)
                    self.p1.colisao = self.p1.personagem.get_rect(topleft=(new_p1x, new_p1y))

                    self.p1._time_last_move = time.time()

        if self.p2 and time.time() - self.p2._time_last_move > 0.01: 
            if tempo - self.p2.time_inalvejavel < 5:
                if ((tempo - self.p2.time_inalvejavel) % 0.5) < 0.25:
                    self.p2.personagem.set_alpha(100)
                else:
                    self.p2.personagem.set_alpha(190)
            else:
                self.p2.personagem.set_alpha(255)

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
                for bombaVetor in self.bombas:
                    for bomba in bombaVetor:  
                        if not bomba.explosao and not self.p2.colisao.colliderect(bomba.colisao): #Para não colidir após colocar a bomba
                            bomba_tile = (bomba.getX() // ConfigJogo.TAM_TILE, bomba.getY() // ConfigJogo.TAM_TILE)
                            new_p2_tile_left = (new_p2x // ConfigJogo.TAM_TILE, new_p2y // ConfigJogo.TAM_TILE)
                            new_p2_tile_right = ((new_p2x + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE, new_p2y // ConfigJogo.TAM_TILE)
                            new_p2_tile_down = (new_p2x // ConfigJogo.TAM_TILE, (new_p2y + ConfigJogo.TAM_TILE - 1) // ConfigJogo.TAM_TILE)

                            if bomba_tile in [new_p2_tile_left, new_p2_tile_right, new_p2_tile_down]:
                                bombaColisao = True
                        if bomba.explosao: # colisao com a explosao
                            for rect in bomba.explosoes:
                                if rect.colliderect(self.p2.colisao):
                                    if time.time() - self.p2.time_inalvejavel > 5:
                                        self.p2.vida -= 1
                                        if self.p2.vida == 0:
                                            self.encerrada = True
                                            print("GAME OVER")
                                            sys.exit(0)
                                        else:
                                            new_p2x = ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE
                                            new_p2y = ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE
                                            self.p2.time_inalvejavel=time.time()

                if not bombaColisao:
                    self.p2.setX(new_p2x)
                    self.p2.setY(new_p2y)
                    self.p2.colisao = self.p2.personagem.get_rect(topleft=(new_p2x, new_p2y))

                    self.p2._time_last_move = time.time()


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

    def verifica_aura(self, personagem: Personagem):
        if len(self.quartel.fantasmas) > 0:
            ghost_positions = np.array([(float(inimigo.getX()), float(inimigo.getY()), inimigo.get_tipo_aura()) for inimigo in self.quartel.fantasmas])
            ghost_positions = np.atleast_2d(ghost_positions)
            distances = np.sqrt((self.p1.getX() - ghost_positions[:, 0])**2 + (self.p1.getY() - ghost_positions[:, 1])**2)
            closest_ghost_index = np.argmin(distances)

            # Check if the character is currently within a ghost aura and the adjustment has not been made yet
            if distances[closest_ghost_index] <= ConfigJogo.RAIO_AURA:
                closest_ghost_type_aura = ghost_positions[closest_ghost_index, 2]

                # Check if the closest ghost or aura type has changed
                if not self.cooldown_adjusted or self.closest_ghost_type != closest_ghost_type_aura:
                    if closest_ghost_type_aura == 0:
                        self.cd_personagem = self.cd_personagem * ConfigJogo.COEFICIENTE_AURA
                    elif closest_ghost_type_aura == 1:
                        self.cd_personagem = self.cd_personagem / ConfigJogo.COEFICIENTE_AURA

                    # Set the flag to indicate that the adjustment has been made
                    self.cooldown_adjusted = True
                    self.closest_ghost_type = closest_ghost_type_aura

            # Check if the character is outside the ghost aura, reset the flag
            elif distances[closest_ghost_index] > ConfigJogo.RAIO_AURA:
                self.cooldown_adjusted = False
                self.cd_personagem = ConfigJogo.CD_PERSONAGEM
        else:
            # Handle the case when there are no ghosts
            self.cooldown_adjusted = False
            self.cd_personagem = ConfigJogo.CD_PERSONAGEM