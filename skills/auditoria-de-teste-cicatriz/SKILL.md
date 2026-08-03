---
name: auditoria-de-teste-cicatriz
description: >-
  Use quando o usuário quer saber se um erro/incidente passado tem cobertura
  durável, ou se um teste de regressão existente é teatral — passaria mesmo com
  o bug de volta. Dispara quando ele pergunta se um caso "está protegido", se o
  teste "pegaria de novo", se a suíte "cobre o incidente", ou se um teste "está
  preso a um caso específico". Audita a cobertura de um risco indicado com
  evidência apontável. É a mais interpretativa das auditorias deste repositório:
  julgar "esse teste pegaria o bug de volta?" exige raciocinar sobre a semântica
  do teste, não só localizar arquivo — trate o primeiro uso como experimento.
  Precisa de acesso ao código.
---

# Auditoria de teste-cicatriz

Descobrir se um risco/incidente passado tem cobertura durável, e se o teste que
o cobre é real ou teatral.

Esta é a auditoria menos validada deste repositório: julgar "esse teste falharia
se o erro voltasse?" é interpretação, não só busca. Trate o primeiro uso como
experimento — reporte a incerteza e prefira NÃO SEI a forçar um veredito.

## Princípio

O permanente é a cobertura do risco, não o teste original. Um teste que passaria
mesmo com o bug de volta é pior que nenhum: fabrica cobertura falsa. Só vale
com prova de onde.

## Procedimento

Peça ao usuário o risco/incidente a auditar (o erro que já aconteceu). Depois
responda às três perguntas, cada uma com um LUGAR concreto no código:

1. **Existe um guarda?** Ache uma verificação que trava a publicação quando este
   erro volta. Aponte o lugar, ou NÃO ENCONTRADO.
2. **O guarda é real ou teatral?** Ele exercita o CAMINHO onde o erro ocorreu e
   FALHARIA se o erro voltasse? Um teste que afirma só sobre entradas fabricadas,
   ou só sobre a forma do código, pode passar com o bug de volta — teatral. Diga
   POR QUE passaria ou falharia, não só que existe.
3. **A cobertura é durável ou frágil?** Congela o COMPORTAMENTO (uma regra geral
   que pega o mecanismo e outros casos iguais) ou uma INSTÂNCIA (um caso ou
   identificador específico que some se o dado sair)? Aponte qual.

## Regra dura

Você NÃO pode responder "coberto" sem apontar o guarda E dizer por que ele
falharia com o erro de volta. Nunca preencha a lacuna com suposição ("deve haver
um teste", "o nome sugere que cobre"): ausência de evidência nunca vira
aprovação. Um teste com o nome do incidente não prova cobertura — leia o que ele
afirma.

## Veredito

Distinga buscar e não achar de não conseguir buscar: inspecionou e concluiu →
veredito abaixo; não conseguiu inspecionar (sem acesso ao código, sem permissão,
stack que não dá para inspecionar), ou não deu para julgar a semântica com
confiança → NÃO SEI (falha de auditoria).

- Guarda existe, exercita o caminho real e congela o comportamento (regra geral)
  → **COBERTO DURÁVEL**.
- Guarda existe e é real, mas preso a uma instância/identificador específico →
  **COBERTO FRÁGIL** (aponte o acoplamento).
- Guarda existe mas passaria com o bug de volta → **TEATRAL** (diga por quê).
- Nenhum guarda para o risco → **DESCOBERTO**.
- Não deu para inspecionar ou julgar → **NÃO SEI**.

A resposta termina OBRIGATORIAMENTE com uma linha `Veredito: X`, onde X é um
dos rótulos acima — sem ela, a auditoria não está concluída. Achados fora das
perguntas desta auditoria vêm DEPOIS da linha de veredito, nunca antes nem
misturados às respostas.
