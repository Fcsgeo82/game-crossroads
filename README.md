# Crossy Road Python - Modular Edition

Um clone moderno, modular e visualmente rico do clássico jogo Crossy Road (ou Frogger) construído em Python usando a biblioteca Pygame. O projeto foca em alta fidelidade visual, colisão precisa e progressão de níveis dinâmica.

## 🌟 Novas Funcionalidades (v2.0)

- **🍂 Sistema de Estações Dinâmico**: O cenário evolui conforme você avança! A cada 5 níveis, o jogo transita entre **Primavera, Verão, Outono e Inverno**, mudando cores de grama, asfalto e aplicando efeitos visuais (tintura) nas árvores.
- **🛣️ Rodovias de Pista Dupla**: Novo layout de estradas com pistas duplas e tráfego sincronizado, proporcionando um desafio mais estratégico.
- **✨ Tecnologia de Imagem Avançada**:
  - **Auto-Cleaning**: Sistema que detecta e remove fundos sólidos de sprites PNG automaticamente.
  - **Limpeza por Tolerância**: Remove resquícios de molduras e artefatos de compressão com precisão cirúrgica.
  - **Tintura Sazonal**: Processamento de imagem em tempo real para colorir a vegetação de acordo com a estação atual.
- **🎯 Colisão Pixel-Perfect**: Substituição de colisões por caixas (Rect) por **Máscaras de Colisão**, garantindo que você só morra se realmente encostar no desenho do carro.

## 🎮 Funcionalidades Base

- **Vidas e Persistência**: Sistema de até 3 vidas que persistem entre os níveis.
- **Power-ups**: Coleta de corações (vida extra) e escudos (invencibilidade temporária).
- **Dificuldade Progressiva**: A velocidade dos veículos e o spawn de obstáculos aumentam com o nível.
- **Build Automatizado**: Script para gerar executável (.exe) via PyInstaller.

## 📁 Estrutura do Projeto

- `main.py`: Ponto de entrada do jogo.
- `src/`: Lógica do jogo dividida em módulos.
  - `constants.py`: Definições globais, paletas de cores sazonais e layout.
  - `sprites.py`: Classes de personagens, veículos (Carros e Ônibus) e itens.
  - `game.py`: Loop principal, gerenciador de estações e física do jogo.
  - `utils.py`: Scanner de bordas e processador de assets.
- `assets/`: Imagens e sons do jogo.
- `legacy/`: Versões antigas do código para referência histórica.

## 🛠️ Instalação e Execução

### Pré-requisitos
- Python 3.8 ou superior instalado.

### Instalação
1. Clone este repositório ou baixe os arquivos.
2. Recomenda-se o uso de um ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Execução
Para iniciar o jogo, execute:
```bash
python main.py
```

## 📦 Gerar Executável (Build)

Para gerar uma versão executável para Windows:
1. Execute o arquivo `installer.bat`.
2. O executável será gerado na pasta `dist/`.

## 🕹️ Controles

- **Setas**: Mover o jogador.
- **R**: Reiniciar jogo (na tela de fim de jogo).
- **Q**: Sair do jogo.

---
*Desenvolvido como um projeto de estudo avançado de Pygame, Processamento de Imagem e Arquitetura Modular.*
