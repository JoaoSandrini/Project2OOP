class ConfigJogo:

    INIMIGOS = True
    TAM_TILE = 32
    ALTURA_MENU = 2*TAM_TILE
    LARGURA_TELA = TAM_TILE*20
    ALTURA_TELA = TAM_TILE*15 + ALTURA_MENU
    FONTE_SUBTITULO = 36
    COR_SUBTITULO = (255, 255, 255)
    COR_INICIO = (0, 0, 0)
    LARGURA_LOGO = LARGURA_TELA*.555
    ALTURA_LOGO = ALTURA_TELA*.453
    ESPACO_SUBTITULO = 1.3
    VELOCIDADE_PERSONAGEM = 1
    DURACAO_BOMBA = 2
    ALCANCE_BOMBA = 5
    MAX_BOMBA = 4
    DURACAO_JOGO = 120
    FONTE_HUD = 50
    COR_FONTE_HUD = (255, 255, 255)
    VELOCIDADE_FANTASMA = 1
    CD_FANTASMA = 0.01
    CD_PERSONAGEM = 0.01
    COR_AURA = (128, 128, 128, 128)
    RAIO_AURA = TAM_TILE * 3 + TAM_TILE/2
    CD_ALIEN = 0.01
    CD_SHOT_ALIEN = 2
    CD_SHOT_MOVE = 0.01
    VELOCIDADE_ALIEN = 1
    LARGURA_PROJETIL = TAM_TILE
    ALTURA_PROJETIL = 5
    VELOCIDADE_PROJETIL = 3
    BUFFER = 5
    QUARTEL_X = 288
    QUARTEL_Y = ALTURA_MENU + 224
    COR_HUD = (0, 0, 100)
    COR_BORDA_HUD = (0, 255, 0)
    VIDA_QUARTEL = 2
    ESPESSURA_AURA = 5
    VIDA_PERSONAGEM = 3
    VIDA_INIMIGO = 1
    ORIGEM = (0, 0)
    CD_AURA_RAPIDA = CD_PERSONAGEM / 3
    CD_AURA_LENTA = CD_PERSONAGEM * 3
    MAX_INIMIGOS = 10
    CD_SPAWN = 1
    DURACAO_BOMBA_LENTA = DURACAO_BOMBA * 3
    DURACAO_BOMBA_RAPIDA = DURACAO_BOMBA / 3
    PONTUACAO_BLOCO = 1
    PONTUACAO_INIMIGO = 10
    PONTUACAO_QUARTEL = 100
    CD_TEXTO = 0.35
    