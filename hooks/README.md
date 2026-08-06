# Instalar os hooks

**O que é um hook, por que ele é diferente de uma regra, e por que só um deles
barra** está no [README da raiz](../README.md). Aqui é só como instalar, medir e
remover.

## Antes de tudo: você tem Python?

Estes hooks são scripts Python 3. Rode isto no seu terminal:

```
python3 --version
git --version
```

Você deve ver duas linhas com número de versão, tipo `Python 3.11.4`.
(No Mac: abra o **Terminal** — ⌘+espaço, digite "Terminal".)

**Se o `python3` der erro, pare aqui.** Sem Python 3 os hooks não rodam — e o pior é que eles
não avisam: o Claude Code trata script que não roda como erro não bloqueante, seu
trabalho segue normal, e você fica com quatro arquivos instalados que não fazem
nada. Instale o Python 3 antes, ou peça ao Claude Code para reescrever os hooks
sem ele — mas não instale assim.

**Se só o `git` der erro**, três dos quatro funcionam normalmente. O da R2 usa o
git para saber o que mudou; sem ele fica calado — instalado e sem fazer nada. Ou
instale o git, ou não instale esse.

*(Por que Python: macOS e a maioria das distribuições Linux já vêm com ele, e o
código fica legível para quem quiser conferir o que o hook faz antes de rodar.)*

## Os quatro hooks (mais o testador)

| Arquivo | Regra | Quando roda | O que faz |
|---|---|---|---|
| `r1-reuso-antes-de-criar.py` | R1 | antes de gravar arquivo de esquema de banco, ou rodar comando que cria/altera tabela | injeta |
| `r2-artefato-sem-leitor.py` | R2 | ao terminar de responder, se há estrutura persistente alterada e não commitada | injeta |
| `r4-execucao-sobre-dado-real.py` | R4 | antes de rodar carga, migração, backfill | injeta |
| `s0-indicadores-criticos.py` | S0 | antes de comando que toca produção | avisa (ou barra, se você ligar) |

**Cada um é um arquivo só, que funciona sozinho.** Não há módulo compartilhado de
propósito: um arquivo esquecido na cópia deixaria os quatro silenciosamente
inertes.

O quinto arquivo, `testar.py`, não é um hook — é o testador. Ele roda os quatro
contra entradas de mentira e confere que disparam quando devem, ficam quietos
quando não devem, e deixam passar quando algo quebra. Os passos 3 e 4 usam ele.

A R3 não tem hook. O motivo está no [bloco da R3, no manual das
regras](../regras-sempre-ativas/regras-de-construcao.md).

## Instalar

**1. Copie os cinco `.py`** para `.claude/hooks/` no seu projeto — os quatro hooks
e o `testar.py`, que os passos 3 e 4 usam. (Este README não precisa ir.)

**2. Descubra os comandos do seu projeto.** Cada hook tem, no topo, uma lista de
palavras que ele procura. Sem ela os hooks não fazem nada de útil — o que vem de
fábrica são exemplos genéricos.

Você não precisa saber quais são de cabeça. Cole isto no Claude Code:

> Liste os comandos e caminhos de arquivo deste projeto que (a) criam ou alteram
> esquema persistente — migração, tabela, coluna, modelo, campo agregador, fonte
> de dados; (b) rodam carga, migração, backfill ou ingestão sobre dado que eu não
> controlo; (c) tocam produção. Me devolva três listas, e para cada item diga onde
> você o encontrou. Não edite nada.

**Na lista (a), não inclua script, fila nem serviço.** O hook da R1 enxerga
formato de banco; script novo e caminho paralelo de coleta ele não distingue de
trabalho legítimo — pôr esses padrões ali só produz ruído. Para essa faixa existe
a skill `auditoria-de-caminho-duplicado`, que você invoca antes de construir.

**Leia as três listas antes de seguir.** Se aparecer alguma coisa que você não
reconhece, pergunte antes de aceitar — é mais barato agora que depois.

**3. Mande ele aplicar.** Quando as listas estiverem boas, cole isto:

