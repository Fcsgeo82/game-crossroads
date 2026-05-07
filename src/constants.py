import pygame

# Configurações da tela
LARGURA = 1000
ALTURA = 800
FPS = 60

# Cores Básicas
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
AMARELO_LINHA = (255, 255, 0)
ROSA = (255, 0, 128)
VERDE_ITEM = (0, 255, 0)
VERDE_GRAMA = (0, 150, 0)  # Marcador para Grama
CINZA_ESTRADA = (50, 50, 50) # Marcador para Estrada

# Definições das Estações
ESTACOES = {
    'PRIMAVERA': {
        'GRAMA': (34, 139, 34),    # Verde floresta
        'ESTRADA': (50, 50, 50),
        'ARVORE': 'Trees-1.png'
    },
    'VERAO': {
        'GRAMA': (0, 200, 0),      # Verde vibrante
        'ESTRADA': (70, 70, 70),   # Asfalto "quente"
        'ARVORE': 'Trees-1.png'
    },
    'OUTONO': {
        'GRAMA': (139, 69, 19),    # Marrom siena
        'ESTRADA': (40, 40, 40),
        'ARVORE': 'Trees-1.png'    # Poderíamos usar uma árvore laranja aqui
    },
    'INVERNO': {
        'GRAMA': (220, 220, 255),  # Branco gelo
        'ESTRADA': (30, 30, 40),   # Escuro azulado
        'ARVORE': 'Trees-1.png'    # Poderíamos usar uma árvore com neve aqui
    }
}

ORDEM_ESTACOES = ['PRIMAVERA', 'VERAO', 'OUTONO', 'INVERNO']

# Layout das faixas
ALTURA_FAIXA_ESTRADA = 65
ALTURA_FAIXA_GRAMA = 100
ALTURA_FAIXA_EXTREMA = 120

FAIXAS_LAYOUT = [
    (ALTURA_FAIXA_EXTREMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA), # Estrada 1 - Faixa 1
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA), # Estrada 1 - Faixa 2
    (ALTURA_FAIXA_GRAMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA), # Estrada 2 - Faixa 1
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA), # Estrada 2 - Faixa 2
    (ALTURA_FAIXA_GRAMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA), # Estrada 3 - Faixa 1
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA), # Estrada 3 - Faixa 2
    (ALTURA_FAIXA_EXTREMA, VERDE_GRAMA),
]

# Áudio
MUSICA_FUNDO = 'musica_fundo.mp3'
SOM_COLISAO = 'som_colisao.wav'
SOM_PONTO = 'som_ponto.OGG'
SOM_GAME_OVER = 'som_game_over.wav'
SOM_VITORIA = 'som_vitoria.wav'
SOM_ITEM = 'som_ponto.OGG' 

# Dificuldade e Velocidades
VELOCIDADE_CARRO_BASE = 6.0
VELOCIDADE_ONIBUS_BASE = 4.0
ESPACO_MINIMO_LIVRE = 50
