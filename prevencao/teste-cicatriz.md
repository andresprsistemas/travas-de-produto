# Teste-cicatriz

## O problema

Um erro encontrado e corrigido volta, a menos que algo bloqueie ativamente o retorno. Em geral a equipe escreve a correção e segue em frente — e a próxima mudança, ou um caminho novo, desfaz aquilo em silêncio. Escrever teste para isso é prática antiga; o que muda o jogo é outra coisa: quais erros viram guarda permanente, e se esse guarda de fato falharia com o erro de volta. Sem isso, a correção é uma limpeza de uma vez, não uma memória.

## De onde isto veio

Um item que eu já tinha corrigido cinco vezes voltou a passar — por um caminho novo: uma funcionalidade que eu mesmo tinha construído produziu evidência a favor dele. Já não bastava corrigir de novo; o erro sabia voltar por portas diferentes. Em vez de escrever mais uma regra, congelei aquele caso exato num teste que trava a publicação se ele voltar a passar. O caso foi em 30 de junho de 2026; o teste, no dia seguinte.

## O princípio

O que precisa ser permanente é a cobertura do risco, não o teste original. O teste congela um caso real que falhou e trava a publicação se ele voltar; mas o diferencial não é o teste — é o critério de admissão: todo erro que chegou ao produto entra, os que aconteceram, não os hipotéticos. E o caso específico pode ser aposentado quando uma regra mais geral cobre explicitamente o mesmo risco — e mais. O invariante é "o risco segue coberto", não "este teste fica para sempre".

## Como aplicar

1. **Admissão:** todo erro real que chegou ao produto vira uma verificação que trava a publicação se ele voltar. Os que aconteceram, não os imagináveis.
2. **Não-teatral:** a verificação tem que exercitar o caminho onde o erro ocorreu e falhar com o erro de volta. Se você o reintroduzisse, ela quebraria? Se passa com entrada fabricada mas não toca o caminho real, é teatral.
3. **Saída:** um caso só sai quando uma regra mais geral cobre o mesmo risco (e mais). Sem essa regra, fica.

Para auditar se incidentes passados já têm essa cobertura — e se os testes existentes não são teatrais —, este repositório traz uma skill que faz essa checagem e devolve um veredito com evidência, em `../skills/auditoria-de-teste-cicatriz`.

## Quando aplicar

Aplique toda vez que um erro real chegou ao produto e você está prestes a seguir em frente depois de corrigi-lo — é o momento de decidir o guarda permanente. E ao herdar uma suíte que você não escreveu, para saber se os testes de regressão pegariam mesmo os erros de volta ou só parecem que pegam.

## O que ele NÃO faz

Isto protege contra o erro que já aconteceu, não contra o que ainda não tem nome — nenhuma cicatriz cobre uma falha que ninguém viu. E não basta a verificação existir: uma que passaria mesmo com o bug de volta é pior que nenhuma, porque fabrica cobertura falsa. O veredito é ponto de partida, não diagnóstico: aponta QUE a cobertura falha, não POR QUE nem qual a correção certa — isso exige investigar o que o veredito revelou.

## Proveniência

Diferente das outras peças, aqui o princípio já estava escrito e valendo no projeto antes deste artefato, com casos datados. Honestidade obrigatória: o próprio teste que originou esta peça ainda usa a forma frágil que ela desaconselha — congela uma instância, não o comportamento — e isso já está mapeado para correção. A peça nasce apontando para a própria dívida.
