---
name: auditoria-de-peca-oca
description: >-
  Use quando o usuário desconfia que uma capacidade construída — um dado
  gravado, uma regra, uma verificação, um serviço — pode não estar sendo usada
  de fato pelo sistema. Dispara quando ele pergunta se algo "está mesmo
  conectado", "roda de verdade", "é consumido", ou se foi "construído e
  esquecido". Audita a capacidade indicada e responde com evidência apontável,
  nunca com opinião. Use só DEPOIS de construído: se nada foi construído ainda e
  a dúvida é se vale criar mais um caminho, a skill é a
  `auditoria-de-caminho-duplicado`.
---

# Auditoria de peça oca

Descobrir se uma capacidade que o usuário aponta realmente participa do
funcionamento, ou se foi construída e nunca ligada.

## Princípio

Uma capacidade construída que nenhum fluxo real aciona é pior do que não
existir: fabrica confiança sem cobertura. "Existe" não é "é usada". Só vale
com prova de onde.

## Procedimento

Peça ao usuário o nome da capacidade a auditar. Depois responda às três
perguntas, cada uma com um LUGAR concreto no repositório ou na configuração
(local de código, ponto de entrada, tarefa agendada, arquivo de config) —
buscando de fato, não deduzindo:

1. **Quem produz?** Ache onde a capacidade é escrita, gerada ou calculada.
   Aponte o lugar.
2. **Quem decide com ela?** Ache, no caminho que decide ou entrega, o ponto
   onde o que o sistema DECIDE ou CALCULA muda por causa dela. Filtrar,
   esconder, exibir, registrar ou logar NÃO conta como decidir. Contrafactual
   testado contra a capacidade que o USUÁRIO alegou (não contra qualquer saída
   do sistema): se ela fosse removida, o sistema decidiria diferente naquilo
   que ela foi dita fazer? Se não, ninguém decide com ela.
3. **O que aciona?** Ache o gatilho, apontável. Vale se roda de forma confiável
   e REGISTRADA em lugar concreto — automático e versionado, agendamento, tarefa
   recorrente configurada, ou um ritual descrito em documento de processo
   versionado. NÃO vale o que depende de memória: rodar só quando alguém se
   lembra, por script ad hoc, ou só na máquina de uma pessoa. Ritual que existe
   só na cabeça de alguém não é apontável e não conta.

## Regra dura

Você NÃO pode responder "sim, está conectada" sem apontar o lugar exato de cada
uma das três. Nunca preencha a lacuna com suposição ("provavelmente algum
serviço lê"): ausência de evidência nunca vira aprovação.

## Veredito

Distinga buscar e não achar de não conseguir buscar: buscou e não achou →
OCA; não conseguiu inspecionar (sem acesso ao código, sem permissão, stack
que não dá para inspecionar) → NÃO SEI (falha de auditoria). Sem acesso ao
código, as três perguntas ainda podem ser feitas a quem conhece o sistema —
o que muda é que a resposta vem de pessoa, não de evidência apontável.

Reporte, por pergunta: LUGAR (caminho concreto) ou NÃO ENCONTRADO.

- Três lugares apontados e a pergunta 2 muda uma decisão → **LIGADA**.
- Qualquer NÃO ENCONTRADO → **OCA** (diga qual pergunta falhou).
- Pergunta 2 só com leitura/registro, sem mudar decisão →
  **OCA (lida, não decidida)**.
- Não deu para inspecionar → **NÃO SEI** (falha de auditoria).

A resposta termina OBRIGATORIAMENTE com uma linha `Veredito: X`, onde X é um
dos rótulos acima — sem ela, a auditoria não está concluída. Achados fora das
perguntas desta auditoria vêm DEPOIS da linha de veredito, nunca antes nem
misturados às respostas.
