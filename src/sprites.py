import pygame
import random
import os
from src.constants import *
from src.utils import resource_path, carregar_imagem_limpa

class Jogador(pygame.sprite.Sprite):
    def __init__(self, spawn_y):
        super().__init__()
        # Carregar imagens
        try:
            self.img_up = carregar_imagem_limpa(os.path.join('assets', 'PlayerUp.png'))
            self.img_down = carregar_imagem_limpa(os.path.join('assets', 'PlayerDown.png'))
            
            # Agora escalar (tamanho real do desenho) - Reduzido para caber nas faixas duplas
            self.img_up = pygame.transform.scale(self.img_up, (50, 65))
            self.img_down = pygame.transform.scale(self.img_down, (50, 65))
            self.mask_up = pygame.mask.from_surface(self.img_up)
            self.mask_down = pygame.mask.from_surface(self.img_down)
        except Exception as e:
            print(f"Erro ao carregar sprites do jogador: {e}")
            self.img_up = pygame.Surface((30, 30))
            self.img_up.fill(VERMELHO)
            self.img_down = self.img_up
            self.mask_up = pygame.mask.from_surface(self.img_up)
            self.mask_down = pygame.mask.from_surface(self.img_up)

        self.image = self.img_up
        self.mask = self.mask_up
        self.spawn_y = spawn_y
        self.resetar_posicao()
        self.velocidade = 5
        self.invulneravel = False
        self.tempo_invulneravel = 0

    def update(self):
        keys = pygame.key.get_pressed()
        moveu = False
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
            moveu = True
        if keys[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.velocidade
            moveu = True
        if keys[pygame.K_UP] and self.rect.top > -10:
            self.rect.y -= self.velocidade
            self.image = self.img_up
            self.mask = self.mask_up
            moveu = True
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTURA:
            self.rect.y += self.velocidade
            self.image = self.img_down
            self.mask = self.mask_down
            moveu = True

        # Sistema de Invulnerabilidade
        if self.invulneravel:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_invulneravel > 3000: # 3 segundos de proteção
                self.invulneravel = False
                self.image.set_alpha(255)
            else:
                # Efeito de piscar/pulsar transparência
                alpha = 100 if (tempo_atual // 100) % 2 == 0 else 255
                self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def tornar_invulneravel(self):
        self.invulneravel = True
        self.tempo_invulneravel = pygame.time.get_ticks()

    def resetar_posicao(self):
        self.rect = self.image.get_rect(center=(LARGURA // 2, self.spawn_y))
        self.faixa_atual = 4 # Valor padrão baseado no layout original

class Veiculo(pygame.sprite.Sprite):
    def __init__(self, x, y_faixa, largura, altura, velocidade, direcao, img_path=None):
        super().__init__()
        if img_path:
            try:
                self.image = carregar_imagem_limpa(img_path)
                self.image = pygame.transform.scale(self.image, (largura, altura))
            except Exception as e:
                print(f"Erro no Veiculo: {e}")
                self.image = pygame.Surface((largura, altura))
                self.image.fill(AZUL)
        else:
            self.image = pygame.Surface((largura, altura))
            self.image.fill(AZUL)

        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = velocidade
        self.direcao = direcao
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
        largura, altura = 100, 45
        velocidade = VELOCIDADE_CARRO_BASE + fator_dificuldade + random.uniform(-0.5, 0.5)
        
        # Escolher sprite baseado na direção
        prefix = 'CarRight1.png' if direcao == 1 else 'CarLeft1.png'
        img_path = os.path.join('assets', prefix)
        
        super().__init__(x, y_faixa, largura, altura, velocidade, direcao, img_path)

class Onibus(Veiculo):
    def __init__(self, x, y_faixa, direcao, fator_dificuldade):
        largura, altura = 140, 50
        velocidade = VELOCIDADE_ONIBUS_BASE + (fator_dificuldade * 0.5) + random.uniform(-0.5, 0.5)
        img_path = os.path.join('assets', 'SchoolBus-1.png')
        super().__init__(x, y_faixa, largura, altura, velocidade, direcao, img_path)
        
        # Se estiver indo para a esquerda, inverte a imagem horizontalmente
        if direcao == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.mask = pygame.mask.from_surface(self.image)

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, x, y_faixa, altura_faixa, estacao_nome='PRIMAVERA'):
        super().__init__()
        try:
            # Pega o asset da estação (ou o padrão)
            img_nome = ESTACOES[estacao_nome]['ARVORE']
            self.image = carregar_imagem_limpa(os.path.join('assets', img_nome))
            self.image = pygame.transform.scale(self.image, (65, 65))
            
            # Efeito de Colorização para Estações (Sem ficar translúcido)
            if estacao_nome == 'OUTONO':
                # Aplica um tom alaranjado/marrom multiplicando as cores
                tint = pygame.Surface(self.image.get_size()).convert_alpha()
                tint.fill((255, 150, 50)) # Laranja forte
                self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            elif estacao_nome == 'INVERNO':
                # Aplica um tom de neve adicionando branco/azul
                tint = pygame.Surface(self.image.get_size()).convert_alpha()
                tint.fill((100, 100, 150)) # Azul acinzentado
                self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
                
        except:
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            # Cor do fallback baseada na estação
            cor = ESTACOES[estacao_nome]['GRAMA']
            pygame.draw.circle(self.image, (max(0, cor[0]-30), max(0, cor[1]-30), max(0, cor[2]-30)), (20, 20), 20)

        self.mask = pygame.mask.from_surface(self.image)
        # Centraliza na faixa de grama (que agora é maior: 100px)
        y_hitbox_centralizado = y_faixa + (altura_faixa - 65) // 2
        self.rect = self.image.get_rect(topleft=(x, y_hitbox_centralizado))

class ItemBonus(pygame.sprite.Sprite):
    def __init__(self, x, y_faixa, altura_faixa, tipo='vida'):
        super().__init__()
        self.tipo = tipo
        try:
            # Tenta carregar imagem baseada no tipo
            nome_arquivo = 'Life.png' if tipo == 'vida' else 'Shield.png'
            self.image = carregar_imagem_limpa(os.path.join('assets', nome_arquivo))
            self.image = pygame.transform.scale(self.image, (45, 45))
        except:
            # Fallback visual se não houver imagem
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            cor = ROSA if tipo == 'vida' else AZUL
            pygame.draw.circle(self.image, cor, (15, 15), 15)
            # Desenha um detalhe branco no meio para diferenciar
            pygame.draw.rect(self.image, BRANCO, (10, 10, 10, 10))

        self.mask = pygame.mask.from_surface(self.image)
        # Centraliza na faixa
        y_hitbox = y_faixa + (altura_faixa - 45) // 2
        self.rect = self.image.get_rect(topleft=(x, y_hitbox))