> Agora ponha essas listas dentro dos hooks em `.claude/hooks/`, assim:
>
> - a lista (a) em `r1-reuso-antes-de-criar.py` — caminhos em `CAMINHOS`,
>   comandos em `COMANDOS`;
> - a lista (a), só os caminhos, em `r2-artefato-sem-leitor.py`, em `CAMINHOS`;
> - a lista (b) em `r4-execucao-sobre-dado-real.py`, em `COMANDOS`;
> - a lista (c) em `s0-indicadores-criticos.py`, em `COMANDOS_DE_PRODUCAO`.
>
> Regras para essa edição:
> 1. Mexa **só** nessas listas. Não altere mais nada em nenhum dos arquivos — nem
>    os textos, nem o resto do código.
> 2. Nas listas, escreva só o pedaço da palavra, sem `\b`. `\bbackfill\b` não casa
>    `backfill_precos.py` nem `run_backfill.py`, porque o underline conta como
>    letra. `backfill` casa os três.
> 3. No `s0-indicadores-criticos.py`, seja **estreito**: é o único que pode barrar
>    minha ação. Só o comando exato que publica. Na dúvida, deixe de fora.
> 4. Não mexa na chave que liga o bloqueio (`BARRAR_DE_VERDADE`) — ela fica
>    desligada. A seção *Medir antes de deixar barrar* diz quando ligar.
> 5. Depois, rode `python3 .claude/hooks/testar.py` e me mostre o resultado.
> 6. Me diga, em uma linha por arquivo, o que você acrescentou.

**4. Olhe o resultado do teste.** Você não roda nada — o passo 3 já mandou o Claude
rodar e te mostrar. Procure a **última linha** do que ele imprimiu:

- **`TODOS OS TESTES PASSARAM`** → siga para o passo 5.
- **`FALHARAM: ...`** → **pare.** Responda: *"algum teste falhou. Conserte só as
  listas e rode de novo."* Não siga com teste falhando: o erro típico é a lista
  escrita de um jeito que nunca casa nada, e aí o hook fica instalado sem fazer
  nada — que é pior que não ter instalado, porque você acha que está protegido.

**5. Ligue os hooks.** Falta dizer ao Claude Code quando chamar cada um. Isso vive
num arquivo de configuração, e você não precisa abri-lo. Cole:

> Registre os quatro hooks de `.claude/hooks/` na configuração deste projeto:
>
> - `r1-reuso-antes-de-criar.py` — no evento PreToolUse, para as ferramentas
>   Write, Edit e Bash;
> - `r4-execucao-sobre-dado-real.py` — no evento PreToolUse, para a ferramenta Bash;
> - `s0-indicadores-criticos.py` — no evento PreToolUse, para a ferramenta Bash;
> - `r2-artefato-sem-leitor.py` — no evento Stop.
>
> Rode cada um com `python3`, use `$CLAUDE_PROJECT_DIR` no caminho, e ponha um
> tempo limite de 10 segundos (15 para o do Stop). Um bloco separado por hook,
> para eu conseguir remover um sem mexer nos outros.
>
> Use `.claude/settings.json` se quiser que a equipe toda tenha os hooks (ele vai
> para o git); use `.claude/settings.local.json` se for só para mim.
>
> Antes de gravar: se o arquivo já existir, **preserve tudo o que já está lá** — acrescente, não substitua. Se já houver hooks configurados, some
> aos que existem. Me mostre o que você vai acrescentar antes de gravar, e depois
> confirme com `/hooks` que os quatro aparecem.

**Isso é arriscado para o meu projeto?** Não. Esse arquivo só configura o Claude
Code *dentro desta pasta* — ele não toca no código do seu produto, nem no seu
banco, nem em nada que roda em produção. Se algo sair errado ali, o pior que
acontece é os hooks não ligarem, ou o Claude Code reclamar do arquivo. Nenhum
desses casos quebra o que você construiu.

O único cuidado de verdade é o que já está no prompt: se o arquivo existir com
outras configurações suas, elas precisam ser preservadas. Por isso o prompt manda
mostrar antes de gravar.

