# Instalar e usar as skills

Uma skill é uma pasta com um arquivo dentro. Você copia a pasta para o lugar
certo do seu projeto e ela passa a existir — não há instalação, não há programa
para rodar, não há nada para configurar. Este manual tem cinco passos e nenhum
deles exige abrir um arquivo de código.

*Conferido na documentação oficial em 31/07/2026:*
[code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills).

---

## 1. Escolha onde ela vale

Dois lugares, e a diferença é só o alcance:

| Onde você põe a pasta | Vale para |
|---|---|
| `.claude/skills/` dentro do projeto | **só aquele projeto** |
| `~/.claude/skills/` na sua pasta pessoal | **todos os seus projetos** |

Comece pelo projeto. Uma auditoria que fala do seu código não tem por que
aparecer nos outros.

## 2. Copie a pasta inteira

O caminho final tem que ficar assim:

```
.claude/skills/auditoria-de-caminho-duplicado/SKILL.md
```

Se preferir não mexer em pasta na mão, cole isto no Claude Code, dentro do seu
projeto:

> Copie a pasta `auditoria-de-caminho-duplicado` de
> `~/Projetos/travas-de-produto/skills/` para `.claude/skills/` deste projeto,
> preservando o nome da pasta e o arquivo `SKILL.md` dentro dela. Não altere o
> conteúdo do arquivo. Depois me diga o caminho final.

Ajuste `~/Projetos/travas-de-produto/` para onde você baixou este repositório.

**O nome da pasta importa mais que o conteúdo do arquivo.** É dele que sai o
comando para chamar a skill — pasta `auditoria-de-caminho-duplicado` vira
`/auditoria-de-caminho-duplicado`. O campo `name` lá dentro é só o rótulo que
aparece nas listagens.

## 3. Reinicie — só na primeira vez

Depois que a pasta `.claude/skills/` existe, o Claude Code percebe sozinho
quando você acrescenta, muda ou remove uma skill, sem reiniciar. **A exceção é
a primeira:** se a pasta `.claude/skills/` não existia quando a sessão começou,
reinicie o Claude Code para ele passar a olhar para ela.

## 4. Confirme que ela está lá

Comece a digitar a barra e o nome — `/auditoria-` — e veja se ela aparece na
lista. Se não aparecer, é quase sempre uma destas três: o caminho está errado, o
arquivo dentro da pasta não se chama `SKILL.md`, ou você não reiniciou depois de
criar a pasta pela primeira vez.

O comando `/skills` abre o menu de gerenciamento, e o `/doctor` mostra
diagnóstico quando algo não carregou.

## 5. Use

Duas formas, e a diferença entre elas é o assunto do repositório inteiro:

**Chamando pelo nome** — `/auditoria-de-caminho-duplicado` — é a forma em que
estas skills têm evidência de funcionar. Você decide que é a hora, e a auditoria
chega sobre um texto já escrito.

**Sozinha**, quando o modelo reconhece pelo texto da `description` que é o caso.
Isso acontece, e é um tiro extra de graça — mas **não conte com ele**. Reconhecer
o momento é exatamente a parte que falhou na medição registrada no
[README](../README.md): a mesma pergunta, deixada para o modelo reconhecer
sozinho, teve zero disparos demonstráveis em dois dias.

Se quiser garantir que uma skill só rode quando você mandar, acrescente
`disable-model-invocation: true` no cabeçalho dela.

---

## O que esperar de volta

Toda skill daqui termina com uma linha `Veredito: X`. **Se a resposta não tiver
essa linha, a auditoria não foi concluída** — mande completar. E todas elas
distinguem *buscou e não achou* de *não conseguiu buscar*: a segunda é `NÃO SEI`,
que é falha de auditoria, não aprovação.

Nenhuma delas aprova por ausência de evidência. Se você receber "provavelmente
está conectado" ou "não parece haver nada parecido", sem caminho de arquivo, a
skill não foi seguida.

## Para remover

Apague a pasta de dentro de `.claude/skills/`. Não sobra nada.
