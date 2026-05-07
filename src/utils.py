import os
import sys
import pygame

def resource_path(relative_path):
    """Obtém o caminho absoluto para o asset, independente de ser executável ou script."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def carregar_imagem_limpa(caminho):
    """Carrega uma imagem, detecta fundo e limpa com tolerância de cor."""
    img = pygame.image.load(resource_path(caminho)).convert_alpha()
    w, h = img.get_size()
    
    # Amostra as bordas
    pixels_borda = []
    for x in range(w): pixels_borda.append(img.get_at((x, 0)))
    for y in range(h): pixels_borda.append(img.get_at((0, y)))
    
    pixels_opacos = [(p.r, p.g, p.b) for p in pixels_borda if p.a == 255]
    
    if pixels_opacos:
        from collections import Counter
        bg_color, freq = Counter(pixels_opacos).most_common(1)[0]
        
        # Se a cor de fundo for detectada, percorre e remove com tolerância
        if freq > (len(pixels_borda) * 0.1):
            new_img = img.copy()
            for x in range(w):
                for y in range(h):
                    p = img.get_at((x, y))
                    # Se a cor for muito similar ao fundo detectado, torna transparente (Tolerância aumentada para 40)
                    if (abs(p.r - bg_color[0]) < 40 and 
                        abs(p.g - bg_color[1]) < 40 and 
                        abs(p.b - bg_color[2]) < 40):
                        new_img.set_at((x, y), (0, 0, 0, 0))
            img = new_img
            
    rect = img.get_bounding_rect()
    if rect.width > 0 and rect.height > 0:
        return img.subsurface(rect)
    return img
