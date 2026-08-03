#!/usr/bin/env python3
"""
R4 — Execução sobre dado real não-controlado.

Evento: PreToolUse · Ferramenta: Bash
Ação: INJETA a regra. Não barra nada.

É o caso mais limpo dos quatro: carga, migração e backfill SÃO comandos, e a
lista deles no seu projeto é finita e enumerável. Injeta em vez de barrar porque
travar toda carga travaria o trabalho normal — o que falta não é permissão, é a
disciplina chegar na hora.

>>> EDITE A SEÇÃO ABAIXO. Sem isso, este hook não faz nada. <<<
"""

import json
import re
import sys

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
# Peça ao Claude: "liste os comandos deste projeto que rodam carga, migração,
# backfill, ingestão de fonte nova ou expansão de escopo sobre dado que eu não
# controlo — inclusive os que chamam script ou serviço externo."
#
# NÃO use \b nestes padrões. `\bbackfill\b` não casa `backfill_precos.py` NEM
# `run_backfill.py`, porque o underline conta como letra para a expressão. Escreva
# só o pedaço da palavra: `backfill` casa os três.
#
# Como este hook só AVISA (não trava nada), errar para mais é barato. Prefira
# pegar demais a deixar passar.
# ─────────────────────────────────────────────────────────────────────────────

COMANDOS = [
    r"backfill",
    r"ingest(?!ion_test)",
    r"bulk[_-]?load",
    r"(^|[\s/_.-])seed([\s_.-]|$)",
    r"migrate",
    r"scrap(e|ing|er)",
    r"collect(?!ions?\b|-only\b|_only\b)",
]

# ─────────────────────────────────────────────────────────────────────────────

TEXTO = """R4 — Execução sobre dado real não-controlado.

Comando prestes a rodar: {alvo}

1. Exponha POUCO antes de expor a base inteira.
2. Olhe o indicador de saúde a cada toque — não só no fim.
3. Se quebrar, a ordem é fixa: CONTER (preservando o que já estava certo) →
   CORRIGIR → PUBLICAR. Nunca corrigir antes de conter: corrigir sobre estado
   quebrado empilha falha sobre falha.

E: se o que você está tocando alimenta um indicador da lista de indicadores
críticos, verifique se esse indicador tem alarme permanente que dispara sozinho
quando desaba. Se não tem, é peça oca de vigilância — registre o gap.

Este aviso chega antes. Olhar o indicador e conter acontecem durante e depois,
e nenhum hook faz isso por você."""


def main():
    dados = ler_entrada()

    if campo(dados, "tool_name") != "Bash":
        seguir()

    comando = campo(dados, "tool_input.command")
    if casa_algum(comando, COMANDOS):
        injetar("PreToolUse", TEXTO.format(alvo=comando))

    seguir()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
