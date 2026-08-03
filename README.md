# Travas de produto

Escrevi estes artefatos a partir de erros reais que vi acontecer construindo um
produto com IA, sem um time de engenharia para revisar o que a IA escreve. Cada
um destila um julgamento que precisei aprender na marra, num erro concreto e
datado. Servem a um tipo específico de produto: o que **afirma uma verdade** —
emite um número, um preço, um veredito — onde o erro custa a confiança de quem
usa. Não a um produto que só conversa.

## O que é

Não é um framework nem um método. É um punhado de disciplinas, cada uma amarrada
a uma cicatriz: o erro que a originou está datado. Há quatro formas de material, e
a diferença entre elas é o que não se adivinha sozinho.

**Esta página condensa tudo o que você precisa saber antes de instalar qualquer
coisa:** o que é cada forma, qual delas funciona sem depender da memória do
modelo, de onde veio cada disciplina, e o que já foi medido — inclusive o que
falhou. As **peças** contam cada erro por dentro; `regras-sempre-ativas/` e
`hooks/` são manuais de instalação.

## Como usar — quatro formas, quatro momentos

- **As peças** — você **lê** e adapta ao seu produto. Cada uma é um princípio mais
  a cicatriz de onde veio: [peça oca](verificacao/auditoria-de-peca-oca.md),
  [carimbar a decisão](memoria/carimbar-a-decisao.md),
  [teste-cicatriz](prevencao/teste-cicatriz.md),
  [vigilância de execução](vigilancia/vigilancia-de-execucao.md).
- **As skills** ([`skills/`](skills/)) — você copia a pasta da skill para
  `.claude/skills/` do seu projeto e a chama pelo nome quando **desconfia de algo
  já construído** ("isto está mesmo ligado?", "esta decisão ficou registrada?") ou
  **antes de construir mais um caminho**. Precisam do código aberto para
  inspecionar — sem ele, o veredito honesto é "não sei". São cinco passos e
  nenhum exige abrir arquivo de código:
  [instalar e usar](skills/README.md).
- **As regras** (`regras-sempre-ativas/`) — você **cola no `CLAUDE.md`** do seu
  projeto para que o julgamento esteja presente durante a construção, e não só
  quando você desconfia. Incluem um setup que roda uma vez, para você declarar o
  que não pode colapsar antes de tocar produção. **Antes de instalar, leia o aviso
  de estado no fim desta página: colar a regra não garante que ela dispare.**
- **Os hooks** ([`hooks/`](hooks/)) — você **copia para `.claude/hooks/`** do seu
  projeto e registra no `settings.json`. São programas que o Claude Code roda num
  momento fixo — antes de um comando, antes de gravar um arquivo, ao terminar de
  responder. **É a única forma aqui que não depende de o modelo lembrar de nada.**
  Quatro das cinco regras viram hook; a R3 não, e o motivo está escrito nela.
  Exigem Python 3 — [instalação e medição](hooks/README.md).

A distinção que importa, e que ninguém adivinha na primeira leitura: **peça =
quando você desconfia; regra = tentativa de estar presente o tempo todo.** A
skill você chama quando quer o veredito com evidência: é a auditoria feita, não o
princípio para ler. Quatro das cinco skills têm peça de tema correspondente; a
`auditoria-de-caminho-duplicado` não tem — ela nasceu de uma regra que não
disparou, e a cicatriz dela mora dentro do próprio arquivo da skill.

## Só uma destas formas age sem depender de memória

Peça, skill e regra são texto que o modelo lê. A peça você lê; a skill você chama
pelo nome; a regra depende de o modelo lembrar dela no meio de todo o resto do
contexto — memória que decai conforme o contexto cresce e os turnos se acumulam.
Vale inclusive para o S0, que manda "BLOQUEIE a ação": é um imperativo ao modelo,
não uma trava.

Uma ressalva que eu precisei corrigir depois de conferir na documentação: **a
skill também pode ser acionada pelo próprio modelo**, que lê a descrição dela e
decide que é o caso. Isso não é exceção à frase acima — é a mesma coisa por outro
caminho. Acionar assim exige reconhecer o momento, que é exatamente o que a
medição abaixo mostra falhando. Conte com a chamada pelo nome; o resto é tiro
extra de graça.

Não é teoria: a única destas regras que chegou a rodar num projeto real teve
**zero disparos autônomos demonstrados** em dois dias — a medição e as ressalvas
estão no aviso de estado, no fim desta página.

O **hook** é a exceção: um programa que o Claude Code executa num momento fixo —
antes de um comando, antes de gravar um arquivo, ao terminar de responder. Ele roda
tenha o modelo lembrado ou não. A diferença não é de grau, é de natureza: hook é
programa; peça, skill e regra são pedidos.

