import sys
import time
from typing import Tuple
from alienigena import Alienigena
from bomba import Bomba
from mapa import Mapa, TileType
from personagem import Personagem
import pygame
from cronometro import Cronometro
from config_jogo import ConfigJogo
from projetil import Projetil
from utils import ler_imagem
from quartel import Quartel
import numpy as np

class CenaPrincipal():
    def __init__(self, tela: pygame.display, num_jogadores: int, bombas: list[list[Bomba], list[Bomba]], projeteis: list[Projetil]):
        self.mapa = Mapa()
        self.tela = tela
        self.encerrada = False
        self.inimigos = []
        self.quartel = Quartel(self.mapa, self.tela)
        self.cronometro = Cronometro()
        self.bombas = bombas
        self.projeteis = projeteis
        self.derrota = True
        
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

    def verifica_aura(self, personagem: Personagem):
        self.quartel.fantasmas = [fantasma for fantasma in self.quartel.fantasmas if not fantasma.morto]
        if self.quartel.fantasmas: 
            posicoes_fantasmas = np.array([
                (float(inimigo.getX()), float(inimigo.getY()), inimigo.get_tipo_aura())
                for inimigo in self.quartel.fantasmas
            ])
            posicoes_fantasmas = np.atleast_2d(posicoes_fantasmas)

            distancias = np.sqrt((personagem.getX() - posicoes_fantasmas[:, 0])**2 + (personagem.getY() - posicoes_fantasmas[:, 1])**2)

            idx_fantasma_perto = np.argmin(distancias)

            if distancias[idx_fantasma_perto] <= ConfigJogo.RAIO_AURA:
                aura_fantasma_perto = posicoes_fantasmas[idx_fantasma_perto, 2]

                if not personagem.cd_atualizado or personagem.tipo_fantasma_perto != aura_fantasma_perto:
                    self.atualiza_cd(personagem, aura_fantasma_perto)

            else:
                personagem.cd_atualizado = False
                personagem.cd = ConfigJogo.CD_PERSONAGEM
                personagem.duracao_bomba = ConfigJogo.DURACAO_BOMBA

    def atualiza_cd(self, personagem: Personagem, aura_fantasma_perto: int):
        if aura_fantasma_perto == 0:
            personagem.cd = ConfigJogo.CD_AURA_RAPIDA
            personagem.duracao_bomba = ConfigJogo.DURACAO_BOMBA_RAPIDA
        elif aura_fantasma_perto == 1:
            personagem.cd = ConfigJogo.CD_AURA_LENTA
            personagem.duracao_bomba = ConfigJogo.DURACAO_BOMBA_LENTA
        personagem.cd_atualizado = True
        personagem.tipo_fantasma_perto = aura_fantasma_perto
                
    def rodar(self):
        while not self.encerrada:
            self.mapa.desenha(self.tela)

            for bomba in self.p1.bombas:
                bomba.desenha(self.tela, self.mapa, self.bombas, self.p1.colisao, self.p1.colisao)
            if self.p2:
                for bomba in self.p2.bombas:
                    bomba.desenha(self.tela, self.mapa, self.bombas, self.p1.colisao, self.p2.colisao)
            
            self.p1.desenha()
            if self.p2:
                self.p2.desenha()

            self.quartel.desenha(self.bombas)
            self.quartel.tratamento_eventos(self.bombas)
            self.tratamento_eventos()
            self.desenha_menu()
       
            pygame.display.flip()

    def tratamento_eventos(self):
        if self.quartel.getVida() == 0:
            self.derrota = False
            self.encerrada = True
            time.sleep(1)
            return
        if not self.p2:
            if self.p1.morto:
                self.encerrada = True
                time.sleep(1)
                return          
        elif self.p1.morto and self.p2.morto or self.quartel.getVida() == 0 or self.cronometro.tempo_passado() > ConfigJogo.DURACAO_JOGO:
            self.encerrada = True
            time.sleep(1)
            return
        self.inimigos = self.quartel.getInimigos()
        tempo = time.time()
        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.p1.soltar_bomba(self.bombas, 1)
                if event.key == pygame.K_0 and self.p2:
                    self.p2.soltar_bomba(self.bombas, 2)

        if self.p1:
            if self.p1.morto:
                self.p1.setX(-100)
                self.p1.setY(-100)
            else:
                self.verifica_aura(self.p1)
                if tempo - self.p1._time_last_move > self.p1.cd:
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
                        if (self.p1.getY()%ConfigJogo.TAM_TILE)<15 and (self.p1.getY()%ConfigJogo.TAM_TILE)!=0 and self.p1.getMapa().destrutivel(self.p1.getX()-1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p1.getY()%ConfigJogo.TAM_TILE)>17 and self.p1.getMapa().destrutivel(self.p1.getX()-1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p1x, new_p1y):
                                self.p1.colisao_quartel = True
                            else:
                                self.p1.colisao_quartel = False
                                        
                    if pygame.key.get_pressed()[pygame.K_d]:
                        if (self.p1.getY()%ConfigJogo.TAM_TILE)<15 and (self.p1.getY()%ConfigJogo.TAM_TILE)!=0 and self.p1.getMapa().destrutivel(self.p1.getX()+ConfigJogo.TAM_TILE+1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p1.getY()%ConfigJogo.TAM_TILE)>17 and self.p1.getMapa().destrutivel(self.p1.getX()+ConfigJogo.TAM_TILE+1, self.p1.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p1x + ConfigJogo.TAM_TILE, new_p1y):
                                self.p1.colisao_quartel = True
                            else:
                                self.p1.colisao_quartel = False
                                
                    if pygame.key.get_pressed()[pygame.K_s]:
                        if (self.p1.getX()%ConfigJogo.TAM_TILE)<15 and (self.p1.getX()%ConfigJogo.TAM_TILE)!=0 and self.p1.getMapa().destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()+ConfigJogo.TAM_TILE+1)==TileType.GRAMA.value:
                            new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p1.getX()%ConfigJogo.TAM_TILE)>17 and self.p1.getMapa().destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()+ConfigJogo.TAM_TILE+1)==TileType.GRAMA.value:
                            new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p1y = self.p1.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p1x, new_p1y + ConfigJogo.TAM_TILE):
                                self.p1.colisao_quartel = True
                            else:
                                self.p1.colisao_quartel = False

                    if pygame.key.get_pressed()[pygame.K_w]:
                        if (self.p1.getX()%ConfigJogo.TAM_TILE)<15 and (self.p1.getX()%ConfigJogo.TAM_TILE)!=0 and self.p1.getMapa().destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()-1)==TileType.GRAMA.value:
                            new_p1x = self.p1.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p1.getX()%ConfigJogo.TAM_TILE)>17 and self.p1.getMapa().destrutivel(self.p1.getX()+int(ConfigJogo.TAM_TILE/2), self.p1.getY()-1)==TileType.GRAMA.value:
                            new_p1x = self.p1.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p1y = self.p1.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p1x, new_p1y):
                                self.p1.colisao_quartel = True
                            else:
                                self.p1.colisao_quartel = False
                    
                    #COLISAO COM PERSONAGEM E PROJETIL OU PERSONAGEM E INIMIGO
                    for inimigo in self.inimigos:
                        if self.p1.colisao.colliderect(inimigo.colisao):
                            if time.time() - self.p1.time_inalvejavel > 5:
                                self.p1.set_vida(self.p1.get_vida() - 1)
                                if self.p1.get_vida() == 0:
                                    self.p1.morto = True
                                    return
                                else:
                                    new_p1x = ConfigJogo.TAM_TILE
                                    new_p1y = ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU
                                    self.p1.time_inalvejavel=time.time()
                        if type(inimigo) == Alienigena:
                            for projetil in inimigo.projeteis:
                                if self.p1.colisao.colliderect(projetil.colisao):
                                    projetil.colidido = True
                                    inimigo.projeteis.remove(projetil)
                                    if time.time() - self.p1.time_inalvejavel > 5:
                                        self.p1.set_vida(self.p1.get_vida() - 1)
                                        if self.p1.get_vida() == 0:
                                            self.p1.morto = True
                                            return
                                        else:
                                            new_p1x = ConfigJogo.TAM_TILE
                                            new_p1y = ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU
                                            self.p1.time_inalvejavel=time.time()
                                
                    if not self.p1.getMapa().is_any_wall(new_p1x, new_p1y) and not self.p1.colisao_quartel:

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
                                                self.p1.set_vida(self.p1.get_vida() - 1)
                                                if self.p1.get_vida() == 0:
                                                    self.p1.morto = True
                                                    return
                                                else:
                                                    new_p1x = ConfigJogo.TAM_TILE
                                                    new_p1y = ConfigJogo.TAM_TILE + ConfigJogo.ALTURA_MENU
                                                    self.p1.time_inalvejavel=time.time()

                        if not bombaColisao:
                            self.p1.setX(new_p1x)
                            self.p1.setY(new_p1y)
                            self.p1.colisao = self.p1.personagem.get_rect(topleft=(new_p1x, new_p1y))

                            self.p1._time_last_move = time.time()

        if self.p2:
            if self.p2.morto:
                self.p2.setX(-100)
                self.p2.setY(-100)
            else:
                self.verifica_aura(self.p2)
                if tempo - self.p2._time_last_move > self.p2.cd: 
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
                        if (self.p2.getY()%ConfigJogo.TAM_TILE)<15 and (self.p2.getY()%ConfigJogo.TAM_TILE)!=0 and self.p2.getMapa().destrutivel(self.p2.getX()-1, self.p2.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p2y = self.p2.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p2.getY()%ConfigJogo.TAM_TILE)>17 and self.p2.getMapa().destrutivel(self.p2.getX()-1, self.p2.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p2y = self.p2.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p2x = self.p2.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p2x, new_p2y):
                                self.p2.colisao_quartel = True
                            else:
                                self.p2.colisao_quartel = False
                                        
                    if pygame.key.get_pressed()[pygame.K_RIGHT]:
                        if (self.p2.getY()%ConfigJogo.TAM_TILE)<15 and (self.p2.getY()%ConfigJogo.TAM_TILE)!=0 and self.p2.getMapa().destrutivel(self.p2.getX()+ConfigJogo.TAM_TILE+1, self.p2.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p2y = self.p2.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p2.getY()%ConfigJogo.TAM_TILE)>17 and self.p2.getMapa().destrutivel(self.p2.getX()+ConfigJogo.TAM_TILE+1, self.p2.getY()+int(ConfigJogo.TAM_TILE/2))==TileType.GRAMA.value:
                            new_p2y = self.p2.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p2x = self.p2.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p2x + ConfigJogo.TAM_TILE, new_p2y):
                                self.p2.colisao_quartel = True
                            else:
                                self.p2.colisao_quartel = False
                                
                    if pygame.key.get_pressed()[pygame.K_DOWN]:
                        if (self.p2.getX()%ConfigJogo.TAM_TILE)<15 and (self.p2.getX()%ConfigJogo.TAM_TILE)!=0 and self.p2.getMapa().destrutivel(self.p2.getX()+int(ConfigJogo.TAM_TILE/2), self.p2.getY()+ConfigJogo.TAM_TILE+1)==TileType.GRAMA.value:
                            new_p2x = self.p2.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p2.getX()%ConfigJogo.TAM_TILE)>17 and self.p2.getMapa().destrutivel(self.p2.getX()+int(ConfigJogo.TAM_TILE/2), self.p2.getY()+ConfigJogo.TAM_TILE+1)==TileType.GRAMA.value:
                            new_p2x = self.p2.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p2y = self.p2.getY() + ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p2x, new_p2y + ConfigJogo.TAM_TILE):
                                self.p2.colisao_quartel = True
                            else:
                                self.p2.colisao_quartel = False

                    if pygame.key.get_pressed()[pygame.K_UP]:
                        if (self.p2.getX()%ConfigJogo.TAM_TILE)<15 and (self.p2.getX()%ConfigJogo.TAM_TILE)!=0 and self.p2.getMapa().destrutivel(self.p2.getX()+int(ConfigJogo.TAM_TILE/2), self.p2.getY()-1)==TileType.GRAMA.value:
                            new_p2x = self.p2.getX() - ConfigJogo.VELOCIDADE_PERSONAGEM
                        elif (self.p2.getX()%ConfigJogo.TAM_TILE)>17 and self.p2.getMapa().destrutivel(self.p2.getX()+int(ConfigJogo.TAM_TILE/2), self.p2.getY()-1)==TileType.GRAMA.value:
                            new_p2x = self.p2.getX() + ConfigJogo.VELOCIDADE_PERSONAGEM
                        else:
                            new_p2y = self.p2.getY() - ConfigJogo.VELOCIDADE_PERSONAGEM
                            if self.quartel.quartel_colisao(new_p2x, new_p2y):
                                self.p2.colisao_quartel = True
                            else:
                                self.p2.colisao_quartel = False
                    
                    #COLISAO COM PERSONAGEM E PROJETIL
                    for inimigo in self.inimigos:
                        if self.p2.colisao.colliderect(inimigo.colisao):
                            if time.time() - self.p2.time_inalvejavel > 5:
                                self.p2.set_vida(self.p2.get_vida() - 1)
                                if self.p2.get_vida() == 0:
                                    self.p2.morto = True
                                    return
                                else:
                                    new_p2x = ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE
                                    new_p2y = ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE
                                    self.p2.time_inalvejavel=time.time()
                        if type(inimigo) == Alienigena:
                            for projetil in inimigo.projeteis:
                                if self.p2.colisao.colliderect(projetil.colisao):
                                    projetil.colidido = True
                                    inimigo.projeteis.remove(projetil)
                                    if time.time() - self.p2.time_inalvejavel > 5:
                                        self.p2.set_vida(self.p2.get_vida() - 1)
                                        if self.p2.get_vida() == 0:
                                            self.p2.morto = True
                                            return
                                        else:
                                            new_p2x = ConfigJogo.LARGURA_TELA - 2*ConfigJogo.TAM_TILE
                                            new_p2y = ConfigJogo.ALTURA_TELA - 2*ConfigJogo.TAM_TILE
                                            self.p2.time_inalvejavel=time.time()

                    if not self.p2.getMapa().is_any_wall(new_p2x, new_p2y) and not self.p2.colisao_quartel:
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
                                                self.p2.set_vida(self.p2.get_vida() - 1)
                                                if self.p2.get_vida() == 0:
                                                    self.p2.morto = True
                                                    return
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

            mostra_pont_p1 = fonte_hud.render(f'{self.p1.get_pontos()}', True, ConfigJogo.COR_FONTE_HUD)
            self.tela.blit(mostra_pont_p1, (ConfigJogo.LARGURA_TELA * .57, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            self.tela.blit(self.img_relogio, (ConfigJogo.LARGURA_TELA * .05, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            
        
        else:
            mostra_pont_p1 = fonte_hud.render(f'{self.p1.get_pontos()}', True, ConfigJogo.COR_FONTE_HUD)
            mostra_pont_p2 = fonte_hud.render(f'{self.p2.get_pontos()}', True, ConfigJogo.COR_FONTE_HUD)

            self.tela.blit(mostra_pont_p1, (ConfigJogo.LARGURA_TELA * .57, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            self.tela.blit(mostra_pont_p2, (ConfigJogo.LARGURA_TELA * .82, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

            self.tela.blit(self.p1.personagem, (ConfigJogo.LARGURA_TELA * .5, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))
            self.tela.blit(self.p2.personagem, (ConfigJogo.LARGURA_TELA * .75, ConfigJogo.ALTURA_MENU * .5 - ConfigJogo.TAM_TILE * .5))

