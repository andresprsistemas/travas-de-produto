# Vigilância de execução

## O problema

Uma correção pode cumprir perfeitamente o objetivo local para o qual foi escrita e, ao topar com o dado real, violar alguma coisa que ninguém tinha como prever. A causa não estava lá para ser especificada — nasce no encontro do código com o dado, não no plano. Mas o efeito tem sempre o mesmo formato: um número que mede o resultado do produto se move demais, de repente. A causa é imprevisível; o efeito, não — e é isso que decide o que dá para vigiar de antemão.

## De onde isto veio

Carreguei mais dados para corrigir uma falha de cobertura — a intenção era certa e o passo, pequeno. A carga fez um identificador comum virar critério de corte, e num instante itens corretos foram barrados em massa. Eu vi acontecer, contive na hora preservando o que já estava certo, e só então investiguei a causa. Foi em 15 de julho de 2026. Mas contive por reflexo — e devia ter sido um alarme a avisar, não eu a perceber. A invariante "o resultado principal não perde itens válidos em massa" era escrevível antes, sem conhecer a causa, e teria gritado o sintoma antes de mim. O reflexo salvou; a estrutura é que faltava.

## O princípio

São duas vigilâncias, de naturezas diferentes, e tratá-las como uma só custa a primeira. Uma se automatiza: para cada número que, se desabar, significa desastre, dá para escrever de antemão a trava que dispara quando ele se move demais. Ela vigia o efeito, não precisa prever a causa, e pega o sintoma mais rápido que qualquer humano. A outra não se automatiza: descobrir por que o número desabou, no calor, e conter sem sacrificar o que estava certo. O alarme avisa que algo sumiu; não diz por quê. Quem confunde as duas deixa de instalar a primeira e fica dependendo do reflexo para o que devia ser trava.

## Como aplicar

Duas coisas, e a ordem importa.

1. **Antes: instale o alarme do efeito.** Para cada indicador de saúde que importa, escreva a trava que dispara quando ele se move além de um limite. Não tente prever a falha — vigie o resultado. É estrutura, escrevível hoje; não depende de você estar olhando na hora certa.
2. **Na hora: investigue e contenha.** Quando o alarme toca, a causa é trabalho humano — nenhuma trava a entrega. E a ordem de contenção é fixa: **conter, preservando o que já estava certo → corrigir a causa → só então publicar.** Nunca corrigir antes de conter: corrigir sobre um estado quebrado empilha falha sobre falha.

Desfazer antes de corrigir é conhecido em engenharia; o que muda é o que se preserva — o que já estava certo não pode ser sacrificado pela pressa de arrumar.

Para verificar se um indicador crítico já tem um alarme que dispara sozinho — ou se ninguém está vigiando o efeito —, este repositório traz uma skill que faz essa checagem e devolve um veredito com evidência, em `../skills/auditoria-de-monitor-de-saude`.

## O molde do monitor

Quando falta o alarme, o que se constrói tem um molde — genérico, serve a qualquer produto. Três propriedades:

1. **Vigia um indicador de saúde que o PM declarou crítico** — não um número qualquer, um dos poucos que, se desabar, significa desastre.
2. **Dispara sozinho quando esse indicador se move além de um limite** — e o limite é julgamento de produto: o PM o define, a ferramenta não.
3. **Roda independente do que mudou** — não é um teste que alguém lembra de rodar; é uma trava permanente que observa o efeito, haja ou não mudança.

Construir esse monitor é uma tarefa de código do PM. Os artefatos apontam que ele falta; não o constroem — construí-lo bem depende do julgamento do PM sobre o próprio sistema (onde o indicador é calculado, qual o limite). O molde é o formato; o conteúdo é do PM.

## Quando aplicar

O alarme: para todo número que representaria desastre se desabasse — instale-o cedo, haja ou não mudança à vista. A investigação e a contenção: sempre que uma mudança encontra dado real que você não controla — uma carga, uma fonte, uma expansão. Quanto menos você controla o que vai chegar, mais as duas valem.

## O que ele NÃO faz

O alarme detecta o sintoma, não entrega a causa: ele grita que itens sumiram, não diz o que os fez sumir — isso é investigação humana, no calor, e não se automatiza. E ele não previne: dispara depois que o efeito começou, cedo o bastante para conter, não para impedir. Vigiar o efeito é escrevível antes; entender a causa e decidir o que preservar, não.

## Proveniência

Nasce de uma cicatriz — o colapso de 15 de julho de 2026 — não de um padrão repetido. É prevenção derivada de uma ausência estrutural que um único incidente revelou: o alarme que faltava, e que era escrevível antes. Por isso só a metade automatizável ganha uma ferramenta de auditoria; a investigação da causa continua trabalho humano que nenhum artefato substitui.
