# GRAAL Security & Trust 1.1 — Etapa 06 / Lilium Mini
Data: 2026-11-26. Escopo: extensão 0.1.1; não inclui auditoria do Desktop ou do repositório inteiro. Design, funcionalidades e distribuição preservados.
## Originais e integridade
- Commit usado no download público: 447d7414f20e28f6c0440647f2b7be71fc44e71d; árvore 8d349895d533c0deb72d8f07b43b188746b03442, 105 blobs. O link público baixa o repositório completo (inclui scripts BAT do Desktop); os bytes desse ZIP gerado pelo GitHub não foram baixados nesta etapa. Foram inspecionados os seis blobs exatos da extensão, que coincidem com main, backup bb9370d9be44e1699e3798b18c745061e5ba1748 e CI 4bb55e74373c81e9018ba9107e8825278a6a9946.
- Artefato experimental original [15078758847](https://github.com/Kgasil/lilium/actions/runs/45736783251/artifacts/15078758847), CI 45736783251, expira 2026-12-10T01:36:36Z. Baixado e analisado sem executar arquivos desconhecidos. ZIP externo 5.713 bytes, SHA-256 recalculado b58b4c63642120f7eba2fa4e7b88a82383cea6f86486b5b56d4927c545fc3511, igual ao digest API.
- ZIP interno Lilium-Mini-0.1.1-experimental.zip: 5.567 bytes; SHA-256 recalculado 5fde935bfcd3bb3f2e1dda983b54a431b380f56c9ce85808608e17b89a524cf7, igual ao arquivo .sha256 do artefato. CRC dos dois ZIPs aprovado; seis entradas únicas esperadas, sem criptografia, symlinks ou executáveis nativos.
- Os seis blobs Git recalculados das entradas coincidem com o commit público. PNG 128x128: assinatura, dimensões, CRC de chunks e fim do arquivo verificados. Digest anterior b72dc762... do README refere-se a build local histórico diferente; não é digest deste artefato.
| Arquivo | SHA-256 |
|---|---|
| icon128.png | 4c40dbc6b97893c14a9787579e81e113f0da453372748b53d8dd46b47990e139 |
| manifest.json | e70b6b79aa00e2dd1b8b42524bb7ebba70d3dbe68a053fd57a55039b393fa180 |
| math.js | 9756e0f0cda650f93fa9864983c9cf6751c341eaea092a2aa5c5c8fd49145a49 |
| popup.css | 738841e6cc4a8901b6fcecd5140555b3922882c98f8870966d788716a84b2660 |
| popup.html | b7b2b8528db0c64f3a727a88c1feb5199a6085f38bca118a34fa0140f5555ae3 |
| popup.js | 7787b9f8e49aafb36b5cf17954a3ec3934e6bfaa423ca633b7a6d789fe5242e2 |

## Revisão
- Manifest V3: action/popup e ícone; nenhuma permissão especial, host permission, background, content script ou native messaging declarada. Sem dependências externas de runtime no pacote.
- math.js: cálculos locais de resultado, preço e ponto de equilíbrio, com centavos inteiros, BigInt no arredondamento de preço e validação de entradas. Nenhuma execução dinâmica de texto, rede ou acesso a arquivos.
- popup.js: DOM por textContent, submissão interceptada por preventDefault, renderização e limpeza de resultado; nenhum armazenamento persistente ou envio automático observado. popup.html/css locais, link explícito para Insights oficial com noopener/noreferrer e sem valores das calculadoras. Ícone PNG estático.
- package_mini.py: lista fixa de seis arquivos, rejeita symlinks, valida manifesto, ZIP determinístico e paridade; usa apenas biblioteca padrão Python. Testes: Node e Playwright/Chromium (somente ambiente de teste). Sem auditoria transitiva das ferramentas de CI.
- Nenhum comportamento malicioso evidente identificado nos seis arquivos. Limites: ferramentas demonstrativas, não contábeis; revisão estática não comprova ausência de malware.

## Testes
- Execução local nesta etapa: Node v22.16.0, sintaxe de math.js e popup.js aprovada. 12/12 testes existentes em math.test.js (blob conferido 1dd8fa5e39dab59b20cdda729a3d5e44925ef134), executados contra math.js extraído do artefato original.
- CI anterior [45736783251](https://github.com/Kgasil/lilium/actions/runs/45736783251) concluída com sucesso: testes de cálculo, regressão de popup Chromium em página local, build duplicado e upload. Runtime idêntico ao atual; não representa nova execução de interface nem instalação nativa.
- Novo verificador tests/verify_mini_original.py: fixa blobs da versão distribuída, verifica PNG e manifesto e usa packager existente em diretório temporário sem publicar ou substituir pacotes. Adicionado ao workflow existente. Nova CI a confirmar.
- Defender atualizado e instalação real Chrome/Edge, assinatura e loja permanecem pendentes. Sem alterações no runtime, sem publicação de novo release ou custo contratado.

## Nova CI
[Execução 45880059459](https://github.com/Kgasil/lilium/actions/runs/45880059459), commit `13877d8b9b6366913d2eb612e564ea04d7cd453d`: verificação dos blobs fixados, PNG, construção temporária duplicada, sintaxe JS e regressão de cálculo aprovadas. Na última consulta, instalação das dependências de teste Chromium ainda em andamento; nova regressão de interface e upload pendentes. Comparação main/backup confirmou apenas três arquivos de documentação e validação alterados/adicionados. Sem alterações no runtime ou no link de distribuição pública.
