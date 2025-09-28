import pygame
import random
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
LARGURA = 1000
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Crossy Road Python - Reiniciar")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
AMARELO = (200, 200, 0)
CINZA = (100, 100, 100)
CINZA_ESCURO = (50, 50, 50)
ROSA = (255, 0, 128)

# --- CONSTANTES GERAIS ---
VELOCIDADE_CARRO_BASE = 6.0
VELOCIDADE_ONIBUS_BASE = 4.0
ESPACO_MINIMO_LIVRE = 50

# Usei o incremento de 100 como exemplo para faixas mais espaçadas
INCREMENTO_Y = 100
FAIXAS_Y = [100, 100 + INCREMENTO_Y, 100 + 2 * INCREMENTO_Y, 100 + 3 * INCREMENTO_Y, 100 + 4 * INCREMENTO_Y]

# Se você usou o INCREMENTO_Y=80 (o valor original), FAIXAS_Y seria [100, 180, 260, 340, 420]

POSICAO_CHEGADA = FAIXAS_Y[0] - 80

# Relógio para controlar FPS
clock = pygame.time.Clock()
FPS = 60
fonte = pygame.font.SysFont(None, 36)


# Classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
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

        # Gerenciar tempo de invulnerabilidade
        if self.invulneravel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_invulneravel > 2000:
                self.invulneravel = False
                self.image.fill(VERMELHO)

            if (tempo_atual // 200) % 2 == 0:
                self.image.fill(ROSA)
            else:
                self.image.fill(VERMELHO)

    def tornar_invulneravel(self):
        self.invulneravel = True
        self.tempo_invulneravel = pygame.time.get_ticks()

    def resetar_posicao(self):
        self.rect = self.image.get_rect(center=(LARGURA // 2, ALTURA - 50))
        self.faixa_atual = len(FAIXAS_Y)


# Classes de Veículos (Carro e Onibus)

class Veiculo(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, cor, velocidade, direcao):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = velocidade
        self.direcao = direcao
        self.largura = largura

    def update(self):
        self.rect.x += self.velocidade * self.direcao

        if self.direcao == 1 and self.rect.left > LARGURA:
            self.rect.right = 0
        elif self.direcao == -1 and self.rect.right < 0:
            self.rect.left = LARGURA


class Carro(Veiculo):
    def __init__(self, x, y, direcao):
        velocidade = VELOCIDADE_CARRO_BASE + random.uniform(-0.5, 0.5)
        super().__init__(x, y, 50, 30, AZUL, velocidade, direcao)
        pygame.draw.rect(self.image, PRETO, (0, 0, 10, 30))
        pygame.draw.rect(self.image, PRETO, (40, 0, 10, 30))
        pygame.draw.rect(self.image, CINZA_ESCURO, (15, 5, 20, 20))


class Onibus(Veiculo):
    def __init__(self, x, y, direcao):
        velocidade = VELOCIDADE_ONIBUS_BASE + random.uniform(-0.5, 0.5)
        super().__init__(x, y, 70, 35, AMARELO, velocidade, direcao)
        for i in range(5):
            pygame.draw.rect(self.image, PRETO, (10 + i * 12, 5, 8, 25))
        pygame.draw.rect(self.image, CINZA_ESCURO, (5, 15, 5, 10))


# Função para desenhar as vidas na tela
def desenhar_vidas(tela, x, y, vidas):
    for i in range(vidas):
        coracao = pygame.Rect(x + i * 35, y, 30, 30)
        pygame.draw.rect(tela, VERMELHO, coracao)
        pygame.draw.polygon(tela, ROSA, [
            (x + i * 35 + 15, y + 5),
            (x + i * 35 + 5, y + 15),
            (x + i * 35 + 15, y + 25),
            (x + i * 35 + 25, y + 15)
        ])


# Lógica de Geração de Veículos
def gerar_veiculos():
    veiculos = pygame.sprite.Group()

    for i, y in enumerate(FAIXAS_Y):

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

            veiculo = TipoVeiculo(x_inicial, y, direcao)
            veiculos.add(veiculo)

    return veiculos


# Função para a tela de Fim de Jogo/Vitória e Reinício
def tela_final(vitoria, pontuacao):
    # Loop da tela final
    aguardando_reiniciar = True
    while aguardando_reiniciar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # *** LÓGICA DE REINÍCIO ***
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Tecla 'R' para Reiniciar
                    return True  # Sinaliza para o loop principal reiniciar
                elif event.key == pygame.K_q:  # Tecla 'Q' para Sair
                    pygame.quit()
                    sys.exit()

        # Desenho da tela final
        TELA.fill(VERDE)

        if vitoria:
            texto_principal = fonte.render("VITÓRIA!", True, AZUL)
            texto_secundario = fonte.render("Você atravessou a rua!", True, PRETO)
        else:
            texto_principal = fonte.render("Game Over!", True, VERMELHO)
            texto_secundario = fonte.render("Você foi atropelado!", True, PRETO)

        texto_pontuacao = fonte.render(f"Pontuação Final: {pontuacao}", True, PRETO)
        texto_reiniciar = fonte.render("Pressione R para Reiniciar ou Q para Sair", True, CINZA_ESCURO)

        # Centralizando os textos
        TELA.blit(texto_principal, (LARGURA // 2 - texto_principal.get_width() // 2, ALTURA // 2 - 90))
        TELA.blit(texto_secundario, (LARGURA // 2 - texto_secundario.get_width() // 2, ALTURA // 2 - 30))
        TELA.blit(texto_pontuacao, (LARGURA // 2 - texto_pontuacao.get_width() // 2, ALTURA // 2 + 30))
        TELA.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 100))

        pygame.display.flip()
        clock.tick(10)  # FPS baixo na tela final

    return False  # Retorno padrão (não deve ser alcançado se o jogador sair ou reiniciar)


# Função principal do Jogo
def jogo():
    # Grupos de sprites
    todos_sprites = pygame.sprite.Group()

    jogador = Jogador()
    todos_sprites.add(jogador)

    veiculos = gerar_veiculos()
    todos_sprites.add(veiculos)

    # Sistema de vidas e pontuação
    vidas = 3
    pontuacao = 0
    pontuacao_faixa = 10

    # Loop do jogo
    executando = True
    while executando:

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                executando = False

        # --- LÓGICA DE PONTUAÇÃO E CHEGADA ---

        vitoria = False

        if jogador.faixa_atual > 0:
            y_da_faixa_alvo = FAIXAS_Y[jogador.faixa_atual - 1] - 10
        else:
            y_da_faixa_alvo = POSICAO_CHEGADA + 10

        if jogador.rect.y < y_da_faixa_alvo:
            if jogador.faixa_atual > 0:
                pontuacao += pontuacao_faixa
                jogador.faixa_atual -= 1

                if jogador.faixa_atual == 0:
                    executando = False
                    vitoria = True

                    # Colisões
        if pygame.sprite.spritecollide(jogador, veiculos, False) and not jogador.invulneravel:
            vidas -= 1
            if vidas <= 0:
                executando = False
                vitoria = False
            else:
                jogador.tornar_invulneravel()
                jogador.resetar_posicao()
                # A faixa atual é resetada dentro de resetar_posicao

        # Atualizar
        if executando:
            todos_sprites.update()

        # Desenhar
        TELA.fill(VERDE)

        # Desenhar área de CHEGADA
        pygame.draw.rect(TELA, AMARELO, (0, POSICAO_CHEGADA, LARGURA, 80))

        # Desenhar estrada
        for i in range(len(FAIXAS_Y) + 1):
            # Faixas de asfalto
            pygame.draw.rect(TELA, CINZA, (0, 80 + i * INCREMENTO_Y, LARGURA, 40))  # Usa INCREMENTO_Y
            # Linhas divisórias
            for j in range(0, LARGURA, 20):
                pygame.draw.rect(TELA, AMARELO, (j, 100 + i * INCREMENTO_Y, 10, 5))  # Usa INCREMENTO_Y

        # Desenhar área de INÍCIO (grama)
        pygame.draw.rect(TELA, VERDE, (0, ALTURA - 80, LARGURA, 80))

        todos_sprites.draw(TELA)

        # Mostrar HUD
        texto_pontos = fonte.render(f"Pontos: {pontuacao}", True, PRETO)
        TELA.blit(texto_pontos, (10, 10))
        desenhar_vidas(TELA, LARGURA - 120, 10, vidas)

        pygame.display.flip()
        clock.tick(FPS)

    # Quando o loop do jogo termina (executando = False), chama a tela final
    return tela_final(vitoria, pontuacao)


# Função principal que gerencia o loop de reinício
def main():
    rodando = True
    while rodando:
        reiniciar_jogo = jogo()
        if not reiniciar_jogo:
            rodando = False

    pygame.quit()
    sys.exit()


# Iniciar o jogo
if __name__ == "__main__":
    main()