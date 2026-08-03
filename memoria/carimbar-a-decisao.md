# Carimbar a decisão

## O problema

Sistemas construídos com agentes tomam decisões o tempo todo — classificar um item, aprovar um pedido, definir um status. O risco silencioso é a decisão não ficar tomada: se cada ponto que precisa dela recalcula a partir da fonte, em vez de ler um resultado gravado, a decisão é refeita a cada uso e muda sozinha quando a fonte ou a regra muda, sem ninguém perceber. E quando a mesma decisão passa a viver em dois lugares, os dois divergem — e a divergência reabre o que já estava fechado.

## De onde isto veio

Meu sistema sabia classificar um item, mas não sabia barrá-lo. A classificação era tomada na hora em que algum passo lia o item — não ficava gravada em lugar nenhum. Então a decisão só existia naquele instante de leitura: assim que a fonte mudava ou o passo seguinte relia, a decisão anterior sumia sem registro do que fora decidido nem quando. Corrigi o mesmo tipo de erro cinco vezes, cada uma parecendo um caso isolado, antes de enxergar que o problema não era a classificação e sim ela nunca ficar registrada — a virada foi ver um item que eu já tinha julgado entrar de novo; o que não sobreviveu foi o julgamento.

## O princípio

Uma decisão recalculada no momento do uso não é uma decisão registrada — é uma aposta na leitura daquele instante. O problema não é ela mudar quando a fonte muda (às vezes deve); é mudar em silêncio, sem ninguém saber e sem rastro do que fora decidido antes nem sob qual regra. E se a mesma decisão vive em dois lugares, os dois divergem, e a divergência reabre o que já estava fechado. O remédio é decidir uma vez, gravar a decisão como propriedade da própria coisa, e fazer os pontos que agem lerem essa propriedade — de uma fonte só.

## Como aplicar

Use este roteiro ao desenhar uma decisão, antes ou durante a construção. Para auditar decisões que já existem no código, este repositório traz uma skill que faz essa busca e devolve um veredito com evidência, em `../skills/auditoria-de-decisao-nao-carimbada`.

1. **Onde a decisão é tomada?** Uma vez e gravada como propriedade da coisa, ou recalculada a cada uso? Recalculada na leitura é aposta, não registro.
2. **Quantos lugares guardam essa decisão?** Um só, ou ela vive em dois que podem divergir? Se são dois, a próxima correção vai a um e não ao outro, e o fechado reabre — junte num só, ou faça um a fonte e o outro só leitor.
3. **O registro diz quando e sob qual regra a decisão foi tomada?** Sem isso, quando a regra mudar você não sabe o que revisar, e a decisão velha segue valendo como afirmação falsa.

## Quando aplicar

Aplique quando for construir um ponto que decide algo que será usado de novo mais adiante — e sempre que uma decisão importante for consultada em mais de um lugar do sistema.

## O que ele NÃO faz

Isto não impede uma classificação errada de entrar. Se o ato de decidir já estava errado, gravar a decisão só torna o erro consistente e duradouro — houve um caso em que, no dia seguinte à gravação, uma falha na derivação ainda deixou itens errados passarem. O ganho é consistência e permanência, não imunidade: ele garante que a decisão certa não se perca nem se contradiga, não que a decisão seja certa. O veredito é ponto de partida, não diagnóstico: aponta QUE a decisão não está bem registrada, não POR QUE nem qual a correção certa — isso exige investigar o que o veredito revelou.

## Proveniência

Praticado desde maio de 2026. O princípio nunca foi escrito no projeto; está sendo formulado agora, ao escrever este artefato.
