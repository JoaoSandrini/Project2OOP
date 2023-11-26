from utils import ler_imagem
from config_jogo import ConfigJogo
class Quartel:
    def __init__(self):
        self.img_quartel = ler_imagem('enemies/ship.png', (ConfigJogo.TAM_TILE, ConfigJogo.TAM_TILE))
        self._x = ConfigJogo.QUARTEL_X
        self._y = ConfigJogo.QUARTEL_Y 
        self._vida = ConfigJogo.VIDA_QUARTEL

    def desenha(self, tela):
        tela.blit(self.img_quartel, (self._x, self._y))