#!/usr/bin/env python3
"""
S0 — Declarar os indicadores críticos antes de tocar produção.

Evento: PreToolUse · Ferramenta: Bash
Ação: BARRA. É o único dos quatro que barra.

Por que este barra e os outros não: a condição dele é 100% legível por um
script — o arquivo `indicadores-criticos.md` tem pelo menos uma linha de dado,
ou não tem. Não há julgamento nenhum. Nos outros três a condição é interpretação,
e barrar por interpretação trava trabalho legítimo.

E é onde barrar mais paga: o S0 é um portão. Portão que o modelo pode ignorar
não é portão, é sugestão.

>>> EDITE A SEÇÃO ABAIXO. Sem isso, este hook não faz nada. <<<
"""

import json
import os
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


def barrar(motivo):
    """Impede a ação. Sai com código 0 — quem barra é o JSON, não o código."""
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": motivo}}))
    sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÃO — a única parte que você precisa mexer.
#
# Peça ao Claude: "liste os comandos deste projeto que tocam produção — deploy,
# migração, carga, ou qualquer escrita em dado real."
#
# ATENÇÃO: este é o único hook que BARRA, e por isso a lista de fábrica é
# deliberadamente ESTREITA — o contrário dos outros. Padrão largo aqui trava
# trabalho legítimo: `deploy` solto pegaria `cat docs/deploy.md`. Comece com o
# comando exato que você usa para publicar, e só acrescente quando sentir falta.
#
# Não use \b: o underline conta como letra para a expressão, então `\bdeploy\b`
# não casa `deploy_prod.sh`. Use pedaço de palavra com a borda explícita, como
# nos exemplos abaixo.
# ─────────────────────────────────────────────────────────────────────────────

COMANDOS_DE_PRODUCAO = [
    r"(^|[\s/_.-])deploy(\.sh|\.py|$|[\s_-])",
    r"kubectl\s+apply(?!.*--dry-run)",
    r"terraform\s+apply",
]

# Comandos que só LEEM. Se a linha começa com um destes, o hook nem olha os
# padrões acima — `cat docs/deploy.md` não é um deploy.
SO_LEEM = [
    r"^\s*(cat|less|more|head|tail|grep|rg|ag|ls|find|echo|which|man|wc)\b",
    r"^\s*git\s+(log|show|diff|status|blame|grep)\b",
]

# Onde o hook procura a lista. Caminho relativo à raiz do projeto.
ARQUIVO = "indicadores-criticos.md"

# Comece com False. Assim o hook só AVISA, sem travar nada, e você vê durante
# alguns dias em que comandos ele realmente dispara. Quando os disparos fizerem
# sentido, troque para True e ele passa a barrar de verdade.
BARRAR_DE_VERDADE = False

# ─────────────────────────────────────────────────────────────────────────────

LEMBRETE = """S0 — o setup dos indicadores críticos continua pendente.

Comando: {alvo}

O PM já pediu para pular, e a pendência está gravada em `{arquivo}` — então NÃO
barro esta ação. Mas a lista continua sem nenhum indicador confirmado, e sem ela
a R4 não tem o que ler. Se for um bom momento, ofereça retomar o roteiro; se não
for, siga em frente sem insistir."""


MOTIVO = """S0 — Setup obrigatório: declare os indicadores críticos antes de tocar produção.

Ação: {alvo}
Motivo: não há nenhum indicador confirmado em `{caminho}`.

Antes de executar, conduza este roteiro com o PM. Diga, textualmente:
"Antes de tocar produção, preciso saber o que NÃO pode colapsar. Vou perguntar
sobre consequência — não sobre que tipo de número é. Responda com as suas
palavras. 1 indicador é o mínimo para prosseguir; 3 a 5 é o ideal. Se preferir
adiar, diga 'pular por agora'."

Faça a primeira pergunta; a cada "mais algum?", use a próxima:
1. Que número, se ficasse errado para um usuário amanhã, faria você perder a
   confiança dele — ou a confiança dele no produto?
2. Que valor, se colapsasse em silêncio, você só descobriria pelo dano, tarde
   demais?
3. Se você pudesse vigiar um único número em produção esta noite, qual seria?

Conduta: faça a pergunta exatamente como está escrita e não acrescente exemplo
de tipo nem de domínio, em nenhum momento. Registre apenas o indicador que o PM
nomear por iniciativa dele. Transcreva a resposta literalmente, sem validar nem
criticar. O julgamento do que é crítico é inteiramente do PM.

Grave em `{arquivo}`, NA RAIZ DO PROJETO (é onde este hook procura), uma linha por
indicador:
  nome | por que o colapso é desastre | onde é calculado (path, ou "não sei ainda")

Se o PM disser "pular por agora", grave só esta linha e prossiga:
  # PENDENCIA: setup adiado — "pular por agora".
A partir daí o portão para de barrar e passa só a lembrar.

Depois de gravar, execute a ação original."""


def estado_da_lista(caminho):
    """
    'confirmado' — tem ao menos uma linha de dado.
    'pendencia'  — só comentário, e um deles é a linha de pendência ("pular por agora").
    'vazio'      — não existe, ou só tem comentário sem pendência.
    'ilegivel'   — existe mas não deu para ler.
    """
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except FileNotFoundError:
        return "vazio"
    except Exception:
        return "ilegivel"

    tem_pendencia = False
    for linha in linhas:
        limpa = linha.strip()
        if not limpa:
            continue
        if limpa.startswith("#"):
            if "pend" in limpa.lower() or "pular por agora" in limpa.lower():
                tem_pendencia = True
            continue
        return "confirmado"
    return "pendencia" if tem_pendencia else "vazio"


def main():
    dados = ler_entrada()

    if campo(dados, "tool_name") != "Bash":
        seguir()

    comando = campo(dados, "tool_input.command")
    if casa_algum(comando, SO_LEEM):
        seguir()
    if not casa_algum(comando, COMANDOS_DE_PRODUCAO):
        seguir()

    caminho = os.path.join(raiz_do_projeto(dados), ARQUIVO)
    estado = estado_da_lista(caminho)

    if estado in ("confirmado", "ilegivel"):
        seguir()   # confirmado: silêncio permanente. Ilegível: falha aberta.

    # ESCAPE: se o PM já disse "pular por agora", o portão NÃO barra mais — ele
    # lembra, e deixa passar. Barrar aqui viraria laço sem saída: o modelo grava
    # a pendência, tenta de novo, é barrado de novo, e ninguém sai disso.
    if estado == "pendencia":
        injetar("PreToolUse", LEMBRETE.format(alvo=comando, arquivo=ARQUIVO))

    texto = MOTIVO.format(alvo=comando, arquivo=ARQUIVO,
                          caminho=os.path.join("<raiz do projeto>", ARQUIVO))
    if BARRAR_DE_VERDADE:
        barrar(texto)
    injetar("PreToolUse", texto)   # modo de observação: avisa e deixa passar


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
