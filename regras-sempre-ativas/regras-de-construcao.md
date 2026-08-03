# Regras de construção — manual

As cinco disciplinas em prosa, para colar no `CLAUDE.md` do seu projeto: o que
cada uma faz, quando **não** vale, e o que muda com o hook instalado.

> ⚠️ **Antes de instalar, leia o [aviso de estado no README](../README.md#aviso-de-estado--o-que-tem-lastro-e-o-que-não-tem).**
> A única destas regras que chegou a rodar num projeto real teve **zero disparos
> autônomos demonstrados** em dois dias. Colar a regra não garante que ela dispare.
> Por que isso acontece, e o que a medição pública diz, está lá — aqui é só o
> manual.

---

## Parte 1 — O setup (pré-requisito da R4)

**Por que aparece primeiro aqui:** a R4 depende da lista de indicadores críticos
que este portão cria. Sem a lista, a R4 não tem o que ler. **Mas não instale por
primeiro** — a ordem recomendada está na Parte 3, e nela o S0 entra no terceiro
passo, junto com a R4.

**Hook: sim — e é o único que *pode* barrar, mas vem desligado** —
[`hooks/s0-indicadores-criticos.py`](../hooks/s0-indicadores-criticos.py). Barra
aqui porque a condição é 100% legível por um programa: o arquivo
`indicadores-criticos.md` tem pelo menos uma linha de dado, ou não tem. Não há
julgamento nenhum. Nas outras a condição é interpretação, e barrar por
interpretação trava trabalho legítimo. E é onde barrar mais paga: o S0 é um
portão, e portão que o modelo pode ignorar é sugestão.

O script vem de fábrica em **modo de observação** — avisa sem travar. Rode assim
alguns dias, olhe onde ele dispara de verdade, e só então ligue o bloqueio.
**Resíduo:** o hook garante a **parada**; quem conduz o roteiro de perguntas
continua sendo o modelo, lendo o bloco do S0. Metade vira determinística, metade
segue pedido.

### O texto do S0 mora num arquivo só

O bloco para o CLAUDE.md, o roteiro de perguntas e o formato do
`indicadores-criticos.md` estão em
[`setup-indicadores-criticos.md`](setup-indicadores-criticos.md). **Não estão
copiados aqui de propósito.**

Duas fontes de verdade para o mesmo texto divergem na primeira correção — é o que
a R1 barra, e vale para este repositório também.

---

## Parte 2 — As regras

Cole no `CLAUDE.md` do seu projeto só as regras que você for instalar, na ordem da
Parte 3.

*O `CLAUDE.md` é um arquivo de texto na raiz do projeto, que o Claude Code lê no
começo de toda sessão. Se ele não existir, peça: "crie um CLAUDE.md na raiz deste
projeto".*

> **Disciplinas de construção (cada uma vale só no seu momento; não em toda edição):**
>
> **R1 — Antes de criar estrutura de dados nova, reusar a que já existe.** *Ao criar ou alterar esquema
> persistente — tabela, coluna, migração, modelo, campo agregador ou fonte de dados nova:* verifique se
> já existe estrutura que guarda este dado. **SE existir,** meça o custo de duplicar contra o de reusar e
> apresente a versão que reusa como **default** — só crie se a medição provar que reusar não serve,
> dizendo por quê. **Se não houver candidato, prossiga e crie direto** (uma entidade genuinamente nova
> não exige o teatro da medição). *Não dispara em: lógica dentro de arquivo existente, script novo que só
> lê, correção local. Para caminho que não é de dados — script, fila, serviço, caminho paralelo — a
> pergunta é a mesma, mas nenhum programa a reconhece na hora: chame a skill
> `auditoria-de-caminho-duplicado` antes de construir.*
>
> **R2 — Capacidade pronta aponta consumidor.** *Ao declarar pronta uma capacidade que produz um dado,
> uma evidência ou uma decisão destinada a ser consumida por outro passo do sistema:* aponte quem a
> consome no caminho vivo. Capacidade que nenhum fluxo real lê é peça oca — finge cobertura.
>
> **R3 — Defeito que chegou ao produto vira teste que trava a regressão.** *Ao fechar a correção de um
> defeito que EFETIVAMENTE CHEGOU ao usuário ou ao dado real publicado:* entregue com um teste que
> **falha se o defeito voltar**. O critério de admissão é ter chegado ao produto/dado publicado, não ter
> apenas existido — bug pego em desenvolvimento, antes de publicar, **não** obriga teste permanente. Se o
> defeito não é reproduzível em teste (dado externo/gated), diga por que e o que trava no lugar.
>
> **R4 — Execução sobre dado real não-controlado.** *Ao rodar carga, migração, backfill, fonte nova ou
> expansão de escopo sobre dado que você não controla:* exponha pouco antes da base inteira; olhe o
> indicador de saúde a cada toque; se quebrar, **conter (preservando o que já estava certo) → corrigir →
> publicar**. **E:** se o que você tocou alimenta um indicador da *lista de indicadores críticos*,
> verifique se esse indicador tem **alarme permanente** que dispara sozinho quando desaba — se não tem, é
> peça oca de vigilância; registre o gap — e o próximo passo é construir o monitor (tarefa de código do
> PM), cujo molde está na peça de vigilância de execução. *Não dispara em: mudança de código que não executa carga/
> migração/backfill sobre dado real; nem quando o que foi tocado não alimenta nenhum indicador da lista.*

### O que cada regra faz

Três campos por regra: **Pega** (o que ela alcança), **NÃO dispara** (quando ela
não vale — evita aplicá-la demais) e **Hook** (o que muda quando você instala o
programa correspondente, e o que continua não coberto).

Quatro das cinco viram hook — R1, R2, R4 e S0. A R3 não, e o motivo está nela. Os
scripts e o manual de instalação estão em [`hooks/`](../hooks/README.md).

**R1**
- **Pega:** criação ou alteração de esquema persistente — tabela, coluna, migração, modelo, campo
  agregador, fonte de dados nova — quando já existe estrutura que guarda aquele dado.
- **NÃO dispara:** quando não há candidato a reuso (entidade genuinamente nova), em fix local, em lógica
  dentro de função existente, ou em leitura/auditoria. **E não dispara no que não é estrutura de dados**
  — script, fila, serviço, caminho paralelo de coleta: a pergunta é a mesma, mas nenhum programa a
  reconhece na hora. Para esses, a skill `auditoria-de-caminho-duplicado`, que você invoca antes de
  construir.
- **Hook: sim, injeta** — [`hooks/r1-reuso-antes-de-criar.py`](../hooks/r1-reuso-antes-de-criar.py).
  Roda antes de gravar arquivo de estrutura (`Write`, `Edit`) ou de rodar comando que a cria (`Bash`).
  Injeta e não barra porque a pergunta central — *já existe estrutura que guarda este dado?* — é
  julgamento sobre o seu código, que programa nenhum responde. **Resíduo:** estrutura que nasce dentro
  de arquivo já existente chega como `Edit`, e ali o hook não distingue "acrescentei um campo agregador"
  de "arrumei um typo". Nessa faixa a precisão é baixa — injetar é tolerável, barrar não seria.
  **Por que o texto da regra é mais estreito do que era:** ele foi encolhido em 31/07/2026 até descrever
  o que o hook enxerga. A versão anterior falava em módulo, caminho de decisão e estado — raio que nenhum
  programa alcança e que a regra, medida, não alcançou sozinha. Regra que promete mais que o mecanismo
  fabrica cobertura falsa.

**R2**
- **Pega:** declarar pronta uma capacidade que produz dado/evidência/decisão sem apontar quem a consome.
- **NÃO dispara:** refactor, mudança de exibição/UI (consumida pelo olho, não por um passo a jusante), doc.
- **Hook: sim, injeta** — [`hooks/r2-artefato-sem-leitor.py`](../hooks/r2-artefato-sem-leitor.py).
  A pergunta que torna isto viável não é *"o modelo declarou pronto?"* — isso um programa não lê. É
  outra, que ele lê: **este turno mexeu em estrutura persistente?** Usa `git` para saber o que mudou e,
  se mudou, entrega a pergunta da R2 ao fim do turno. **Resíduo:** ele sabe QUE a estrutura foi tocada;
  não procura o consumidor. Para o veredito com evidência apontável existe a skill
  `auditoria-de-peca-oca`. Sem `git` no projeto, o hook não faz nada — de propósito: melhor não disparar
  do que disparar por adivinhação.

**R3**
- **Pega:** um fix de defeito que chegou ao usuário/dado publicado sem um teste que trave a volta.
- **NÃO dispara:** bug pego em desenvolvimento, antes de publicar.
- **Hook: não, e é de propósito.** O evento existe — dá para interceptar o comando de commit ou de
  publicação. O que não existe é a **condição**: saber se aquele defeito chegou ao usuário ou ao dado
  publicado é uma classificação que não está no comando nem no arquivo. Um hook em toda edição
  dispararia em tudo. Em compensação, é a regra cujo gatilho o **modelo** reconhece melhor de todas:
  quando você pede a correção, você diz onde o bug apareceu — a informação chega na conversa. Fica
  regra em prosa mais a skill `auditoria-de-teste-cicatriz`.

**R4**
- **Pega:** execução sobre dado real não-controlado sem expor-pouco / olhar-o-indicador / conter-antes-de-
  corrigir; e (emenda) tocar a entrada de um indicador crítico que não tem alarme permanente.
- **NÃO dispara:** mudança de código que não executa carga/migração/backfill sobre dado real; ou quando o
  que foi tocado não alimenta nenhum indicador da lista.
- **Hook: sim, injeta** — [`hooks/r4-execucao-sobre-dado-real.py`](../hooks/r4-execucao-sobre-dado-real.py).
  É o caso mais limpo: carga, migração e backfill **são comandos**, e a lista deles num projeto é finita
  e enumerável. Injeta e não barra porque travar toda carga travaria o trabalho normal — o que falta não
  é permissão, é a disciplina chegar na hora. **Resíduo:** o hook avisa **antes**. Olhar o indicador a
  cada toque e a ordem conter → corrigir → publicar acontecem durante e depois, e nenhum hook faz
  contenção — isso é o julgamento no calor, que a peça de vigilância já diz não se automatizar.

**Não existe regra para carimbar-a-decisão**, e é de propósito: como regra
sempre-ativa ela empurraria carimbo e materialização prematuros — a própria
inflação que a R1 evita. O julgamento dela vive na peça `memoria/` e na skill
`auditoria-de-decisao-nao-carimbada`, que você invoca quando desconfia.

---

## Parte 3 — Ordem de instalação recomendada

Não instale tudo de uma vez. **Instalar as cinco de uma vez impede saber qual
virou ruído** — se algo começar a incomodar, você não saberá quem foi. A ordem
que reduz o risco:

1. **R1 + R2 primeiro** — atacam a correção que incha e têm o gatilho mais limpo.
2. **Rode dias de construção real e observe** — elas disparam no momento certo, ou
   atrapalham?
3. **S0 + R4 juntas** (uma depende da outra) só depois — porque S0 adiciona
   fricção no primeiro deploy e precisa de teste com um PM real.
4. **R3 quando quiser cobertura de regressão.**
