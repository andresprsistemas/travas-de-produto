# Auditoria de peça oca

## O problema

Sistemas construídos com agentes e automação acumulam capacidades que parecem prontas. Um dado passa a ser gravado, uma regra é escrita, uma verificação é criada — e tudo isso é reportado como entregue. Mas "foi construído" não é o mesmo que "está em uso". Às vezes a coisa existe mas nenhum caminho que faz o trabalho de verdade a aciona — e o problema não aparece, porque a presença do artefato imita a presença da função.

## De onde isto veio

Pedi a uma ferramenta um recurso para marcar itens à mão e classificá-los, e ela confirmou que o que eu marcava alimentava o aprendizado do sistema. Trabalhei meses confiando que estava ensinando a máquina. Muito depois descobri que nenhuma parte do algoritmo consultava aquelas marcações — elas só escondiam da minha própria tela os itens que eu tinha marcado. Eu achava que corrigia o sistema; só arrumava a minha vista.

## O princípio

Uma capacidade construída que nenhum fluxo real aciona é pior do que não existir. Quem sabe que não tem proteção fica atento; quem acha que tem, baixa a guarda — e o artefato inerte fabrica exatamente essa falsa confiança.

## Como aplicar

As três perguntas:

1. **Quem produz isto?** Algo escreve ou gera este dado, regra ou verificação.
2. **Quem decide com isto?** O que o sistema DECIDE ou CALCULA muda por causa disto — não o que aparece na tela; e a mudança tem que ser naquilo que esta peça foi dita fazer, não um efeito colateral em outro lugar.
3. **O que aciona isto?** Existe um gatilho confiável — automático, ou um ritual que roda sem depender de alguém lembrar?

Como ler: cada pergunta exige um lugar concreto e apontável. Falta em qualquer uma = peça oca. "Não encontrei" é veredito oco, nunca "deve estar certo". Atalho da 2: sem esta peça, o sistema decidiria diferente naquilo que ela promete? Filtrar, esconder ou registrar não conta.

Duas ilustrações: um escore de risco é salvo em toda cobrança, mas a aprovação decide só por valor e cartão — ninguém decide com o escore → oca. Uma marca de trânsito guia o roteirizador a desviar a cada despacho — produz, decide, aciona → passa.

Para rodar isto sobre uma capacidade que já existe no código, este repositório traz uma skill que faz essa busca e devolve um veredito com evidência, em `../skills/auditoria-de-peca-oca`.

## Quando aplicar

Faça esta auditoria quando alguém disser que uma capacidade está "pronta" ou "conectada" e você não viu, com os próprios olhos, onde ela é usada — e sempre que uma decisão importante depender de algo que você presume estar no lugar mas nunca conferiu. Auditar uma capacidade obriga alguém a olhar o código com propósito, e esse olhar às vezes esbarra em outras coisas — que não são o veredito desta peça, mas valem anotar.

## O que ele NÃO faz

Este roteiro não diz se a capacidade é boa, correta ou bem-feita — só se ela participa. Uma peça pode passar nas três perguntas e ainda decidir errado, ou falhar por estar desligada de propósito. Ele encontra o desligado; não julga o ligado. O veredito é ponto de partida, não diagnóstico: aponta QUE uma peça está oca, não POR QUE ficou assim nem qual a correção certa — isso exige investigar o que o veredito revelou.

## Proveniência

Praticado desde abril de 2026; formalizado como princípio em junho de 2026, a partir de três casos do mesmo sintoma — causas diferentes, mesma aparência de peça pronta.
