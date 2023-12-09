from personagem import Personagem
from config_jogo import ConfigJogo
import sys

import pygame

class CenaFinal():
    def __init__(self, tela: pygame.Surface, p1: Personagem, p2: Personagem) -> None:
        self.tela = tela
        self.p1 = p1
        if p2:
            self.p2 = p2 
        else:
            self.p2 = False
        self.pontos_p1 = self.p1.get_pontos()
        self.pontos_p2 = self.p2.get_pontos() if p2 else 0
        self.tela = tela
        self.encerrada = False
        fonte = pygame.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.textos = [fonte.render(f'Vitória Jogador 1', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'Vitória Jogador 2', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'Empate', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'Pressione ESC para sair', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'Pressione ESPAÇO para iniciar um novo jogo', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'Game Over', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'{self.pontos_p1}', True, ConfigJogo.COR_SUBTITULO), fonte.render(f'{self.pontos_p2}', True, ConfigJogo.COR_SUBTITULO)]

    def rodar(self):
        while not self.encerrada:
            self.tratamento_eventos()
            self.desenha()

    def tratamento_eventos(self):
        pygame.event.get()

        # evento de saida
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit(0)

        # evento de prosseguimento
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.encerrada = True
    
    def desenha(self):
        self.tela.fill(ConfigJogo.COR_INICIO)
        self.desenha_vencedor()
        pygame.display.flip()
    
    def desenha_vencedor(self):

        py = 0.2 * ConfigJogo.ALTURA_TELA // 2
        if self.p2:
            self.tela.blit(self.textos[6], ((ConfigJogo.LARGURA_TELA - self.textos[6].get_width()//2)*.25, py+ConfigJogo.TAM_TILE*2))
            self.tela.blit(self.textos[7], ((ConfigJogo.LARGURA_TELA - self.textos[7].get_width()//2)*.75, py+ConfigJogo.TAM_TILE*2))
            self.tela.blit(self.textos[5], ((ConfigJogo.LARGURA_TELA - self.textos[5].get_width())//2, py+ConfigJogo.TAM_TILE*4))
            if self.pontos_p1 > self.pontos_p2:
                self.img_vencedor = self.p1.personagem
                self.tela.blit(self.img_vencedor, (ConfigJogo.LARGURA_TELA//2, py))
                self.tela.blit(self.textos[0], ((ConfigJogo.LARGURA_TELA - self.textos[0].get_width())//2, py+ConfigJogo.TAM_TILE*2))

            elif self.pontos_p1 < self.pontos_p2:
                self.img_vencedor = self.p2.personagem
                self.tela.blit(self.img_vencedor, (ConfigJogo.LARGURA_TELA//2, py))
                self.tela.blit(self.textos[1], ((ConfigJogo.LARGURA_TELA - self.textos[1].get_width())//2, py+ConfigJogo.TAM_TILE*2))

            elif self.p2 and self.pontos_p1 == self.pontos_p2:
                self.img_empate1 = self.p1.personagem
                self.img_empate2 = self.p2.personagem
                self.tela.blit(self.img_empate1, ((ConfigJogo.LARGURA_TELA - ConfigJogo.TAM_TILE)*.25, py))
                self.tela.blit(self.img_empate2, ((ConfigJogo.LARGURA_TELA - ConfigJogo.TAM_TILE)*.75, py))
                self.tela.blit(self.textos[2], ((ConfigJogo.LARGURA_TELA - self.textos[2].get_width())//2, py+ConfigJogo.TAM_TILE*3))
        else:
            self.img_vencedor = self.p1.personagem
            self.tela.blit(self.img_vencedor, ((ConfigJogo.LARGURA_TELA - ConfigJogo.TAM_TILE)//2, py))
            self.tela.blit(self.textos[5], ((ConfigJogo.LARGURA_TELA - self.textos[5].get_width())//2, py+ConfigJogo.TAM_TILE*4))
            self.tela.blit(self.textos[6], ((ConfigJogo.LARGURA_TELA - self.textos[6].get_width())//2, py+ConfigJogo.TAM_TILE*2))

        self.tela.blit(self.textos[3], ((ConfigJogo.LARGURA_TELA - self.textos[3].get_width())//2, ConfigJogo.ALTURA_TELA//2))
        self.tela.blit(self.textos[4], ((ConfigJogo.LARGURA_TELA - self.textos[4].get_width())//2, (ConfigJogo.ALTURA_TELA//2) + ConfigJogo.TAM_TILE))

    



