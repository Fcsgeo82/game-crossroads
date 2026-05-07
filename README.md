# Crossy Road Python

Um clone moderno e modular do clássico jogo Crossy Road (ou Frogger) construído em Python usando a biblioteca Pygame. O jogo apresenta integração completa com assets visuais, sistema de níveis progressivos e suporte a bônus.

## 🎮 Funcionalidades

- **Visual Premium**: Utiliza sprites reais para jogador, veículos e ambiente.
- **Estrutura Modular**: Código organizado em módulos (`src/`) para fácil manutenção.
- **Sistema de Dificuldade**: A velocidade dos veículos aumenta conforme você avança de nível.
- **Bônus e Power-ups**: Inclui sistema de vidas extras e escudos de invulnerabilidade.
- **Build Automatizado**: Script para gerar executável (.exe) via PyInstaller.

## 📁 Estrutura do Projeto

- `main.py`: Ponto de entrada do jogo.
- `src/`: Lógica do jogo dividida em módulos.
  - `constants.py`: Configurações globais.
  - `sprites.py`: Classes de personagens e veículos.
  - `game.py`: Loop principal e gerenciamento de estados.
  - `utils.py`: Funções auxiliares.
- `assets/`: Imagens e sons do jogo.
- `legacy/`: Versões antigas do código para referência.

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
*Desenvolvido como um projeto de estudo de Pygame e Arquitetura Modular.*
