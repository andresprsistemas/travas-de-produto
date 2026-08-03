#!/usr/bin/env python3
"""
R1 — Antes de criar ESTRUTURA DE DADOS nova, reusar a que já existe.

RECORTE: este hook enxerga só formato de banco — migração, esquema, modelo,
.sql, e os comandos que criam ou alteram tabela. NÃO enxerga script novo, fila
nova, serviço novo nem caminho paralelo de coleta: essas são duplicações que
nenhum programa reconhece no instante da ação. Para elas existe a skill
`auditoria-de-caminho-duplicado`, que você invoca antes de construir.

Evento: PreToolUse · Ferramentas: Write, Edit, Bash
Ação: INJETA a regra. Não barra nada.

Por que injeta e não barra: a pergunta da R1 — "já existe estrutura que guarda
este dado?" — é julgamento sobre o seu código. Nenhum script responde isso. O
hook só garante que a pergunta chegue no momento certo.

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
# São expressões regulares, sem diferenciar maiúsculas de minúsculas.
# Se não souber quais são as suas, peça ao Claude: "liste os caminhos e comandos
# deste projeto que criam estrutura persistente — migração, esquema, tabela,
# modelo, fonte, campo agregador."
#
# NÃO use \b nestes padrões. `\bmigrate\b` não casa `migrate_precos.py` NEM
# `db_migrate.py`, porque o underline conta como letra para a expressão. Escreva
# só o pedaço da palavra: `migrate` casa os três.
# ─────────────────────────────────────────────────────────────────────────────

CAMINHOS = [
    r"/migrations?/",
    r"/schemas?/",
    r"/models?/",
    r"\.sql$",
    r"alembic",
    r"prisma/schema",
]

COMANDOS = [
    r"create\s+table",
    r"alter\s+table.*\badd\b",
    r"migrate",
    r"alembic",
    r"prisma\s+migrate",
    r"createdb",
]

# ─────────────────────────────────────────────────────────────────────────────

TEXTO = """R1 — Antes de criar estrutura de dados nova, reusar a que já existe.

Você está prestes a {acao} ({alvo}).

Antes de seguir: verifique se já existe estrutura neste projeto que guarda este
dado. SE existir, meça o custo de duplicar contra o de reusar e apresente a
versão que reusa como default — só crie se a medição provar que reusar não
serve, dizendo por quê. Se NÃO houver candidato, prossiga e crie direto: uma
entidade genuinamente nova não exige o teatro da medição.

Escreva a medição. Sem medição escrita, a regra não foi aplicada."""


def main():
    dados = ler_entrada()
    ferramenta = campo(dados, "tool_name")

    if ferramenta in ("Write", "Edit"):
        alvo = campo(dados, "tool_input.file_path")
        if casa_algum(alvo, CAMINHOS):
            injetar("PreToolUse", TEXTO.format(
                acao="gravar num arquivo de estrutura persistente", alvo=alvo))

    elif ferramenta == "Bash":
        alvo = campo(dados, "tool_input.command")
        if casa_algum(alvo, COMANDOS):
            injetar("PreToolUse", TEXTO.format(
                acao="executar um comando que cria estrutura", alvo=alvo))

    seguir()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Falha aberta: hook quebrado nunca trava o trabalho.
        sys.exit(0)
