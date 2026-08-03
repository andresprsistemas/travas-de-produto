#!/usr/bin/env python3
"""
Testa os quatro hooks sem precisar do Claude Code.

Roda cada script com entradas JSON de mentira e confere três coisas:
  1. dispara quando deve;
  2. fica em silêncio quando não deve disparar;
  3. deixa passar quando a entrada está quebrada (falha aberta).

Uso:  python3 hooks/testar.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
falhas = []


def roda(script, entrada, cwd=None):
    pasta = BARRANDO if script.startswith("_") else AQUI
    p = subprocess.run(
        [sys.executable, os.path.join(pasta, script)],
        input=json.dumps(entrada) if isinstance(entrada, dict) else entrada,
        capture_output=True, text=True, timeout=20,
        cwd=cwd or tempfile.gettempdir(),
        env={**os.environ, "CLAUDE_PROJECT_DIR": cwd or tempfile.gettempdir()},
    )
    saida = {}
    if p.stdout.strip():
        try:
            saida = json.loads(p.stdout)
        except Exception:
            saida = {"__ilegivel__": p.stdout}
    return p.returncode, saida


def checa(nome, condicao, detalhe=""):
    print(("  ok   " if condicao else "  FALHA ") + nome + ("" if condicao else "  <- " + detalhe))
    if not condicao:
        falhas.append(nome)


def injetou(saida):
    return "additionalContext" in saida.get("hookSpecificOutput", {})


def barrou(saida):
    return saida.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


print("\nR1 — reuso antes de criar")
cod, s = roda("r1-reuso-antes-de-criar.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Write",
    "tool_input": {"file_path": "/proj/db/migrations/0007_add_table.sql"}})
checa("dispara em arquivo de migração", cod == 0 and injetou(s), str(s)[:120])

cod, s = roda("r1-reuso-antes-de-criar.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Bash",
    "tool_input": {"command": "psql -c 'CREATE TABLE precos (id int)'"}})
checa("dispara em CREATE TABLE", cod == 0 and injetou(s), str(s)[:120])

cod, s = roda("r1-reuso-antes-de-criar.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Write",
    "tool_input": {"file_path": "/proj/README.md"}})
checa("silencio em arquivo comum", cod == 0 and not injetou(s), str(s)[:120])

cod, s = roda("r1-reuso-antes-de-criar.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Bash",
    "tool_input": {"command": "npm test"}})
checa("silencio em comando comum", cod == 0 and not injetou(s), str(s)[:120])

cod, s = roda("r1-reuso-antes-de-criar.py", "{isto nao e json")
checa("falha aberta com json quebrado", cod == 0 and not injetou(s), str(s)[:120])

cod, s = roda("r1-reuso-antes-de-criar.py", {"tool_name": "Write"})
checa("falha aberta sem tool_input", cod == 0 and not injetou(s), str(s)[:120])


print("\nR4 — execucao sobre dado real")
cod, s = roda("r4-execucao-sobre-dado-real.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Bash",
    "tool_input": {"command": "python scripts/backfill_precos.py --all"}})
checa("dispara em backfill", cod == 0 and injetou(s), str(s)[:120])

cod, s = roda("r4-execucao-sobre-dado-real.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Bash",
    "tool_input": {"command": "make ingest-discogs"}})
checa("dispara com hifen no nome", cod == 0 and injetou(s), str(s)[:120])

cod, s = roda("r4-execucao-sobre-dado-real.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Bash",
    "tool_input": {"command": "git status"}})
checa("silencio em comando comum", cod == 0 and not injetou(s), str(s)[:120])

for c in ["python scripts/run_backfill.py", "bash jobs/daily_ingest.sh",
          "python manage.py db_migrate", "make data_bulk_load"]:
    cod, s = roda("r4-execucao-sobre-dado-real.py", {
        "hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": c}})
    checa("dispara com prefixo: " + c, cod == 0 and injetou(s), str(s)[:120])

for c in ["python -c 'import collections'", "pytest --collect-only"]:
    cod, s = roda("r4-execucao-sobre-dado-real.py", {
        "hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": c}})
    checa("silencio em: " + c, cod == 0 and not injetou(s), str(s)[:120])

cod, s = roda("r4-execucao-sobre-dado-real.py", {
    "hook_event_name": "PreToolUse", "tool_name": "Write",
    "tool_input": {"file_path": "/proj/backfill.py"}})
checa("silencio em ferramenta que nao e Bash", cod == 0 and not injetou(s), str(s)[:120])

cod, s = roda("r4-execucao-sobre-dado-real.py", "")
checa("falha aberta com entrada vazia", cod == 0 and not injetou(s), str(s)[:120])


print("\nS0 — modo observacao (BARRAR_DE_VERDADE=False, o padrao)")
with tempfile.TemporaryDirectory() as d:
    entrada = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": "./deploy.sh"}, "cwd": d}
    cod, s = roda("s0-indicadores-criticos.py", entrada, cwd=d)
    checa("AVISA sem barrar quando falta a lista", cod == 0 and injetou(s) and not barrou(s), str(s)[:160])


print("\nS0 — modo barrar (BARRAR_DE_VERDADE=True)")
# A variante que barra é escrita FORA da pasta dos hooks, de propósito: se ela
# ficasse aqui e o teste morresse no meio, sobraria um sósia do S0 com o bloqueio
# LIGADO na pasta que você copia para o projeto.
BARRANDO = tempfile.mkdtemp()
orig = open(os.path.join(AQUI, "s0-indicadores-criticos.py"), encoding="utf-8").read()
open(os.path.join(BARRANDO, "_s0_barrando.py"), "w", encoding="utf-8").write(
    orig.replace("BARRAR_DE_VERDADE = False", "BARRAR_DE_VERDADE = True"))

with tempfile.TemporaryDirectory() as d:
    entrada = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": "./deploy.sh"}, "cwd": d}

    cod, s = roda("_s0_barrando.py", entrada, cwd=d)
    checa("BARRA quando o arquivo nao existe", cod == 0 and barrou(s), str(s)[:160])

    with open(os.path.join(d, "indicadores-criticos.md"), "w") as f:
        f.write("# cabecalho, sem indicador nenhum\n")
    cod, s = roda("_s0_barrando.py", entrada, cwd=d)
    checa("BARRA quando so tem comentario (sem pendencia)", cod == 0 and barrou(s), str(s)[:160])

    with open(os.path.join(d, "indicadores-criticos.md"), "a") as f:
        f.write("mediana de preco | se colapsa o cliente perde confianca | nao sei ainda\n")
    cod, s = roda("_s0_barrando.py", entrada, cwd=d)
    checa("libera em silencio com 1 indicador", cod == 0 and not barrou(s) and not s, str(s)[:160])

    cod, s = roda("_s0_barrando.py", {
        "hook_event_name": "PreToolUse", "tool_name": "Bash",
        "tool_input": {"command": "ls -la"}, "cwd": d}, cwd=d)
    checa("silencio em comando que nao toca producao", cod == 0 and not barrou(s), str(s)[:160])

    os.remove(os.path.join(d, "indicadores-criticos.md"))
    cod, s = roda("_s0_barrando.py", {
        "hook_event_name": "PreToolUse", "tool_name": "Bash",
        "tool_input": {"command": "bash deploy_prod.sh"}, "cwd": d}, cwd=d)
    checa("BARRA com underline no nome do script", cod == 0 and barrou(s), str(s)[:160])

    cod, s = roda("_s0_barrando.py", "nao e json", cwd=d)
    checa("falha aberta NAO barra", cod == 0 and not barrou(s), str(s)[:160])

    for c in ["cat docs/deploy.md", "rg -n deploy .", "git log --oneline",
              "NODE_ENV=production npm run build",
              "kubectl apply --dry-run=client -f k8s/dev.yaml"]:
        cod, s = roda("_s0_barrando.py", {
            "hook_event_name": "PreToolUse", "tool_name": "Bash",
            "tool_input": {"command": c}, "cwd": d}, cwd=d)
        checa("NAO barra falso positivo: " + c, cod == 0 and not barrou(s), str(s)[:160])

    with open(os.path.join(d, "indicadores-criticos.md"), "w") as f:
        f.write("# Indicadores criticos do produto\n"
                "# nome | por que o colapso e desastre | onde e calculado\n"
                '# <nome> | <consequencia, uma linha> | <path ou "nao sei ainda">\n')
    cod, s = roda("_s0_barrando.py", {
        "hook_event_name": "PreToolUse", "tool_name": "Bash",
        "tool_input": {"command": "bash deploy.sh"}, "cwd": d}, cwd=d)
    checa("template so com comentario NAO abre o portao", cod == 0 and barrou(s), str(s)[:160])

    with open(os.path.join(d, "indicadores-criticos.md"), "w") as f:
        f.write('# PENDENCIA: setup adiado - "pular por agora".\n')
    cod, s = roda("_s0_barrando.py", {
        "hook_event_name": "PreToolUse", "tool_name": "Bash",
        "tool_input": {"command": "bash deploy.sh"}, "cwd": d}, cwd=d)
    checa("ESCAPE: com pendencia NAO barra, so lembra",
          cod == 0 and not barrou(s) and injetou(s), str(s)[:200])


shutil.rmtree(BARRANDO, ignore_errors=True)

print("\nCada hook funciona sozinho, fora da pasta")
with tempfile.TemporaryDirectory() as solto:
    for nome in ["r1-reuso-antes-de-criar.py", "r4-execucao-sobre-dado-real.py",
                 "s0-indicadores-criticos.py", "r2-artefato-sem-leitor.py"]:
        shutil.copy(os.path.join(AQUI, nome), os.path.join(solto, nome))
    for nome in ["r1-reuso-antes-de-criar.py", "r4-execucao-sobre-dado-real.py",
                 "s0-indicadores-criticos.py", "r2-artefato-sem-leitor.py"]:
        p = subprocess.run([sys.executable, os.path.join(solto, nome)],
                           input="{}", capture_output=True, text=True, timeout=20)
        checa("roda isolado, sem traceback: " + nome,
              p.returncode == 0 and not p.stdout.strip() and "Traceback" not in p.stderr,
              "cod=%s err=%s" % (p.returncode, p.stderr[:80]))
    # e um deles disparando de verdade, sozinho na pasta
    p = subprocess.run([sys.executable, os.path.join(solto, "r4-execucao-sobre-dado-real.py")],
                       input=json.dumps({"tool_name": "Bash",
                                         "tool_input": {"command": "make backfill"}}),
                       capture_output=True, text=True, timeout=20)
    checa("dispara isolado (r4)", p.returncode == 0 and "additionalContext" in p.stdout,
          p.stdout[:80] + p.stderr[:80])


print("\nR2 — artefato sem leitor (precisa de git)")
with tempfile.TemporaryDirectory() as d:
    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d}, cwd=d)
    checa("silencio quando nao ha git", cod == 0 and not injetou(s), str(s)[:120])

    subprocess.run(["git", "init", "-q"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=d, capture_output=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=d, capture_output=True)
    open(os.path.join(d, "leiame.txt"), "w").write("x")
    subprocess.run(["git", "add", "-A"], cwd=d, capture_output=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=d, capture_output=True)

    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d}, cwd=d)
    checa("silencio com git limpo", cod == 0 and not injetou(s), str(s)[:120])

    os.makedirs(os.path.join(d, "db", "migrations"), exist_ok=True)
    open(os.path.join(d, "db", "migrations", "0001.sql"), "w").write("ALTER TABLE x ADD y int;")
    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d}, cwd=d)
    checa("dispara com migracao nova nao commitada", cod == 0 and injetou(s), str(s)[:200])

    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d}, cwd=d)
    checa("NAO repete o aviso no turno seguinte", cod == 0 and not injetou(s), str(s)[:200])

    open(os.path.join(d, "db", "migrations", "0002.sql"), "w").write("ALTER TABLE z ADD w int;")
    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d}, cwd=d)
    checa("avisa de novo quando a lista muda", cod == 0 and injetou(s), str(s)[:200])
    os.remove(os.path.join(d, "db", "migrations", "0002.sql"))

    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d, "stop_hook_active": True}, cwd=d)
    checa("respeita stop_hook_active", cod == 0 and not injetou(s), str(s)[:120])

    open(os.path.join(d, "anotacao.txt"), "w").write("nada a ver")
    os.remove(os.path.join(d, "db", "migrations", "0001.sql"))
    cod, s = roda("r2-artefato-sem-leitor.py",
                  {"hook_event_name": "Stop", "cwd": d}, cwd=d)
    checa("silencio com arquivo fora dos caminhos", cod == 0 and not injetou(s), str(s)[:120])


print("\n" + ("TODOS OS TESTES PASSARAM" if not falhas
              else "FALHARAM: " + ", ".join(falhas)))
sys.exit(1 if falhas else 0)
