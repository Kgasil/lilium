# Lilium — matriz de aceitação manual / Manual acceptance matrix

**v0.14.0 · Estado: não executada / Not executed.** Roteiro complementar à [aceitação Windows](clean-machine-validation.md) e à [Issue #1](https://github.com/Kgasil/lilium/issues/1). Use exclusivamente dados sintéticos. Valores de referência derivados do gerador de cenários e dos contratos de testes no commit [e34b2f5](https://github.com/Kgasil/lilium/tree/e34b2f5a7a2f928ac6b2aea80bfea23a78d258c0), não de uma execução manual do binário.

## Preparação

Conferir hash, diagnósticos, ambiente e restrições descritos no guia Windows. Não ignorar alertas de segurança. Carregar o cenário **Comércio de bairro** completo em Comece por aqui, confirmar a substituição de entradas e limpar filtros de período. Executar os módulos individualmente. Histórico e fila Flow podem conter registros anteriores: usar sessão de teste e não excluir dados alheios. Registrar cada caso como APROVADO, REPROVADO, BLOQUEADO ou NÃO EXECUTADO; arredondamentos visuais devem corresponder ao valor exibido com a precisão prevista.

## 1. Reconciliação independente: comércio de bairro

Cada mês de janeiro a setembro de 2026 possui três pedidos agregados fictícios, com preços unitários R$ 24, R$ 5 e R$ 95. No mês m (1 a 9), quantidades são 18+2m, 21+2m e 24+2m. Receita = 2817 + 248m; custo = 68% da receita; resultado = receita menos custo.

| Mês | Receita (R$) | Custo (R$) | Resultado (R$) |
|---|---:|---:|---:|
| Jan | 3.065,00 | 2.084,20 | 980,80 |
| Fev | 3.313,00 | 2.252,84 | 1.060,16 |
| Mar | 3.561,00 | 2.421,48 | 1.139,52 |
| Abr | 3.809,00 | 2.590,12 | 1.218,88 |
| Mai | 4.057,00 | 2.758,76 | 1.298,24 |
| Jun | 4.305,00 | 2.927,40 | 1.377,60 |
| Jul | 4.553,00 | 3.096,04 | 1.456,96 |
| Ago | 4.801,00 | 3.264,68 | 1.536,32 |
| Set | 5.049,00 | 3.433,32 | 1.615,68 |
| Total | 36.513,00 | 24.828,84 | 11.684,16 |

Margem total: 32%. Sales: 27 pedidos distintos, 837 unidades, ticket agregado R$ 1.352,33, Mochila lidera em receita (R$ 29.070,00). Forecast: selecionar manualmente tendência linear e horizonte de 3 meses; outubro R$ 5.297,00, novembro R$ 5.545,00, dezembro R$ 5.793,00. Não interpretar a previsão sintética como garantia de receita futura.

### Referências para os cinco cenários

O arquivo [acceptance-reference.test.js](../tests/acceptance-reference.test.js) fixa os resultados esperados dos cinco cenários em centavos inteiros. Inclui 26 grupos de verificações (catálogo, totais CSV de Insights, Sales, Finance, Operations e Forecast). Os 26 grupos passaram em V8 com módulos do commit de referência e uma implementação mínima de assert; a execução Node.js/CI do novo teste ainda não foi confirmada. Os totais CSV de Insights são verificados independentemente, não pelo motor Python. O workflow Windows já executa arquivos `tests/*.test.js`. Não substitui a aceitação manual ou altera o candidato aprovado.

| Cenário | Receita (R$) | Resultado (R$) | Margem |
|---|---:|---:|---:|
| Comércio | 36.513,00 | 11.684,16 | 32% |
| Serviços | 146.790,00 | 76.330,80 | 52% |
| Indústria | 77.670,00 | 20.194,20 | 26% |
| Restaurante | 25.272,00 | 7.076,16 | 28% |
| Loja virtual | 69.309,00 | 23.565,06 | 34% |

### Backend Python — regressão dos indicadores

[tests/test_acceptance_reference.py](../tests/test_acceptance_reference.py) contém três métodos unittest, cada um com cinco subcasos: totais exatos, 45 agregações mensais com entrada fora de ordem, e rejeição de uma linha inválida após nove linhas válidas. Os três métodos e 15 subcasos passaram em Python 3.13.5 no ambiente Linux local; os blobs do motor e do teste conferem com o GitHub (`8e380e01f3e30a9fdf3775e8c9fbb01ab79038f8` e `445055558f7e118680cb04ed8cad67517f5e13d6`). A regressão completa em Windows e a execução manual do pacote continuam pendentes. Nenhuma alteração funcional ou mudança do candidato.

## 2. Casos funcionais

| ID | Módulo / ação | Resultado esperado |
|---|---|---|
| M01 | Insights: analisar cenário completo | Nove meses, totais e margem da tabela acima |
| M02 | Insights: filtrar somente setembro | R$ 5.049,00; custo R$ 3.433,32; resultado R$ 1.615,68; margem 32% |
| M03 | Insights: importar CSV com cabeçalho incorreto | Diagnóstico de erro; nenhuma análise nova válida ou resultado antigo apresentado como novo |
| M04 | Finance: cenário independente, preço 100, variável 40, fixo 2000, quantidade 100, taxa 5%, meta 1000 | Receita R$ 10.000, variável R$ 4.000, taxa R$ 500, resultado R$ 3.500, margem 35%, contribuição unitária R$ 55, equilíbrio 37 un., meta 55 un. |
| M05 | Finance: precificar custo R$ 60 com margem desejada de 40% | R$ 100,00; rejeitar margem de 100% |
| M06 | Sales: analisar cenário completo e comparar Insights | Receita R$ 36.513,00, 27 pedidos, 837 unidades, ticket R$ 1.352,33; Mochila em primeiro |
| M07 | Operations: cenário de comércio | Três etapas, gargalo estimado Expedição e capacidade serial de 210 unidades no período informado; não confundir capacidade com produção realizada |
| M08 | Strategy: cenário de comércio, data-base 30/09/2026 | Dois KRs; nenhuma meta vencida nessa data; ações ordenadas com Revisar custos em primeiro, pontuação 10 |
| M09 | Forecast: tendência linear de 3 meses | Outubro a dezembro conforme tabela de referência; três modelos disponíveis; nenhuma promessa de precisão futura |
| M10 | Flow: regra sintética da seção 3, após recalcular Insights completo | Regra de margem acionada; proposta pendente, duplicação evitada; conclusão somente após aprovação manual |
| M11 | Connect: entrada da seção 3 com separador ponto e vírgula, vírgula decimal ativada | Normalizar para CSV de três colunas; campo Cliente descartado; confirmar transferência antes de substituir Insights |
| M12 | Copilot: consultar Insights após recalcular cenário completo | Resposta guiada com receita e margem compatíveis, fonte e período; sem IA externa; ausência de dados não deve produzir números inventados |
| M13 | Reports: selecionar fontes calculadas | Seções correspondem às fontes selecionadas, períodos e natureza dos dados explícitos; simulações não somadas aos totais históricos |
| M14 | Reports: exportar TXT/JSON e imprimir PDF | Arquivos abrem e preservam valores; PDF legível sem elementos cortados; inspeção visual manual necessária |
| M15 | Starter: trocar cenário | Resultados afetados e relatórios anteriores limpos; histórico salvo e fila Flow preservados; verificar proveniência antes de combinar |
| M16 | Help Center: pesquisar termo com e sem acento | Busca local retorna tópicos correspondentes; modelo de feedback sem dados pessoais |

M04/M05 usam valores independentes do cenário de comércio, conforme [finance.test.js](../tests/finance.test.js). M11 altera as entradas; recarregue e recalcule o cenário completo antes de M12–M13.

## 3. Entradas de teste

Flow: use o formato de cabeçalho exibido pelo módulo (contrato de [flow.test.js](../tests/flow.test.js)) e a linha abaixo:

```csv
QA1,insights.margin,lt,40,Revisar custos ficticios
```

Connect:

```csv
Dia;Receita;Custo;Cliente
2026-01-01;100,50;60,25;IGNORAR
```

Mapear date→Dia, revenue→Receita, cost→Custo. Resultado:

```csv
date,revenue,cost
2026-01-01,100.50,60.25
```

Após transferir e executar Insights, receita R$ 100,50, custo R$ 60,25, resultado R$ 40,25. O campo Cliente não deve aparecer na saída normalizada.

## 4. Casos não funcionais

| ID | Ação | Resultado esperado |
|---|---|---|
| N01 | Verificar ZIP e seis diagnósticos em Windows limpo | Hash idêntico ao candidato; seis diagnósticos positivos sem alertas ignorados |
| N02 | Inicializar, encerrar e iniciar novamente | Serviço local em loopback; sem travamento; token anterior rejeitado |
| N03 | Salvar análise sintética e reiniciar | Análise disponível; entradas originais não armazenadas como CSV pelo histórico |
| N04 | Exportar backup, excluir só registro de teste e recuperar duas vezes | Recuperação correta sem duplicatas; não sobrescrever registros existentes |
| N05 | Teclado e viewport de 390 px | Foco visível, controles alcançáveis, conteúdo legível; registrar barreiras |
| N06 | Revisão de privacidade e segurança | Registrar comportamento de rede, limitações do armazenamento e achados; revisão manual independente ainda exigida |
| N07 | Preparar nova pasta da mesma versão | Pasta anterior preservada; backup antes de alternar; não afirmar migração entre versões |

## 5. Registro a preencher (sem dados sensíveis)

Data / Windows e arquitetura / versão / URL do build / SHA-256 do ZIP interno / ambiente sem Python / executor (identificador não pessoal, opcional).

| ID | Status | Resultado observado | Evidência redigida | Gravidade / ação |
|---|---|---|---|---|
| M01–M16, N01–N07 | NÃO EXECUTADO | — | — | — |

Copie uma linha por caso. Não publique tokens, caminhos privados, dados reais ou detalhes de exploração de vulnerabilidades. Reporte bloqueios e mantenha o piloto fechado até aprovação registrada conforme [pilot-readiness.md](pilot-readiness.md). Nenhum caso manual foi marcado como aprovado nesta matriz.