**Um hook pode fazer duas coisas, e o custo é muito diferente.** *Injetar* põe o
texto da regra na frente do modelo naquele instante — disparar errado custa alguns
tokens. *Barrar* impede a ação — disparar errado trava trabalho legítimo. Daí o
critério que organiza a pasta [`hooks/`](hooks/): **barre quando a condição pode
ser lida por um programa; injete quando a condição é julgamento.** Dos quatro que
estão lá, três só injetam; só o do S0 barra, e vem de fábrica avisando sem travar.

**Uma disciplina não vira hook, e o motivo não é o que parece.** Para a R3 o
evento existe — dá para interceptar o comando de publicação. O que falta é o
programa conseguir **julgar naquele instante** se a regra se aplica: saber se
aquele defeito chegou ao usuário é uma classificação que só você tem. Ela segue
sendo prosa mais a skill que você invoca — e isso não é consolo: é o mecanismo
certo para condição que exige julgamento.

Nada disso resolve sozinho. O hook entrega a disciplina na hora certa; **cumprir
continua sendo do modelo e seu.** Não tente ordenar peça, skill e regra por
confiabilidade entre si: não há medição que sustente uma ordem entre as três, e
este repositório não vai fingir que há.

## De onde veio cada disciplina

Nenhuma nasceu de teoria. Cada uma tem um incidente datado atrás dela — é a regra
de admissão deste repositório, logo abaixo.

| | Cicatriz |
|---|---|
| **R1** — reusar antes de criar estrutura de dados | **P12a, 24–25/jul/2026.** Uma proposta que acrescentava um bloco agregador (mais uma fonte de verdade) foi barrada e trocada por um carimbo derivado, depois de medir o que já existia. É a parte da cicatriz que a R1 estreitada ainda pega: campo agregador é esquema. O mesmo julgamento agiu na auditoria de 11/06/2026 e na cadeia D2.24→D2.30 (04–05/jul/2026). |
| **Caminho duplicado** — skill, não regra | **28 e 29/07/2026.** No dia 28, a pergunta feita sob invocação derrubou uma spec de cinco estruturas novas para uma. No dia 29, a mesma pergunta como regra sempre-ativa não disparou, e nasceu um caminho paralelo de coleta. É a parte que saiu da R1 quando ela foi estreitada. |
| **R2** — capacidade pronta aponta consumidor | **16/06/2026.** Um contrato de evidência construído e nunca plugado, declarado pronto sem consumidor no caminho vivo. É a peça oca. |
| **R3** — defeito vira teste-cicatriz | **30/06/2026.** Um item já corrigido cinco vezes voltou a passar por um caminho novo: uma funcionalidade construída depois produziu evidência a favor dele. O teste nasceu no dia seguinte. |
| **R4** — execução sobre dado real | **15/07/2026.** Uma carga fez um identificador comum virar critério de corte e barrou itens corretos em massa. |
| **S0** — declarar indicadores críticos | O mesmo 15/07: não havia número declarado como crítico, então não havia o que alarmar. |

## A regra de admissão

Só entra aqui artefato com **cicatriz real e datada**. Sem um incidente concreto
por trás, não entra. E uma peça pode **sair** quando deixar de refletir a prática
— não há compromisso de manter o que virou folclore. É essa regra que impede este
repositório de virar os outros: os que têm mil skills, nenhuma data, e ninguém
sabe qual funciona.

## Aviso de estado — o que tem lastro e o que não tem

Nem tudo aqui tem o mesmo lastro, e não vou fingir que tem:

- **As skills** foram exercitadas contra código real; uma delas, contra uma stack
  diferente da minha. Têm lastro de uso, ainda que pequeno — **exceto a de
  teste-cicatriz**, que é interpretativa e nunca foi usada para valer: o próprio
  arquivo dela manda tratar o primeiro uso como experimento.
- **A `auditoria-de-caminho-duplicado`** é de 31/07/2026 e **nunca rodou como
  skill**. O que ela tem é a medição que a originou: a mesma pergunta, feita sob
  invocação contra uma spec já escrita, derrubou a spec de cinco estruturas novas
  para uma em 28/07 — e a mesma pergunta, instalada como regra sempre-ativa, teve
  zero disparos demonstráveis no dia seguinte. Lastro de caso, nenhum de uso na
  forma de skill.
- **As regras** têm lastro de **caso** — cada uma nasceu de um incidente datado.
  De **uso**, o pouco que existe é **negativo**, e está medido logo abaixo. Estão
  **em observação**: instale poucas por vez, remova a que virar ruído — e **não
  conte a regra instalada como problema resolvido**.
- **O setup S0** é o menos validado de tudo: nunca rodou com um PM real, só em
  simulação. O risco conhecido é o escape ("pular por agora") virar hábito se a
  primeira ação que toca produção for sempre urgência — aí a lista nunca nasce.
  **É uma aposta declarada.**
