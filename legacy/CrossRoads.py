import pygame
import random
import sys
import os  # Necessário para a função de caminho

# Inicializar o Pygame
pygame.init()


# ----------------------------------------------------
# Função para Corrigir o Caminho de Assets no PyInstaller
# ----------------------------------------------------
def resource_path(relative_path):
    """Obtém o caminho absoluto para o asset, independente de ser executável ou script."""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Modo normal (quando rodando com 'python script.py')
        base_path = os.path.abspath(".")

    # Combina o caminho base com o nome do arquivo
    return os.path.join(base_path, relative_path)


# ----------------------------------------------------

# --- Inicialização e Carregamento de Áudio ---
MUSICA_FUNDO = 'musica_fundo.mp3'
SOM_COLISAO = 'som_colisao.wav'
SOM_PONTO = 'som_ponto.OGG'
SOM_GAME_OVER = 'som_game_over.wav'
SOM_VITORIA = 'som_vitoria.wav'
SOM_ITEM = 'som_item.wav'

try:
    pygame.mixer.init()
    # Carregamento DOS EFEITOS SONOROS (usando resource_path)
    SOM_COLISAO = pygame.mixer.Sound(resource_path(SOM_COLISAO))
    SOM_PONTO = pygame.mixer.Sound(resource_path(SOM_PONTO))
    SOM_GAME_OVER = pygame.mixer.Sound(resource_path(SOM_GAME_OVER))
    SOM_VITORIA = pygame.mixer.Sound(resource_path(SOM_VITORIA))
    SOM_ITEM = pygame.mixer.Sound(resource_path(SOM_ITEM))

    # Ajustar volume
    SOM_COLISAO.set_volume(0.5)
    SOM_PONTO.set_volume(0.3)
    SOM_VITORIA.set_volume(0.5)
    SOM_ITEM.set_volume(0.5)

    AUDIO_DISPONIVEL = True
except pygame.error as e:
    print(f"ATENÇÃO: Erro ao carregar áudio. Arquivos faltando ou problema no Mixer: {e}")


    class DummySound:
        def play(self, *args, **kwargs): pass

        def set_volume(self, *args, **kwargs): pass


    SOM_COLISAO = DummySound()
    SOM_PONTO = DummySound()
    SOM_GAME_OVER = DummySound()
    SOM_VITORIA = DummySound()
    SOM_ITEM = DummySound()
    MUSICA_FUNDO = None
    AUDIO_DISPONIVEL = False

# Configurações da tela
LARGURA = 1000
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Crossy Road Python")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_GRAMA = (0, 150, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
AMARELO_LINHA = (255, 255, 0)
CINZA_ESTRADA = (50, 50, 50)
ROSA = (255, 0, 128)
VERDE_ITEM = (0, 255, 0)

# --- CONSTANTES DE LAYOUT E POSIÇÃO ---
ALTURA_FAIXA_ESTRADA = 60
ALTURA_FAIXA_GRAMA = 60
ALTURA_FAIXA_EXTREMA = 80

FAIXAS_LAYOUT = [
    (ALTURA_FAIXA_EXTREMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA),
    (ALTURA_FAIXA_GRAMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA),
    (ALTURA_FAIXA_GRAMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA),
    (ALTURA_FAIXA_GRAMA, VERDE_GRAMA),
    (ALTURA_FAIXA_ESTRADA, CINZA_ESTRADA),
    (ALTURA_FAIXA_EXTREMA, VERDE_GRAMA),
]

POSICOES_Y = []
y_acumulado = 0
for altura, cor in FAIXAS_LAYOUT:
    POSICOES_Y.append(y_acumulado)
    y_acumulado += altura

FAIXAS_VEICULOS_Y = [POSICOES_Y[1], POSICOES_Y[3], POSICOES_Y[5], POSICOES_Y[7]]

