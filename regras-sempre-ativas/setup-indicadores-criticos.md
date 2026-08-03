# Setup obrigatório: declarar os indicadores críticos

Artefato de tipo diferente das peças e skills: não audita nada e não espera ser
chamado por nome. É uma instrução para o Claude parar **uma vez**, na primeira
ação que toca produção, e pedir ao PM que declare o que não pode colapsar — antes
de construir. Depois que a lista existe, ele silencia.

**O que este texto é, e o que ele não é.** Abaixo está escrito "BLOQUEIE a ação",
e isso é um imperativo ao modelo, não uma trava. Um bloco em CLAUDE.md não tem
como barrar coisa alguma: ele pede que o modelo pare por conta própria, e esse
pedido compete com todo o resto do contexto.

**A versão que barra de verdade existe, e é um hook:**
[`hooks/s0-indicadores-criticos.py`](../hooks/s0-indicadores-criticos.py). Ele roda
antes do comando que toca produção, lê o `indicadores-criticos.md` e decide — se há
pelo menos uma linha de dado, libera em silêncio; se não há, barra. É o **único
hook deste repositório que pode barrar**, e pode porque aqui a condição é inteiramente
legível por um programa: o arquivo tem linha ou não tem, sem julgamento no meio.
Vem de fábrica em modo de observação — avisa sem travar —, para você ver onde ele
dispara antes de ligar o bloqueio.

O texto abaixo continua valendo mesmo com o hook instalado: o hook garante a
**parada**; quem conduz o roteiro de perguntas é o modelo, lendo este bloco.

E a ressalva de lastro: este é o artefato **menos validado** do repositório —
nunca rodou com um PM real, só em simulação.

---

## Bloco para o CLAUDE.md (a regra de setup)

> **S0 — Setup obrigatório: declarar os indicadores críticos (dispara uma vez).**
>
> *Gatilho:* na primeira ação do PM que toca produção — deploy, migração, carga,
> ou qualquer escrita em dado real — **antes de executar**, verifique o arquivo
> `indicadores-criticos.md`. Se ele tem **pelo menos um indicador confirmado**
> (uma linha de dado, não só comentário/pendência) → **silêncio permanente**; não
> repita, exceto se o PM pedir "revisar indicadores críticos". Se o arquivo não
> existe, ou tem só comentário → **BLOQUEIE a ação** e conduza o roteiro abaixo
> antes de executar qualquer coisa. Se já houver linha de **pendência**, não
> bloqueie: apenas lembre e prossiga.
>
> *Escape rastreável:* o PM pode responder **"pular por agora"**. Aí não rode o
> roteiro: grave no arquivo uma linha de **pendência** com o momento e
> **prossiga** com a ação. Pendência não conta como indicador confirmado — daí em
> diante, **lembre** na próxima ação que toca produção, sem bloquear, até existir
> ao menos um confirmado. Insistir com bloqueio depois de o PM já ter pulado vira
> laço sem saída.
>
> *Mínimo e ideal:* diga na tela, textualmente: **"1 indicador é o mínimo para
> prosseguir; 3 a 5 é o ideal."** Não trave o PM que só consegue pensar em um agora.
>
> *Conduta deste portão — o julgamento do que é crítico é inteiramente do PM:*
> **(1)** Faça a pergunta do roteiro **exatamente como está escrita** — e não
> acrescente exemplo de tipo nem de domínio, em nenhum momento da conversa.
> **(2)** Registre apenas o indicador que o **PM nomear por iniciativa dele**; não
> ofereça candidatos, nem para destravar quem hesitou. **(3)** Transcreva a
> resposta **literalmente**, sem validar nem criticar o que ele disse. **(4)**
> Encerre cada indicador nos campos do roteiro — nome, consequência e, opcional,
> onde é calculado. Monitoramento e alarme são a etapa da R4.

---

## O roteiro que ele executa

**Abertura (uma vez):**
> Antes de tocar produção, preciso saber o que **não pode colapsar**. Vou
> perguntar sobre consequência — não sobre que tipo de número é. Responda com as
> suas palavras. **1 indicador é o mínimo para prosseguir; 3 a 5 é o ideal.** Se
> preferir adiar, diga "pular por agora".

**Perguntas que puxam pelo efeito do erro** (faça a primeira; a cada "mais
algum?", use a próxima — para o ângulo do dano silencioso sempre aparecer, não só
quando o Claude resolve variar; nunca cite um tipo de indicador):
1. Que número, se ficasse errado para um usuário amanhã, faria você perder a
   confiança dele — ou a confiança dele no produto?
2. Que valor, se colapsasse em silêncio, você só descobriria pelo dano, tarde
   demais?
3. Se você pudesse vigiar um único número em produção esta noite, qual seria?

**Para CADA indicador que o PM nomear, pergunte só isto** (nada além):
- **Nome** — a palavra do PM.
- **Por que o colapso é desastre** — uma linha, nas palavras do PM.
- **Você já sabe onde ele é calculado no código?** — opcional; "não sei ainda" é
  resposta válida.

Depois de cada um: *"Mais algum, ou encerro?"* Ao encerrar com ≥1, grave o
arquivo e **prossiga com a ação original**. Nunca encerre com zero (só via "pular
por agora").

---

## O arquivo que ele produz — `indicadores-criticos.md`

Formato mínimo, uma linha por indicador, editável à mão. É o pré-requisito que a
R4 estendida lê.

```
# Indicadores críticos do produto
# Os números que, se colapsarem, significam desastre. Editável à mão.
# Um por linha. Mínimo 1 para o portão liberar; ideal 3-5.
# nome | por que o colapso é desastre | onde é calculado (path, ou "não sei ainda")

# <nome> | <consequência, uma linha> | <path ou "não sei ainda">
# (esta linha é exemplo e está comentada. Apague o "#" ao escrever o primeiro
#  indicador de verdade — linha sem "#" é o que abre o portão.)
```

**Estado de pendência (escape):** se o PM pulou, o arquivo existe só com esta
linha (nenhuma linha de dado):

```
# PENDENCIA: setup adiado em <momento> — "pular por agora". Sem indicador
# confirmado; o portão volta a lembrar na próxima ação que toca produção,
# sem bloquear.
```

**Regra de leitura do gatilho:** o portão libera quando há ≥1 linha de dado (não
comentário). Só-comentário = bloqueia. Só-pendência = lembra, sem bloquear. Ao
gravar o primeiro indicador confirmado, a linha de pendência é removida.
