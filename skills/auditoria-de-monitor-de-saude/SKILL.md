---
name: auditoria-de-monitor-de-saude
description: >-
  Use quando o usuário quer saber se existe uma trava que o AVISA sozinha caso
  um número crítico do produto desabe — um alarme de efeito. Dispara quando ele
  pergunta "se isso despencar, alguém me avisa?", "tem monitor disso?", "isso é
  vigiado ou só calculado?". Ela verifica o monitor de um indicador que O USUÁRIO
  declara — NÃO descobre qual indicador importa; isso é julgamento de produto, e
  é dele.
---

# Auditoria de monitor de saúde

Descobrir se um número crítico do produto tem uma trava que dispara sozinha
quando ele se move demais — ou se ninguém está vigiando o efeito.

## Princípio

A causa de um desastre é imprevisível; o efeito não — ele sempre aparece como um
número de saúde que se move demais, de repente. Esse efeito é vigiável de
antemão, sem conhecer a causa. Um número que é só calculado e exibido, mas que
nada dispara quando desaba, é peça oca de vigilância: parece vigiado, não é.

## Procedimento

O usuário DECLARA o indicador crítico — o número que, se desabar, significa
desastre. A skill não sugere qual é (isso é julgamento de produto). Depois,
responda com um LUGAR concreto no código/configuração, buscando de fato:

1. **O indicador é calculado em algum lugar?** Ache onde o número nasce. Se nem
   o cálculo existe, não há o que monitorar — reporte.
2. **Existe uma trava que DISPARA quando ele cruza um limite?** Ache o ponto
   apontável que falha um gate, emite alerta ou bloqueia a publicação quando o
   número passa de um limite. Calcular, exibir num painel ou logar o número NÃO
   conta — tem que disparar uma ação.
3. **A trava roda sozinha e de forma registrada?** Vale se é automática,
   versionada, agendada, ou um gate de publicação que sempre roda. NÃO vale a que
   depende de alguém lembrar de olhar ou de rodar um check à mão.

## Regra dura

Você NÃO pode responder "está monitorado" sem apontar o lugar exato da trava que
dispara. Exibir o número num painel que ninguém vigia não é monitor; um check que
só roda quando alguém lembra não é monitor. Ausência de evidência nunca vira
aprovação.

## Veredito

Distinga buscar e não achar de não conseguir buscar: inspecionou e concluiu →
veredito abaixo; não conseguiu inspecionar (sem acesso ao código, sem permissão)
→ NÃO SEI (falha de auditoria).

- Trava apontável que dispara ao indicador cruzar o limite, rodando sozinha →
  **MONITORADO** (aponte o lugar).
- Indicador calculado/exibido mas nada dispara quando ele desaba, OU trava que só
  roda quando alguém lembra → **NÃO MONITORADO** (peça oca de vigilância; diga
  qual dos dois).
- Nem o cálculo do indicador existe → **NÃO MONITORADO** (não há o que vigiar).
- Não deu para inspecionar → **NÃO SEI**, dizendo o que faltou.

**Próximo passo quando NÃO MONITORADO:** o veredito não é o fim — construir o
alarme é tarefa de código do PM. Em forma curta, o molde: vigia um indicador que
o PM declarou crítico; dispara sozinho quando ele passa de um limite que o PM
define; roda permanente, independente do que mudou. O molde completo está na peça
de vigilância de execução (seção "O molde do monitor",
`../../vigilancia/vigilancia-de-execucao.md`). A ferramenta aponta a falta e dá o
molde; a construção e o limite são do PM.

A resposta termina OBRIGATORIAMENTE com uma linha `Veredito: X`, onde X é um dos
rótulos acima — sem ela, a auditoria não está concluída. Achados fora desta
auditoria vêm DEPOIS da linha de veredito, nunca antes nem misturados.
