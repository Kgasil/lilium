# Lilium Copilot — Etapa 04
Candidato de desenvolvimento, base c3676b00f530b8e08eadac063eb632147ac78c80. Sem lançamento.
## Arquitetura
Pergunta livre -> regras locais ou roteador Ollama opcional -> tópico permitido -> Copilot determinístico existente -> métricas, escopo, limitações e sugestões verificáveis. Modelo não produz números nem executa ações. Continuidade simples por tópico, até oito registros de perguntas/tópicos em memória, limpeza explícita. Exportação existente contém relatório determinístico, não conversa.
## Modelo local
Instale Ollama de https://ollama.com/ separadamente e obtenha qwen2.5:1.5b ou llama3.2:1b, respeitando licenças e requisitos. API documentada em https://docs.ollama.com/api/chat. Sem download automático. Consentimento renovado por pergunta, texto até 240 caracteres, sem métricas, arquivos, regras ou histórico enviados. Endpoint local protegido por token e Origin, 2 KiB, host literal 127.0.0.1:11434, sem proxy/redirect/URL configurável, modelos em allowlist, saída JSON restrita, resposta limitada, concorrência única. Timeout de socket 20s (não deadline total). Se indisponível, regras locais ou esclarecimento. Sem garantia sobre logs/comportamento de serviço local de terceiros; usar dados fictícios e perguntas sem segredos.
## Limites
Não é chatbot generativo irrestrito, modelo não sintetiza análises em prosa nem acessa planilhas. Roteamento pode errar; tópico exibido, respostas determinísticas, dados faltantes explícitos. Não afirmar ausência de alucinações ou certificação. Sem voz, RAG, memória persistente ou integração cloud. Revisão humana e Flow pendente permanecem. Sem alteração de Web Lab/Mini distribuídos ou custos contratados.
## Testes
Novos casos JS, teste de endpoint e transporte mockado, navegador sem modelo. Inferência real, desempenho local, testes adversariais amplos, CI e aceite manual ainda pendentes. Nota 9/10 não comprovada.
