---
name: auditoria-de-decisao-nao-carimbada
description: >-
  Use quando o usuário desconfia que uma decisão — uma classificação, um status,
  uma aprovação — pode não estar registrada, ou pode viver em mais de um lugar
  que diverge. Dispara quando ele pergunta se algo "fica gravado", "é
  recalculado toda vez", "tem cópia em cache", "os dois lugares batem", ou por
  que "um item já corrigido voltou". Audita a decisão indicada com evidência
  apontável. Precisa de acesso ao código: sem o repositório não há o que buscar
  e o veredito é NÃO SEI — não rode no vazio.
---

# Auditoria de decisão não carimbada

Descobrir se uma decisão que o usuário aponta está registrada, em quantos
lugares ela vive, e se o registro diz quando e sob qual regra foi tomada.

## Princípio

Uma decisão recalculada a cada uso não é uma decisão registrada — é uma aposta
na leitura daquele instante. Se a mesma decisão vive em dois lugares, os dois
divergem, e a divergência reabre o que estava fechado. Só vale com prova de onde.

## Procedimento

Peça ao usuário o nome da decisão a auditar. Depois responda às três perguntas,
cada uma com um LUGAR concreto no código ou na configuração — buscando de fato,
não deduzindo:

1. **A decisão é gravada ou recalculada?** Ache onde ela é produzida. Se cada
   consumidor a recalcula a partir da fonte em vez de ler um resultado gravado,
   aponte isso — não há registro, cada uso refaz.
2. **Quantos lugares guardam essa decisão?** ESTA É A MAIS VALIOSA: decisão
   duplicada é quase invisível a olho e é o que mais causa dano. Busque
   ATIVAMENTE por um segundo armazenamento, cache, cópia ou recomputação
   paralela. NÃO conclua "só um lugar" sem ter procurado o segundo; diga o que
   buscou. Se achar dois ou mais, procure um documento, comentário, spec ou
   ticket APONTÁVEL declarando a duplicação intencional e temporária, com destino
   ou plano de convergência. Sem esse documento apontável de destino, é
   acidental — reporte qual sinal parcial encontrou, se houver.
3. **O registro carrega quando e sob qual regra a decisão foi tomada?** Aponte
   o campo com a data e a versão da regra, ou diga que não existe.

## Regra dura

Você NÃO pode responder "está carimbada" sem apontar o lugar exato em cada uma
das três. Nunca preencha a lacuna com suposição ("deve haver um só lugar",
"provavelmente fica gravado"): ausência de evidência nunca vira aprovação. Na
pergunta 2, "só um lugar" só vale se você procurou o segundo e disse onde.

## Veredito

Distinga buscar e não achar de não conseguir buscar: inspecionou e concluiu →
veredito abaixo; não conseguiu inspecionar (sem acesso ao código, sem
permissão, stack que não dá para inspecionar) → NÃO SEI (falha de auditoria).
Sem acesso ao código, o roteiro em prosa do artefato ainda serve para desenhar
a decisão.

- Gravada, fonte única, com data e regra → **CARIMBADA**.
- Sem registro, cada uso refaz → **RECALCULADA**.
- Dois ou mais lugares, sem documento apontável de que é deliberado →
  **DUPLICADA (acidental)** (aponte os lugares).
- Dois ou mais lugares, com documento/comentário/spec/ticket apontável que
  declara a duplicação intencional e temporária, com destino →
  **DUPLICADA (declarada)** (aponte os lugares e o documento).
- Gravada e única, mas sem quando/sob qual regra → **CARIMBADA SEM VALIDADE**.
- Não deu para inspecionar → **NÃO SEI**, dizendo o que faltou.

A resposta termina OBRIGATORIAMENTE com uma linha `Veredito: X`, onde X é um
dos rótulos acima — sem ela, a auditoria não está concluída. Achados fora das
perguntas desta auditoria vêm DEPOIS da linha de veredito, nunca antes nem
misturados às respostas.