POSICAO_CHEGADA = POSICOES_Y[0]
POSICAO_SPAWN_CENTER_Y = POSICOES_Y[8] + ALTURA_FAIXA_EXTREMA // 2

# --- CONSTANTES GERAIS E DIFICULDADE ---
VELOCIDADE_CARRO_BASE = 6.0
VELOCIDADE_ONIBUS_BASE = 4.0
ESPACO_MINIMO_LIVRE = 50
FATOR_DIFICULDADE = 0.0

# Relógio e Fonte
clock = pygame.time.Clock()
FPS = 60
fonte = pygame.font.SysFont(None, 36)


# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERMELHO)
        self.resetar_posicao()
        self.velocidade = 5
        self.invulneravel = False
        self.tempo_invulneravel = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade

        if self.invulneravel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_invulneravel > 1000: #1 segundo de invulnerabilidade
                self.invulneravel = False
                self.image.fill(VERMELHO)

            if (tempo_atual // 200) % 2 == 0:
                self.image.fill(AZUL)
            else:
                self.image.fill(VERMELHO)
        else:
            self.image.fill(VERMELHO)

    def tornar_invulneravel(self):
        self.invulneravel = True
        self.tempo_invulneravel = pygame.time.get_ticks()

    def resetar_posicao(self):
        self.rect = self.image.get_rect(center=(LARGURA // 2, POSICAO_SPAWN_CENTER_Y))
        self.faixa_atual = len(FAIXAS_VEICULOS_Y)


# --- CLASSE BASE DE VEÍCULOS ---
class Veiculo(pygame.sprite.Sprite):
    def __init__(self, x, y_faixa, largura, altura, cor, velocidade, direcao):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(cor)
        self.velocidade = velocidade
        self.direcao = direcao
        self.largura = largura

        y_centralizado = y_faixa + (ALTURA_FAIXA_ESTRADA - altura) // 2
        self.rect = self.image.get_rect(topleft=(x, y_centralizado))

    def update(self):
        self.rect.x += self.velocidade * self.direcao

        if self.direcao == 1 and self.rect.left > LARGURA:
            self.rect.right = 0
        elif self.direcao == -1 and self.rect.right < 0:
            self.rect.left = LARGURA


class Carro(Veiculo):
    def __init__(self, x, y_faixa, direcao, fator_dificuldade):
        largura, altura = 50, 30
        velocidade_ajustada = VELOCIDADE_CARRO_BASE + fator_dificuldade
        velocidade = velocidade_ajustada + random.uniform(-0.5, 0.5)
        super().__init__(x, y_faixa, largura, altura, AZUL, velocidade, direcao)
        self.image.fill(AZUL)
        pygame.draw.rect(self.image, PRETO, (0, 0, 10, altura))
        pygame.draw.rect(self.image, PRETO, (largura - 10, 0, 10, altura))
        pygame.draw.rect(self.image, CINZA_ESTRADA, (15, 5, 20, 20))


class Onibus(Veiculo):
    def __init__(self, x, y_faixa, direcao, fator_dificuldade):
        largura, altura = 70, 35
        velocidade_ajustada = VELOCIDADE_ONIBUS_BASE + (fator_dificuldade * 0.5)
        velocidade = velocidade_ajustada + random.uniform(-0.5, 0.5)
        super().__init__(x, y_faixa, largura, altura, AMARELO_LINHA, velocidade, direcao)
        self.image.fill(AMARELO_LINHA)
        for i in range(5):
            pygame.draw.rect(self.image, PRETO, (10 + i * 12, 5, 8, altura - 10))
        pygame.draw.rect(self.image, CINZA_ESTRADA, (5, 15, 5, 10))


# --- CLASSE OBSTÁCULO ESTÁTICO (Árvores) ---
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y_faixa, altura_faixa):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERDE_GRAMA)
        self.image.set_colorkey(VERDE_GRAMA)
        pygame.draw.circle(self.image, (0, 100, 0), (15, 15), 15)
        pygame.draw.rect(self.image, (139, 69, 19), (12, 20, 6, 10))

        altura_hitbox = 30
        y_hitbox_centralizado = y_faixa + (altura_faixa - altura_hitbox) // 2

        self.rect = self.image.get_rect(topleft=(x, y_hitbox_centralizado))

    def update(self):
        pass


# --- CLASSE ITEM BÔNUS ---
class ItemBonus(pygame.sprite.Sprite):
    def __init__(self, x, y_faixa, altura_faixa, tipo):
        super().__init__()
        self.tipo = tipo
        self.image = pygame.Surface((25, 25))
        self.image.set_colorkey(PRETO)

        if self.tipo == 'vida':
            self.cor = ROSA
            pygame.draw.circle(self.image, self.cor, (8, 8), 8)
            pygame.draw.circle(self.image, self.cor, (17, 8), 8)
            pygame.draw.polygon(self.image, self.cor, [(0, 10), (25, 10), (12.5, 25)])

        elif self.tipo == 'escudo':
            self.cor = AZUL
            pygame.draw.circle(self.image, self.cor, (12, 12), 12)
            pygame.draw.rect(self.image, BRANCO, (8, 8, 8, 8))

        altura_hitbox = 25
        y_hitbox_centralizado = y_faixa + (altura_faixa - altura_hitbox) // 2
        self.rect = self.image.get_rect(topleft=(x, y_hitbox_centralizado))

    def update(self):
        pass


# Função para desenhar as vidas na tela
def desenhar_vidas(tela, x, y, vidas):
    for i in range(vidas):
        x_diamond = x + i * 40 + 15
        y_diamond = y + 15

        pygame.draw.polygon(tela, ROSA, [
            (x_diamond, y_diamond - 15),
            (x_diamond + 15, y_diamond),
            (x_diamond, y_diamond + 15),
            (x_diamond - 15, y_diamond)
        ])


# Lógica de Geração de Veículos
def gerar_veiculos(fator_dificuldade):
    veiculos = pygame.sprite.Group()

    for i, y_faixa in enumerate(FAIXAS_VEICULOS_Y):
        if random.random() < 0.5:
            TipoVeiculo = Carro
            largura_veiculo = 50
        else:
            TipoVeiculo = Onibus
            largura_veiculo = 70

        direcao = random.choice([-1, 1])
        num_veiculos = i + 1

        largura_total_veiculos = num_veiculos * largura_veiculo
        espaco_vazio_total_necessario = num_veiculos * ESPACO_MINIMO_LIVRE
        circuito_largura_total = largura_total_veiculos + espaco_vazio_total_necessario
        distancia_entre_veiculos = largura_veiculo + ESPACO_MINIMO_LIVRE

        for j in range(num_veiculos):
            if direcao == 1:
                x_inicial = -circuito_largura_total + (j * distancia_entre_veiculos)
            else:
                x_inicial = LARGURA + circuito_largura_total - (j * distancia_entre_veiculos)

            veiculo = TipoVeiculo(x_inicial, y_faixa, direcao, fator_dificuldade)
            veiculos.add(veiculo)

    return veiculos


# Função para a tela de Fim de Jogo/Vitória e Reinício
def tela_final(vitoria, pontuacao, fator_dificuldade_atual):
    aguardando_reiniciar = True
    while aguardando_reiniciar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if vitoria:
                    if event.key == pygame.K_r:
                        return True
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_r:
                        return "RESTART"
                    elif event.key == pygame.K_c:
                        return "CONTINUE"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

        TELA.fill(VERDE_GRAMA)

        if vitoria:
            texto_principal = fonte.render("VITÓRIA!", True, AZUL)
            texto_secundario = fonte.render("Você atravessou a rua!", True, PRETO)
            texto_opcoes = fonte.render("Pressione R para Próximo Nível ou Q para Sair", True, CINZA_ESTRADA)
        else:
            texto_principal = fonte.render("Game Over!", True, VERMELHO)
            nivel = int(fator_dificuldade_atual * 2) + 1
            texto_secundario = fonte.render(f"Nível Alcançado: {nivel}", True, PRETO)
            texto_opcoes = fonte.render("R: Reiniciar Nível 1 | C: Continuar Nível Atual | Q: Sair", True,
                                        CINZA_ESTRADA)

        texto_pontuacao = fonte.render(f"Pontuação Final: {pontuacao}", True, PRETO)

        TELA.blit(texto_principal, (LARGURA // 2 - texto_principal.get_width() // 2, ALTURA // 2 - 90))
        TELA.blit(texto_secundario, (LARGURA // 2 - texto_secundario.get_width() // 2, ALTURA // 2 - 30))
        TELA.blit(texto_pontuacao, (LARGURA // 2 - texto_pontuacao.get_width() // 2, ALTURA // 2 + 30))
        TELA.blit(texto_opcoes, (LARGURA // 2 - texto_opcoes.get_width() // 2, ALTURA // 2 + 100))

        pygame.display.flip()
        clock.tick(10)

    return False


# Função principal do Jogo
def jogo(fator_dificuldade):
    # Grupos de sprites
    todos_sprites = pygame.sprite.Group()
    veiculos = pygame.sprite.Group()
    obstaculos = pygame.sprite.Group()
    itens_bonus = pygame.sprite.Group()

    jogador = Jogador()
    todos_sprites.add(jogador)

    veiculos = gerar_veiculos(fator_dificuldade)
    todos_sprites.add(veiculos)

    # --- GERAÇÃO DE OBSTÁCULOS ESTÁTICOS ---
    faixas_grama_indices = [0, 2, 4, 6, 8]

    for i in faixas_grama_indices:
        y_faixa = POSICOES_Y[i]
        altura_faixa = FAIXAS_LAYOUT[i][0]

        num_obstaculos_por_faixa = random.randint(2, 4) if i not in [0, 8] else random.randint(1, 2)

        for _ in range(num_obstaculos_por_faixa):
            x = random.randint(5, LARGURA - 30 - 5)
            arvore = Obstaculo(x, y_faixa, altura_faixa)
            if i == 8 and abs(x - jogador.rect.centerx) < 60:
                continue
            colisoes_iniciais = pygame.sprite.spritecollide(arvore, obstaculos, False)
            if not colisoes_iniciais:
                obstaculos.add(arvore)
                todos_sprites.add(arvore)

                # --- GERAÇÃO DE ITENS BÔNUS ---
    faixas_grama_intermed = [2, 4, 6]

    for i in faixas_grama_intermed:
        y_faixa = POSICOES_Y[i]
        altura_faixa = FAIXAS_LAYOUT[i][0]

        if random.random() < 0.2: # 20% de chance de gerar um item bônus
            x = random.randint(30, LARGURA - 30)
            tipo_item = random.choice(['vida', 'escudo'])

            item = ItemBonus(x, y_faixa, altura_faixa, tipo_item)

            colisoes_obstaculo = pygame.sprite.spritecollide(item, obstaculos, False)
            if not colisoes_obstaculo:
                itens_bonus.add(item)
                todos_sprites.add(item)
    # ------------------------------------

    # Sistema de vidas e pontuação
    vidas = 3
    pontuacao = 0
    pontuacao_faixa = 10

    executando = True
    while executando:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executando = False

        # --- ATUALIZAÇÃO DE POSIÇÃO ---
        jogador.update()
        veiculos.update()

        # Colisão com Obstáculos Estáticos
        colisoes_obstaculo = pygame.sprite.spritecollide(jogador, obstaculos, False)
        if colisoes_obstaculo:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: jogador.rect.x += jogador.velocidade
            if keys[pygame.K_RIGHT]: jogador.rect.x -= jogador.velocidade
            if keys[pygame.K_UP]: jogador.rect.y += jogador.velocidade
            if keys[pygame.K_DOWN]: jogador.rect.y -= jogador.velocidade

        # --- Colisão com Itens Bônus ---
        colisoes_item = pygame.sprite.spritecollide(jogador, itens_bonus, True)
        for item in colisoes_item:
            if AUDIO_DISPONIVEL: SOM_ITEM.play()

            if item.tipo == 'vida':
                if vidas < 5:
                    vidas += 1
            elif item.tipo == 'escudo':
                jogador.tornar_invulneravel()
        # ------------------------------------

        # Lógica de Pontuação e Chegada
        vitoria = False

        if jogador.faixa_atual > 0:
            y_da_faixa_alvo = FAIXAS_VEICULOS_Y[jogador.faixa_atual - 1]
        else:
            y_da_faixa_alvo = POSICAO_CHEGADA

        if jogador.rect.top < y_da_faixa_alvo:
            if jogador.faixa_atual > 0:
                pontuacao += pontuacao_faixa
                jogador.faixa_atual -= 1
                if AUDIO_DISPONIVEL: SOM_PONTO.play()

            if jogador.faixa_atual == 0:
                executando = False
                vitoria = True
                if AUDIO_DISPONIVEL: SOM_VITORIA.play()

                # Colisões com Veículos
        if pygame.sprite.spritecollide(jogador, veiculos, False) and not jogador.invulneravel:
            vidas -= 1
            if vidas <= 0:
                executando = False
                vitoria = False
                if AUDIO_DISPONIVEL: SOM_GAME_OVER.play()
            else:
                jogador.tornar_invulneravel()
                jogador.resetar_posicao()
                if AUDIO_DISPONIVEL: SOM_COLISAO.play()

        # --- DESENHO DO MAPA ---
        TELA.fill(VERDE_GRAMA)

        y_atual = 0
        for i, (altura, cor) in enumerate(FAIXAS_LAYOUT):
            pygame.draw.rect(TELA, cor, (0, y_atual, LARGURA, altura))

            if cor == CINZA_ESTRADA:
                y_linha = y_atual + altura // 2 - 2
                for j in range(0, LARGURA, 40):
                    pygame.draw.rect(TELA, AMARELO_LINHA, (j, y_linha, 20, 5))

            y_atual += altura

        pygame.draw.rect(TELA, AMARELO_LINHA, (0, POSICAO_CHEGADA, LARGURA, 5))

        todos_sprites.draw(TELA)

        # Mostrar HUD
        texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, PRETO)
        texto_dificuldade = fonte.render(f"Nível: {int(fator_dificuldade * 2) + 1}", True, PRETO)
        TELA.blit(texto_pontos, (10, 10))
        TELA.blit(texto_dificuldade, (10, 40))

        desenhar_vidas(TELA, LARGURA - 120, 10, vidas)

        pygame.display.flip()
        clock.tick(FPS)

    return tela_final(vitoria, pontuacao, fator_dificuldade)


# Função principal que gerencia o loop de reinício
def main():
    global FATOR_DIFICULDADE
    rodando = True

    if MUSICA_FUNDO and AUDIO_DISPONIVEL:
        try:
            # Importante: Usa resource_path ao carregar a música
            pygame.mixer.music.load(resource_path(MUSICA_FUNDO))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Erro ao tocar música: {e}")

    while rodando:
        resultado_final = jogo(FATOR_DIFICULDADE)

        if resultado_final is True:
            FATOR_DIFICULDADE += 0.5

        elif resultado_final == "RESTART":
            FATOR_DIFICULDADE = 0.0

        elif resultado_final == "CONTINUE":
            pass

        else:
            rodando = False

    pygame.quit()
    sys.exit()


# Iniciar o jogo
if __name__ == "__main__":
    main()