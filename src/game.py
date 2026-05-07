import pygame
import random
import sys
from src.constants import *
from src.utils import resource_path
from src.sprites import Jogador, Carro, Onibus, Obstaculo, ItemBonus

class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Crossy Road Python - Modular")
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.SysFont(None, 36)
        
        self.fator_dificuldade = 0.0
        self.posicoes_y = self._calcular_posicoes_y()
        self.faixas_veiculos_y = [self.posicoes_y[1], self.posicoes_y[2], self.posicoes_y[4], self.posicoes_y[5], self.posicoes_y[7], self.posicoes_y[8]]
        self.posicao_chegada = self.posicoes_y[0]
        self.spawn_y = self.posicoes_y[9] + ALTURA_FAIXA_EXTREMA // 2
        
        self.audio_disponivel = self._inicializar_audio()
        
    def _calcular_posicoes_y(self):
        pos = []
        y = 0
        for altura, _ in FAIXAS_LAYOUT:
            pos.append(y)
            y += altura
        return pos

    def _inicializar_audio(self):
        try:
            pygame.mixer.init()
            self.sons = {
                'colisao': pygame.mixer.Sound(resource_path(SOM_COLISAO)),
                'ponto': pygame.mixer.Sound(resource_path(SOM_PONTO)),
                'game_over': pygame.mixer.Sound(resource_path(SOM_GAME_OVER)),
                'vitoria': pygame.mixer.Sound(resource_path(SOM_VITORIA)),
                'item': pygame.mixer.Sound(resource_path(SOM_ITEM))
            }
            pygame.mixer.music.load(resource_path(MUSICA_FUNDO))
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
            return True
        except Exception as e:
            print(f"Erro ao inicializar áudio: {e}")
            return False

    def reset_groups(self):
        self.todos_sprites = pygame.sprite.Group()
        self.veiculos = pygame.sprite.Group()
        self.obstaculos = pygame.sprite.Group()
        self.itens_bonus = pygame.sprite.Group()
        
        self.jogador = Jogador(self.spawn_y)
        self.jogador.faixa_atual = len(self.faixas_veiculos_y) # Começa na última faixa
        self.todos_sprites.add(self.jogador)
        
        # Gerar Veículos
        for i, y_faixa in enumerate(self.faixas_veiculos_y):
            # Apenas um veículo por faixa conforme solicitado
            num_veiculos = 1
            direcao = 1 if i % 2 == 0 else -1
            
            for j in range(num_veiculos):
                x = random.randint(0, LARGURA - 200)
                tipo = random.choice([Carro, Onibus])
                v = tipo(x, y_faixa, direcao, self.fator_dificuldade)
                self.veiculos.add(v)
                self.todos_sprites.add(v)

        # Gerar Obstáculos (Árvores apenas na Grama)
        for i in [0, 3, 6, 9]:
            num = random.randint(2, 4) if i not in [0, 9] else 1
            for _ in range(num):
                x = random.randint(10, LARGURA-50)
                if i == 9 and abs(x - LARGURA//2) < 100: continue
                # Passa a estação para o obstáculo usar o visual correto
                obs = Obstaculo(x, self.posicoes_y[i], FAIXAS_LAYOUT[i][0], self.estacao_nome)
                self.obstaculos.add(obs)
                self.todos_sprites.add(obs)

        # Gerar Itens Bônus (Power-ups)
        for i in [3, 6]: # Gramados intermediários
            if random.random() < 0.5:
                # Tenta encontrar uma posição que não colida com árvores
                for _ in range(10): # 10 tentativas
                    x = random.randint(100, LARGURA-100)
                    tipo_item = random.choice(['vida', 'escudo'])
                    item = ItemBonus(x, self.posicoes_y[i], FAIXAS_LAYOUT[i][0], tipo_item)
                    if not pygame.sprite.spritecollideany(item, self.obstaculos):
                        self.itens_bonus.add(item)
                        self.todos_sprites.add(item)
                        break

    def desenhar_hud(self, vidas, pontuacao):
        txt_pontos = self.fonte.render(f"Pontos: {pontuacao}", True, PRETO)
        txt_nivel = self.fonte.render(f"Nível: {int(self.fator_dificuldade * 2) + 1}", True, PRETO)
        self.tela.blit(txt_pontos, (10, 10))
        self.tela.blit(txt_nivel, (10, 40))
        
        # Desenhar Corações no HUD
        for i in range(vidas):
            x = LARGURA - 40 - i*35
            y = 25
            # Desenha um coração usando dois círculos e um triângulo
            cor = ROSA
            pygame.draw.circle(self.tela, cor, (x - 6, y - 5), 7)
            pygame.draw.circle(self.tela, cor, (x + 6, y - 5), 7)
            pygame.draw.polygon(self.tela, cor, [(x - 13, y - 2), (x + 13, y - 2), (x, y + 12)])

    def loop(self, vidas, pontuacao):
        # Determinar estação atual (muda a cada 5 níveis)
        nivel = int(self.fator_dificuldade * 2) + 1
        estacao_idx = ((nivel - 1) // 5) % 4
        self.estacao_nome = ORDEM_ESTACOES[estacao_idx]
        self.estacao_atual = ESTACOES[self.estacao_nome]
        
        self.reset_groups()
        
        rodando = True
        while rodando:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"

            self.todos_sprites.update()
            
            # Colisões
            if pygame.sprite.spritecollide(self.jogador, self.obstaculos, False, pygame.sprite.collide_mask):
                # Impede movimento (lógica simplificada: volta um pouco)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP]: self.jogador.rect.y += self.jogador.velocidade
                if keys[pygame.K_DOWN]: self.jogador.rect.y -= self.jogador.velocidade
                if keys[pygame.K_LEFT]: self.jogador.rect.x += self.jogador.velocidade
                if keys[pygame.K_RIGHT]: self.jogador.rect.x -= self.jogador.velocidade

            if pygame.sprite.spritecollide(self.jogador, self.veiculos, False, pygame.sprite.collide_mask) and not self.jogador.invulneravel:
                vidas -= 1
                if self.audio_disponivel: self.sons['colisao'].play()
                if vidas <= 0:
                    if self.audio_disponivel: self.sons['game_over'].play()
                    return "GAMEOVER", pontuacao, 0
                self.jogador.tornar_invulneravel()
                self.jogador.resetar_posicao()

            # Sistema de Pontuação por Faixas
            if self.jogador.faixa_atual > 0:
                y_alvo = self.faixas_veiculos_y[self.jogador.faixa_atual - 1]
                if self.jogador.rect.top < y_alvo:
                    pontuacao += 10
                    self.jogador.faixa_atual -= 1
                    if self.audio_disponivel: self.sons['ponto'].play()

            # Colisão com Itens de Bônus
            item_hit = pygame.sprite.spritecollide(self.jogador, self.itens_bonus, True, pygame.sprite.collide_mask)
            for item in item_hit:
                if self.audio_disponivel: self.sons['item'].play()
                if item.tipo == 'vida':
                    if vidas < 3: vidas += 1 # Limite de 3 vidas
                elif item.tipo == 'escudo':
                    self.jogador.tornar_invulneravel()
                pontuacao += 50

            # Chegada
            if self.jogador.rect.top <= self.posicao_chegada:
                if self.audio_disponivel: self.sons['vitoria'].play()
                return "VITORIA", pontuacao, vidas

            # Desenho
            self.tela.fill(VERDE_GRAMA)
            self._desenhar_cenario()
            
            self.todos_sprites.draw(self.tela)
            self.desenhar_hud(vidas, pontuacao)
            pygame.display.flip()

    def _desenhar_cenario(self):
        y = 0
        cor_grama = self.estacao_atual['GRAMA']
        cor_estrada = self.estacao_atual['ESTRADA']
        
        for i, (altura, cor_original) in enumerate(FAIXAS_LAYOUT):
            # Usa as cores da estação
            cor_final = cor_grama if cor_original == (0, 150, 0) else cor_estrada # Compara com verde padrão
            # Na verdade, no Layout usamos as constantes (0, 150, 0) indiretamente?
            # Melhor usar a lógica: se for grama no layout original, usa grama da estação.
            
            # Vamos corrigir o layout para usar identificadores em vez de cores fixas no futuro, 
            # mas por hora, se o layout diz CINZA_ESTRADA, usamos o da estação.
            cor_desenho = cor_estrada if cor_original == (50, 50, 50) else cor_grama
            
            pygame.draw.rect(self.tela, cor_desenho, (0, y, LARGURA, altura))
            
            # Desenha linha amarela apenas se houver duas faixas de asfalto seguidas
            if cor_original == (50, 50, 50) and i + 1 < len(FAIXAS_LAYOUT):
                if FAIXAS_LAYOUT[i+1][1] == (50, 50, 50):
                    for x in range(0, LARGURA, 40):
                        pygame.draw.line(self.tela, AMARELO_LINHA, (x, y + altura), (x + 20, y + altura), 3)
            y += altura

    def tela_final(self, estado, pontuacao):
        pygame.event.clear() # Limpa eventos residuais
        while True:
            self.tela.fill(VERDE_GRAMA)
            nivel_atual = int(self.fator_dificuldade * 2) + 1
            msg = f"VITÓRIA NO NÍVEL {nivel_atual}!" if estado == "VITORIA" else "GAME OVER!"
            txt = self.fonte.render(f"{msg} Pontos: {pontuacao}", True, PRETO)
            txt2 = self.fonte.render("Pressione R para Reiniciar ou Q para Sair", True, PRETO)
            self.tela.blit(txt, (LARGURA//2 - 100, ALTURA//2 - 50))
            self.tela.blit(txt2, (LARGURA//2 - 200, ALTURA//2 + 50))
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        if estado == "VITORIA": self.fator_dificuldade += 0.5
                        else: self.fator_dificuldade = 0.0
                        return True
                    if event.key == pygame.K_q: return False

    def run(self):
        jogando = True
        vidas = 3
        pontuacao = 0
        while jogando:
            resultado = self.loop(vidas, pontuacao)
            if resultado == "QUIT": break
            estado, pontuacao, vidas = resultado
            
            # Se for vitoria, mantém o estado para o próximo nível
            # Se for game over, reseta vidas e pontos
            jogando = self.tela_final(estado, pontuacao)
            if estado == "GAMEOVER":
                vidas = 3
                pontuacao = 0
        pygame.quit()