- **Os hooks** são os mais novos e os menos rodados: nasceram em 30/07/2026, da
  medição que está logo abaixo. O código está testado — 43 casos cobrindo disparo, silêncio e
  falha aberta —, mas **os padrões que vêm de fábrica são exemplos genéricos, não
  medição**. Eles provam que o programa funciona como escrito, não que dispara nos
  momentos certos do seu projeto. Neste aqui, dois hooks de lembrete já foram
  medidos e descartados — um teve 10% de precisão (3 acertos em 30 disparos); o
  outro pegaria 2 de 9 casos e dispararia em 41% de tudo. Desenho plausível erra.
  Rode em observação antes de deixar qualquer um barrar.

Não venda como pronto o que ainda está sendo observado.

### A medição que mudou o desenho — R1, 27 a 29/07/2026

A R1 foi instalada num projeto real em 27/07. Em dois dias de construção densa,
uma auditoria do registro encontrou **zero disparos autônomos demonstrados**. Nos
quatro episódios em que ela aparece agindo, três foram **provocados** por um
pedido explícito de ceticismo no prompt ("valide contra o código real"); o quarto
é indeterminável.

E há uma cicatriz datada: em 29/07 — dois dias depois da instalação — foi criado
um script com fila, cadência e disjuntor próprios, num projeto onde fila e
cadência já existiam e estavam em uso. O candidato a reuso era óbvio e nenhuma
medição foi escrita. **No texto largo que estava instalado, a R1 cobria esse caso
e silenciou nele.**

Um dia antes, em 28/07, a mesma pergunta feita **sob invocação** contra uma spec
já escrita derrubou a spec de cinco estruturas novas para uma. Os dois episódios,
com um dia de diferença, são a mesma disciplina em dois formatos — e é a diferença
entre eles que explica o resto: como regra, o modelo precisava reconhecer sozinho
que estava no momento de criar; invocada, a pergunta chega sobre um texto pronto
para classificar.

**Foi essa medição que estreitou a R1 em 31/07.** O texto da regra encolheu até
descrever o que o hook enxerga — esquema de banco —, e o caso de 29/07, que é
script e fila, saiu da regra e virou a skill `auditoria-de-caminho-duplicado`. O
efeito colateral está dito de propósito: **a R1 de hoje não pegaria o incidente
que a mediu.** Ela deixou de prometer aquele raio porque nunca o entregou; quem
entrega é uma skill que você invoca, e invocar depende de você lembrar.

*Ressalva de método, para você não confiar demais neste número:* nesse projeto a
R1 é indistinguível de uma regra pré-existente — o registro cita as duas como
sinônimos. Não dá para separar o efeito de uma da outra. O que a auditoria
sustenta é a **ausência de disparo autônomo demonstrável**, não a culpa da R1
isoladamente.

**O que isto muda no uso:** continua valendo instalar poucas por vez e remover a
que virar ruído. Deixa de valer **medir a regra pelo silêncio dela** — silêncio
não é "não houve caso"; pode ser a regra não tendo disparado no caso que havia.

### Não é caso isolado — o que a medição pública diz

O benchmark **HANDBOOK.md** (Surge AI, [arXiv:2607.25398](https://arxiv.org/abs/2607.25398),
28/07/2026) põe agentes de fronteira para executar tarefas sob um manual de 20 a
124 páginas, com 824 critérios programáticos. A maioria das 30 configurações
testadas fica **abaixo de 25%** de aprovação estrita; o teto é **36,2%**. Mesmo a
melhor configuração testada falha cerca de 2 em cada 3 tarefas — com o manual ali,
inteiro, no contexto.

O achado que mais importa para quem instala regras não é o número, é o modo de
falha. Nas palavras do paper:

> *"Nearly every failed trajectory ends with a confident statement that the
> handbook was followed, frequently citing the specific sections that violated it.
> The reports are detailed, structured, and wrong."*

É por isso que "instalei a regra" não é evidência de nada, e "o Claude disse que
seguiu" é evidência de menos ainda. A única evidência que vale é a medição escrita:
o que foi comparado, contra o quê, com que resultado.

*Ressalva de escopo, para você não citar isto além do que ele mede:* são 65
tarefas agênticas em domínios de negócio (finanças, faturamento médico, seguros,
logística, RH), com rubrica programática. Não mede julgamento nem qualidade de
código.

## Os manuais

O *como fazer* de cada coisa está no arquivo dela:

- [`regras-sempre-ativas/regras-de-construcao.md`](regras-sempre-ativas/regras-de-construcao.md)
  — as cinco regras em prosa, o que cada uma faz, quando não vale, e a ordem de
  instalação recomendada.
- [`regras-sempre-ativas/setup-indicadores-criticos.md`](regras-sempre-ativas/setup-indicadores-criticos.md)
  — o texto do S0 e o roteiro que ele conduz.
- [`hooks/README.md`](hooks/README.md) — instalar, medir e remover os hooks, em
  seis passos.
- [`skills/README.md`](skills/README.md) — instalar, chamar e remover as skills,
  em cinco passos, e o que esperar de uma resposta de auditoria.
- As quatro peças e as cinco skills se explicam dentro de si — os links estão em
  *Como usar*, mais acima.