*Se preferir fazer à mão*, é isto:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Bash",
        "hooks": [{ "type": "command", "timeout": 10,
          "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/r1-reuso-antes-de-criar.py\"" }]
      },
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "timeout": 10,
          "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/r4-execucao-sobre-dado-real.py\"" }]
      },
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "timeout": 10,
          "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/s0-indicadores-criticos.py\"" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "timeout": 15,
          "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/r2-artefato-sem-leitor.py\"" }]
      }
    ]
  }
}
```

**6. Confira.** Digite `/hooks` no Claude Code. Devem aparecer os quatro. Se
faltar algum, diga ao Claude qual faltou.

## 7. Confirme que ele **executa** — aparecer na lista não é rodar

Este passo não existia até 06/08/2026, e a cicatriz é o motivo dele.

No projeto onde estes hooks nasceram, uma camada inteira — nove hooks em cinco
eventos — **nunca executou, por cerca de três meses e meio**. Estavam escritos,
registrados e listados. O que faltava era banal: o Claude Code lê a pasta
`.claude/` a partir do diretório onde a sessão foi aberta, e as sessões abriam no
diretório **pai** do repositório. Ninguém percebeu porque a única evidência de que
um hook rodou é ele aparecer — e ele nunca apareceu, o que foi lido como "não
houve caso". **Nada vigiava o vigia.**

Então force um disparo antes de confiar em qualquer coisa. Peça ao Claude, dentro
do projeto:

> Crie uma tabela nova chamada `teste_do_hook` numa migração, só para eu conferir
> se o hook dispara. Não rode a migração.

O hook da R1 deve aparecer com o texto da regra. Se **nada** aparecer, ele não
está executando — e o problema quase sempre é de onde a sessão foi aberta: ela
precisa abrir **dentro** da pasta do projeto, a mesma que contém o `.claude/`.
Corrigido isso, repita o teste. Depois é só pedir para desfazer a migração de
mentira.

E a regra que fica, que vale mais que o teste: **silêncio tem duas causas** — não
houve caso, ou não está instalado. Enquanto você não tiver visto o hook disparar
**uma vez**, você não sabe em qual das duas está. Refaça este passo sempre que
mudar de máquina, mover a pasta ou trocar o jeito de abrir a sessão.

## Remover

Peça: *"remova o hook `<nome do arquivo>` da configuração deste projeto, sem mexer
nos outros."* É por isso que cada hook tem o seu arquivo e o seu bloco separado —
tirar um não afeta os demais.

## Medir antes de deixar barrar

Três dos quatro hooks só avisam — nunca travam nada. O do S0 é o único que pode
travar, e ele **começa desligado**: nos primeiros dias só avisa, igual aos outros.

Isso é de propósito. Use esses dias para olhar **em que comandos ele aparece**. Se
ele avisar em coisas que não são publicação de verdade, o problema é a lista, não
você. Peça o ajuste:

> O hook do S0 está aparecendo em comandos que não publicam nada — por exemplo
> `<cole aqui o comando>`. Ajuste só a lista dele para não pegar esses casos, sem
> mexer em mais nada, e rode `python3 .claude/hooks/testar.py` depois.

Quando ele só aparecer nas publicações de verdade, aí sim vale ligar a trava:

> Ligue o bloqueio do hook do S0: mude `BARRAR_DE_VERDADE` para `True` em
> `.claude/hooks/s0-indicadores-criticos.py`. Não altere mais nada no arquivo.

A partir daí ele deixa de avisar e passa a **parar** o comando quando faltar a
lista de indicadores críticos. Se quiser voltar atrás, é o mesmo pedido com
`False`.

Neste projeto, dois hooks de lembrete já foram medidos e descartados — os números
estão no [aviso de estado do README](../README.md#aviso-de-estado--o-que-tem-lastro-e-o-que-não-tem).
Desenho plausível erra. **Se um hook virar ruído, apague.**

## O que os scripts garantem

- **Falha aberta.** Script quebrado, entrada malformada ou campo renomeado numa
  versão nova do Claude Code: a ação **passa**. Testado. (Estouro de tempo também
  passa — isso é do próprio Claude Code, que trata demora como erro não
  bloqueante; li na documentação, não testei.)
- **Nada para instalar.** Python 3 puro, sem `pip install`, sem `jq`. Única
  chamada externa: o hook da R2 usa `git` para saber o que mudou. Sem git, ele
  fica inerte.
- **Silêncio é o padrão.** Fora dos seus padrões, o hook não imprime nada e não
  consome contexto.

## O que eles NÃO fazem

- **Não decidem.** Três dos quatro só entregam a pergunta; quem responde é o
  modelo, olhando o código, e depois você, olhando a resposta.
- **Não substituem as skills.** O hook da R2 sabe QUE a estrutura está alterada;
  ele não procura o consumidor. Isso é a skill `auditoria-de-peca-oca`.
- **Não cobrem o durante e o depois.** O hook da R4 avisa antes do comando. Olhar
  o indicador a cada toque e a ordem de contenção continuam sendo seu trabalho.
- **Não foram medidos no seu projeto.** Os testes provam que o código funciona
  como escrito — não que ele dispara nos momentos certos do seu código.

## Ressalva de validade

Escrito contra a documentação do Claude Code de **30/07/2026**. Mecânica de
ferramenta muda, e este é o trecho do repositório que envelhece mais rápido: se
algo aqui parar de bater com a documentação, acredite na documentação.
