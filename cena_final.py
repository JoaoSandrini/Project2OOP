from personagem import Personagem
from config_jogo import ConfigJogo
import sys
from cronometro import Cronometro
import pygame

class CenaFinal():
    def __init__(self, tela: pygame.Surface, p1: Personagem, p2: Personagem, derrota: bool) -> None:
        self.cronometro = Cronometro()
        self.tela = tela
        self.p1 = p1
        self.img_p1 = self.p1.personagem
        self.derrota = derrota
        if p2:
            self.p2 = p2 
            self.img_p2 = self.p2.personagem
        else:
            self.p2 = False
        self.pontos_p1 = self.p1.get_pontos()
        self.pontos_p2 = self.p2.get_pontos() if p2 else 0
        self.tela = tela
        self.encerrada = False
        self.mostrar_texto = True
        fonte = pygame.font.SysFont(None, ConfigJogo.FONTE_SUBTITULO)
        self.textos = [fonte.render(f'Derrota', True, ConfigJogo.COR_SUBTITULO), #0
                       fonte.render(f'Vitória', True, ConfigJogo.COR_SUBTITULO),  #1
                       fonte.render(f'Pressione ESC para sair', True, ConfigJogo.COR_SUBTITULO),    #2  
                       fonte.render(f'Pressione ESPAÇO para iniciar um novo jogo', True, ConfigJogo.COR_SUBTITULO), #3
                       fonte.render(f'{self.pontos_p1}', True, ConfigJogo.COR_SUBTITULO),   #4
                       fonte.render(f'{self.pontos_p2}', True, ConfigJogo.COR_SUBTITULO)]   #5

    def rodar(self):
        while not self.encerrada:
            self.atualiza_estado()
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

        if self.derrota:
            self.tela.blit(self.textos[0], ((ConfigJogo.LARGURA_TELA - self.textos[0].get_width()) // 2, py))
        else:
            self.tela.blit(self.textos[1], ((ConfigJogo.LARGURA_TELA - self.textos[1].get_width()) // 2, py))

        if self.p2:
            self.tela.blit(self.textos[4], ((ConfigJogo.LARGURA_TELA * 0.25) + ConfigJogo.TAM_TILE//2 - self.textos[4].get_width()//2, py + ConfigJogo.TAM_TILE * 4))
            self.tela.blit(self.textos[5], ((ConfigJogo.LARGURA_TELA * 0.75) + ConfigJogo.TAM_TILE//2 - self.textos[5].get_width()//2, py + ConfigJogo.TAM_TILE * 4))
            
            self.tela.blit(self.img_p1, ((ConfigJogo.LARGURA_TELA) * 0.25, py + ConfigJogo.TAM_TILE * 2))
            self.tela.blit(self.img_p2, ((ConfigJogo.LARGURA_TELA) * 0.75, py + ConfigJogo.TAM_TILE * 2))

        else:
            self.tela.blit(self.textos[5], ((ConfigJogo.LARGURA_TELA * 0.5) - self.textos[5].get_width()//2, py + ConfigJogo.TAM_TILE * 4))
            
            self.tela.blit(self.img_p1, (ConfigJogo.LARGURA_TELA * .5 - ConfigJogo.TAM_TILE*.5 , py + ConfigJogo.TAM_TILE * 2))
        if self.mostrar_texto:
            self.tela.blit(self.textos[2], ((ConfigJogo.LARGURA_TELA - self.textos[2].get_width()) // 2, ConfigJogo.ALTURA_TELA // 2))
            self.tela.blit(self.textos[3], ((ConfigJogo.LARGURA_TELA - self.textos[3].get_width()) // 2, (ConfigJogo.ALTURA_TELA // 2) + ConfigJogo.TAM_TILE))

        
                
    def atualiza_estado(self):
        if self.cronometro.tempo_passado() > ConfigJogo.CD_TEXTO:
            self.mostrar_texto = not self.mostrar_texto
            self.cronometro.reset()


