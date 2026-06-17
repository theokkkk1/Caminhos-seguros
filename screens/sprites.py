"""
sprites.py — Gerenciador de sprites customizados

Carrega imagens da pasta assets/sprites/ conforme configurado em
assets/sprites_config.json. Se a imagem não existir ou falhar ao
carregar, retorna False e o código original continua sendo usado
(fallback transparente, sem erros).

Uso típico nas fases:
    from screens import sprites

    # No início (main.py já chama automaticamente):
    sprites.load_all()

    # Na função de desenho:
    if not sprites.draw(screen, "arvore", rect.x, rect.y):
        draw_tree_fallback(screen, rect)
"""

import os
import json
import pygame

# =========================================================
# Resolução de caminhos
# =========================================================
#
# Tenta encontrar a pasta assets/ checando múltiplos candidatos.
# Cobre: "python main.py" de dentro da pasta, chamadas de fora,
# e executáveis empacotados.

def _find_base_dir() -> str:
    candidates = [
        os.getcwd(),                                                      # diretório de trabalho atual
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),      # relativo ao sprites.py
        os.path.dirname(os.path.abspath(__file__)),                       # pasta screens/
    ]
    for c in candidates:
        if os.path.isdir(os.path.join(c, "assets", "sprites")):
            return c
    return os.getcwd()  # fallback: deixa o log mostrar o caminho errado


_BASE_DIR   = _find_base_dir()
_SPRITES_DIR = os.path.join(_BASE_DIR, "assets", "sprites")
_CONFIG_PATH = os.path.join(_BASE_DIR, "assets", "sprites_config.json")

# =========================================================
# Estado interno
# =========================================================

_config:   dict = {}
_cache:    dict = {}   # {nome: Surface} ou {nome: None}
_hitboxes: dict = {}   # {nome: (off_x, off_y, w, h)} ou {nome: None}
_loaded:   bool = False


# =========================================================
# API pública
# =========================================================

def load_all() -> None:
    """
    Lê sprites_config.json e pré-carrega todas as imagens disponíveis.
    Chamado automaticamente por main.py após pygame.init().
    """
    global _config, _loaded

    print(f"[sprites] Pasta base  : {_BASE_DIR}")
    print(f"[sprites] Pasta sprites: {_SPRITES_DIR}")
    print(f"[sprites] Config       : {_CONFIG_PATH}")

    _config = _load_config()
    _cache.clear()
    _hitboxes.clear()

    for name, cfg in _config.items():
        if name.startswith("_"):
            continue
        _load_sprite(name, cfg)

    _loaded = True


def draw(screen: pygame.Surface, name: str, x: int, y: int) -> bool:
    """
    Desenha o sprite 'name' em (x, y).
    Retorna True se desenhado; False se sem imagem (use fallback).
    """
    if not _loaded:
        load_all()

    surface = _cache.get(name)
    if surface is None:
        return False

    screen.blit(surface, (x, y))
    return True


def get_hitbox(name: str, x: int, y: int):
    """
    Retorna pygame.Rect do hitbox configurado para 'name' em (x, y).
    Retorna None se não há sprite carregado para esse nome.
    """
    if not _loaded:
        load_all()

    if _cache.get(name) is None:
        return None

    hb = _hitboxes.get(name)
    if hb is None:
        surf = _cache[name]
        return pygame.Rect(x, y, surf.get_width(), surf.get_height())

    off_x, off_y, w, h = hb
    return pygame.Rect(x + off_x, y + off_y, w, h)


def has_sprite(name: str) -> bool:
    """Retorna True se a imagem para 'name' foi carregada com sucesso."""
    if not _loaded:
        load_all()
    return _cache.get(name) is not None


# =========================================================
# Helpers internos
# =========================================================

def _load_config() -> dict:
    try:
        with open(_CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[sprites] AVISO: sprites_config.json não encontrado em {_CONFIG_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"[sprites] ERRO: JSON inválido em sprites_config.json: {e}")
        return {}


def _load_sprite(name: str, cfg: dict) -> None:
    arquivo = cfg.get("arquivo", "")
    path = os.path.join(_SPRITES_DIR, arquivo)

    if not os.path.isfile(path):
        print(f"[sprites] '{name}': imagem não encontrada em {path} (usando fallback)")
        _cache[name] = None
        _hitboxes[name] = None
        return

    try:
        surface = pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"[sprites] '{name}': falha ao carregar {path}: {e}")
        _cache[name] = None
        _hitboxes[name] = None
        return

    # Redimensionar conforme configurado
    rw = cfg.get("render_width")
    rh = cfg.get("render_height")

    if rw and rh:
        surface = pygame.transform.smoothscale(surface, (int(rw), int(rh)))
    elif rw:
        ratio = rw / surface.get_width()
        surface = pygame.transform.smoothscale(
            surface, (int(rw), int(surface.get_height() * ratio))
        )
    elif rh:
        ratio = rh / surface.get_height()
        surface = pygame.transform.smoothscale(
            surface, (int(surface.get_width() * ratio), int(rh))
        )

    _cache[name] = surface

    # Processar hitbox
    hb_cfg = cfg.get("hitbox")
    if hb_cfg is None:
        _hitboxes[name] = None
    else:
        _hitboxes[name] = (
            int(hb_cfg.get("x", 0)),
            int(hb_cfg.get("y", 0)),
            int(hb_cfg.get("width",  surface.get_width())),
            int(hb_cfg.get("height", surface.get_height())),
        )

    print(f"[sprites] '{name}' OK: {path} → {surface.get_size()}")
