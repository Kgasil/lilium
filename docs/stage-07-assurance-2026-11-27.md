# Etapa 07 — Security & Quality Assurance
Base f227f4ef6c859236b34645a57614f3146cfa5190, PR #7. Candidato não publicado.
- Rejeição de JSON duplicado, constantes não finitas, profundidade inválida, respostas de ferramenta, perguntas com controles/surrogates; limites e consentimento mantidos. Bloqueio liberado mesmo se fechamento falhar. Testes adversariais sintéticos, sem execução de modelo real.
- Rejeição de entradas ZIP duplicadas em XLSX e limite antecipado de linhas normalizadas.
- Benchmark sintético de 10 mil linhas e paridade CSV; revisão de navegador com texto literal, labels, teclado, impressão, isolamento e viewport estreito.
- Workflow Windows acrescenta job independente que baixa artefato da mesma execução, confere commit, tamanho e SHA-256, testa executável e revisão final. Hash de manifesto e ZIP do mesmo build não equivale a assinatura independente. Prévia portátil, não instalador MSI.
- Evidência anterior Mini 0.1.3: run 46067518409, artifact 15231442155, inner ZIP SHA-256 5b960d274a670a278a3db5211aec71c94416f615c62881548d108806b7f8f495 (dois builds idênticos nos logs). Artifact wrapper SHA-256 91b0b471b663a41272d5129157a9078586e981b2fcb1786715358a317a75f55b. Não é hash do candidato novo. Expira 11/12/2026.
- Dependências: run 46067518432, inventário atual resolvido sem vulnerabilidades conhecidas segundo pip-audit; inventário histórico registrou 89 em dois pacotes. Não é análise de malware nem certificação. Modelos e serviço Ollama não auditados nessa CI.
- Matriz de qualidade: quality-gate-2026-11-27.md. Sem nota comprovada, sem release.
