#!/usr/bin/env python3
"""
R2 — Capacidade pronta aponta consumidor.

Evento: Stop (quando o Claude termina de responder) · Ação: INJETA. Não barra.

A ideia que torna este hook viável não é "o modelo declarou pronto" — isso um
script não lê. É outra pergunta, que um script LÊ: **este turno mexeu em
estrutura persistente?** Se mexeu, a pergunta da R2 chega junto.

Usa `git` para saber o que mudou. Sem git, o hook não faz nada — e isso é
proposital: melhor não disparar do que disparar por adivinhação.

>>> EDITE A SEÇÃO ABAIXO. Sem isso, este hook não faz nada. <<<
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

# ─── funções internas (iguais nos quatro hooks, de propósito) ────────────────
# Cada hook é um arquivo só, que funciona sozinho. Não há módulo compartilhado:
# um quinto arquivo esquecido na cópia deixaria os quatro silenciosamente
# inertes — que é exatamente a peça oca que este repositório existe para evitar.

def ler_entrada():
    """Lê o JSON que o Claude Code manda no stdin. Devolve {} se falhar."""
    try:
        bruto = sys.stdin.read()
        if not bruto.strip():
            return {}
        dados = json.loads(bruto)
        return dados if isinstance(dados, dict) else {}
    except Exception:
        return {}


def campo(dados, caminho, padrao=""):
    """Lê um campo aninhado ('tool_input.command') sem estourar se faltar."""
    atual = dados
    try:
        for parte in caminho.split("."):
            atual = atual[parte]
        return atual if isinstance(atual, str) else padrao
    except Exception:
        return padrao


def casa_algum(texto, padroes):
    """Devolve o padrão que casou, ou None. Regex, sem diferenciar maiúsculas."""
    if not texto:
        return None
    for p in padroes:
        try:
            if re.search(p, texto, re.IGNORECASE):
                return p
        except re.error:
            continue   # padrão inválido escrito pelo usuário: ignora esse
    return None


def raiz_do_projeto(dados):
    """Melhor palpite da raiz do projeto: variável do Claude Code, senão o cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR") or campo(dados, "cwd") or os.getcwd()


def injetar(evento, texto):
    """Põe o texto na frente do modelo SEM barrar a ação. Sai com código 0."""
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": evento, "additionalContext": texto}}))
    sys.exit(0)


def seguir():
    """Nada a dizer. A ação segue normalmente."""
    sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO — a única parte que você precisa mexer.
#
# Caminhos onde mora estrutura que outra coisa deveria consumir: esquemas,
# modelos, migrações, geradores de dado, relatórios de saída.
# ─────────────────────────────────────────────────────────────────────────────

CAMINHOS = [
    r"/migrations?/",
    r"/schemas?/",
    r"/models?/",
    r"\.sql$",
]

# ─────────────────────────────────────────────────────────────────────────────

TEXTO = """R2 — Capacidade pronta aponta consumidor.

Há estrutura persistente alterada e ainda não commitada:
{lista}

Antes de declarar isso pronto: aponte quem consome, no caminho que roda de
verdade. Não basta alguém LER — o que o sistema DECIDE ou CALCULA tem que mudar
por causa disto. Filtrar, esconder ou registrar não conta.

Se você não achar o consumidor, diga isso em vez de assumir que existe.
Capacidade que nenhum fluxo real lê é peça oca: finge cobertura.

Este aviso só sabe QUE a estrutura está alterada. Ele não procurou o consumidor —
para isso existe a skill `auditoria-de-peca-oca`, que devolve veredito com
evidência apontável.

(Você só vê este aviso uma vez por conjunto de arquivos. Ele volta se a lista
mudar.)"""


def arquivos_mexidos(raiz):
    """Arquivos alterados segundo o git. Lista vazia se não houver git."""
    vistos = []
    for args in (["git", "diff", "--name-only", "HEAD"],
                 ["git", "ls-files", "--others", "--exclude-standard"]):
        try:
            saida = subprocess.run(
                args, cwd=raiz, capture_output=True, text=True, timeout=5)
            if saida.returncode == 0:
                vistos += [l.strip() for l in saida.stdout.splitlines() if l.strip()]
        except Exception:
            continue
    return vistos


def ja_avisado(raiz, alvos):
    """
    Avisa uma vez por conjunto de arquivos. Sem isto, o hook injetaria o bloco
    inteiro ao fim de TODO turno enquanto a migração ficasse sem commit — que é
    o jeito mais rápido de virar ruído que a pessoa aprende a ignorar.
    """
    marca = hashlib.sha256("\n".join(alvos).encode("utf-8")).hexdigest()[:16]
    try:
        pasta = os.path.join(raiz, ".git")
        if not os.path.isdir(pasta):
            pasta = tempfile.gettempdir()
        arquivo = os.path.join(pasta, "r2-ultimo-aviso")
        if os.path.exists(arquivo):
            with open(arquivo, encoding="utf-8") as f:
                if f.read().strip() == marca:
                    return True
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(marca)
    except Exception:
        return False   # não deu para lembrar: melhor avisar de novo que calar
    return False


def main():
    dados = ler_entrada()

    # Se o hook já bloqueou seguidas vezes, o Claude Code marca isto. Nunca
    # insistimos — este hook não bloqueia, mas a checagem é barata e correta.
    if dados.get("stop_hook_active") is True:
        seguir()

    raiz = raiz_do_projeto(dados)
    alvos = sorted(set(a for a in arquivos_mexidos(raiz) if casa_algum(a, CAMINHOS)))

    if alvos and not ja_avisado(raiz, alvos):
        lista = "\n".join("  - " + a for a in alvos[:20])
        injetar("Stop", TEXTO.format(lista=lista))

    seguir()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
