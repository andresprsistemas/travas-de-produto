---
name: auditoria-de-caminho-duplicado
description: >-
  Use quando houver proposta de construir algo que talvez já exista no projeto —
  outro script de coleta, outra fila, outro serviço, outra tabela, outro caminho
  de decisão — e a dúvida for se isto vira caminho paralelo ou segunda fonte de
  verdade. Dispara quando o usuário pergunta "isto duplica o que já temos?", "já
  existe um caminho que faz isso?", "precisa mesmo criar outro?", ou quando pede
  revisão de uma spec ou de um plano antes de construir. Precisa de acesso ao
  código para inspecionar. Use só ANTES de construir: se a coisa já está
  construída e a dúvida é se ela está ligada ou é consumida, a skill é a
  `auditoria-de-peca-oca`.
---

# Auditoria de caminho duplicado

Descobrir se o que está prestes a ser construído já tem caminho no projeto, e
obrigar a comparação entre os dois a ficar escrita.

## Princípio

Caminho paralelo não custa o trabalho de escrevê-lo: custa o estado passando a
viver em dois lugares e alguém tendo que mantê-los iguais para sempre. Quando os
dois divergem — e divergem na primeira correção feita só de um lado — o sistema
passa a afirmar duas verdades sem saber qual está usando.

"É mais simples assim" e "é temporário" não são medição. O caminho paralelo
temporário é a forma mais comum de duplicação que fica.

## Quando vale, e quando não

Vale antes de construir. Depois de construído, o caso é outro e a skill é a
`auditoria-de-peca-oca`. Não vale para correção local, lógica dentro de função
existente, nem para entidade genuinamente nova: quando não há candidato a reuso,
criar direto é o certo, e exigir medição vira teatro.

## Procedimento

Peça duas coisas ao usuário: **o que vai ser construído** e **onde a proposta
está escrita** (spec, plano, mensagem). Depois responda às três perguntas, cada
uma com um LUGAR concreto no repositório — buscando de fato, não deduzindo:

1. **Que caminho existente faz, ou quase faz, este trabalho?** Busque por
   função, não por nome: o que já grava este dado, o que já controla esta
   cadência, o que já fala com esta fonte externa, o que já decide isto. Relate
   **onde você procurou** — caminhos e padrões de busca —, não só o que achou.
   "Não achei" só conta acompanhado da lista de onde se procurou.
2. **Qual o custo de duplicar contra o de reusar?** Contável dos dois lados.
   *Reusar:* qual arquivo existente muda, quantos pontos o chamam, e quais
   testes cobrem hoje o ponto que muda, com caminho — se nenhum, escreva
   "nenhum". *Duplicar:* quantos arquivos nascem, **qual estado passa a existir
   em dois lugares**, e qual documento ou dono declarado responde pela sincronia
   dos dois — se não houver, escreva "sem dono declarado", que é um custo, não
   uma lacuna. Sem os dois lados não há medição, há preferência.
3. **A versão que reusa está escrita?** A resposta precisa conter a alternativa
   descrita o bastante para ser comparada: qual caminho existente, o que muda
   dentro dele. Se não está escrita, esta pergunta falha mesmo com as duas
   primeiras respondidas.

## Regra dura

Você NÃO pode aprovar a construção sem as três respondidas com lugar concreto.
Ausência de candidato só vale com a lista de onde você buscou: uma busca que não
achou não é ausência. Nunca preencha a lacuna com suposição ("provavelmente não
tem nada parecido").

E desconfie especialmente do caminho paralelo que se justifica por urgência ou
por ser de desenvolvimento: é o formato do incidente que originou esta auditoria.

## Veredito

- Existe caminho, a versão que reusa está escrita e a medição não mostra
  impedimento → **REUSAR** (cite o caminho e o que muda dentro dele).
- Existe caminho e a versão que reusa não está escrita →
  **DUPLICAÇÃO NÃO MEDIDA**.
- Existe caminho, a medição está escrita e mostra que reusar não serve →
  **CONSTRUIR JUSTIFICADO** (cite a linha da medição).
- Buscou nos lugares listados e não há caminho → **CAMINHO NOVO LEGÍTIMO**.
- Não deu para inspecionar o código → **NÃO SEI** (falha de auditoria).

A resposta termina OBRIGATORIAMENTE com uma linha `Veredito: X`. Achados fora
destas três perguntas vêm depois da linha de veredito, nunca antes.

## De onde veio, e o que ela não faz

**28/07/2026 — o caso positivo, e é o motivo desta skill existir.** A mesma
pergunta, feita sob invocação contra uma spec já escrita, derrubou a spec de
**cinco estruturas novas para uma**. O auditor tinha o texto pronto para
classificar.

**29/07/2026 — o caso negativo, no dia seguinte.** Num projeto onde já existiam
fila e cadência de coleta, em uso e com dois catálogos drenados, nasceu um script
com fila, cadência e disjuntor próprios, num caminho paralelo de 4 a 15 vezes
mais agressivo que o canônico. Não há medição escrita de por que o caminho
existente não servia. A mesma disciplina estava instalada como regra
sempre-ativa desde 27/07, e a auditoria do registro daquele trabalho encontrou
**zero disparos autônomos demonstráveis** — com a ressalva de método registrada
no README do repositório.

Os dois casos, com um dia de diferença, são a mesma pergunta em dois formatos:
como regra em prosa, o modelo precisava reconhecer sozinho que estava no momento
de criar, e não reconheceu; **invocada, a pergunta chega sobre um texto já
escrito, que é classificável.**

Por isso a forma em que esta skill tem evidência é a chamada pelo nome —
`/auditoria-de-caminho-duplicado`. Ela **também** pode ser acionada sozinha, pelo
texto desta `description`, e isso é um tiro extra de graça; mas não conte com ele.
Reconhecer o momento é justamente a parte que falhou na medição de 29/07.
