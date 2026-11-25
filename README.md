<p align="center"><a href="https://kgasil.github.io/lilium/"><img src="assets/readme-cover.svg" alt="Project Lilium — official project identity" width="760"></a></p>

# Project Lilium
**Strategy & Growth · Estratégia e Crescimento**  
*Make smarter decisions. Grow with confidence.*

[Website](https://kgasil.github.io/lilium/) · [K&G Vision](https://kgasil.github.io/) · [Português](#português) · [English](#english)

## Português
Lilium é uma iniciativa independente da K&G Vision para desenvolver uma aplicação web de inteligência empresarial, com foco inicial em pequenas e médias empresas. A proposta é transformar planilhas em indicadores verificáveis, relatórios executivos e apoio a decisões. 

**Status:** website institucional, primeiro protótipo local de indicadores e prévia de desenvolvimento da extensão Lilium Mini. [Experimente Lilium Insights](https://kgasil.github.io/lilium/demo.html). O Lilium Core v0.14.0 e o Workspace local já estão em desenvolvimento e disponíveis para testes. Não há aplicação comercial, integração de IA ativa, consultoria oferecida ou data de lançamento anunciada.

### Lilium Business Suite
| Módulo planejado | Escopo |
|---|---|
| Insights | Importação CSV/XLSX, validação, indicadores e dashboards |
| Reports | Relatórios executivos com evidências |
| Finance | Receitas, custos, margens, fluxo de caixa |
| Flow | Automação com aprovação humana |
| Sales | Inteligência comercial e CRM |
| Operations | Indicadores de eficiência e gargalos |
| Strategy | Metas e cenários |
| Forecast | Previsões com validação histórica |
| Copilot | Perguntas sobre dados e explicações fundamentadas |
| Connect | Integrações de leitura com APIs, CRM e ERP |

### Arquitetura proposta
Python/FastAPI, DuckDB para análise local inicial, PostgreSQL para futura operação multiempresa, React/TypeScript para interface e adaptadores de modelos de IA no backend. O motor de cálculo determinístico será separado do modelo de linguagem. A IA receberá apenas dados autorizados e minimizados, citará métricas e fontes, não executará SQL arbitrário ou ações externas sem autorização. Isolamento por organização, permissões, testes e trilhas de auditoria são requisitos antes de qualquer piloto real.

### Roadmap
1. Importação CSV, validação de esquema, indicadores determinísticos e relatório exportável.
2. XLSX, histórico de períodos, visualizações e testes automatizados.
3. Copilot com evidências, adaptador de IA e avaliação de respostas.
4. Integrações, autenticação, isolamento multiempresa e piloto controlado.
5. Avaliação comercial; eventual SaaS e serviços de implantação.

## English
Lilium is built around a clear ambition: empower small businesses to make smarter decisions, operate with confidence and grow sustainably. This independent K&G Vision initiative is developing a modular business intelligence web application. The initial focus is validated spreadsheet analytics and executive reporting; future AI capabilities will explain verified metrics, with source references and human oversight. The proposed modules and architecture above are planned, not production-ready. A local metrics prototype is available; no commercial services or production application release are currently offered.

## Ecosystem / Ecossistema
| Project | Website | Repository |
| --- | --- | --- |
| K&G Vision | [Institutional](https://kgasil.github.io/) | [Source](https://github.com/Kgasil/kgasil.github.io) |
| Genesis | [Wisdom & Application / Sabedoria e Aplicação](https://kgasil.github.io/genesis/) · [Interactive library / Biblioteca interativa](https://kgasil.github.io/genesis/biblioteca.html) | [Source](https://github.com/Kgasil/genesis) |
| Vision | [Security & Efficiency](https://kgasil.github.io/vision/) | [Source](https://github.com/Kgasil/vision) |
| Aeris | [Discreto e Eficiente.](https://kgasil.github.io/aeris/) | [Source](https://github.com/Kgasil/aeris) |
| Lilium | [Strategy & Growth / Estratégia e Crescimento](https://kgasil.github.io/lilium/) | [Source](https://github.com/Kgasil/lilium) |

**Learn · Build · Simplify · Transform / Aprender · Construir · Simplificar · Transformar**

## Protótipo local / Local prototype

- `demo.html`: CSV restrito (`date,revenue,cost`), valores BRL não negativos com até duas casas decimais, datas ISO, agregação mensal, receita, custos, resultado, margem e exportação TXT. Processamento no navegador, sem conexão com IA. Use dados sintéticos.
- Oito verificações unitárias do cálculo executadas antes do commit: totais, receita zero, precisão decimal, data inválida, cabeçalho inválido, valores negativos, precisão inválida e agregação mensal. Não são testes de segurança ou de interface no navegador.
- **Lilium Core v0.14.0:** Python/FastAPI, contrato de métricas, validação de CSV, API local e Workspace inicial. 30 testes Python/API aprovados na v0.3; 295 testes JavaScript reexecutados com sucesso na v0.14 em V8. A regressão Python e a geração/validação do executável Windows estão configuradas no workflow, mas ainda não foram confirmadas; impressão e UI completa também pendentes. Histórico opcional em SQLite (até 200 análises consolidadas, sem armazenar CSV original); banco não criptografado pelo aplicativo.
- [Instruções para executar no Windows / Local setup](core/README.md) · [Código do Core](core/) · [Testes](tests/test_core.py).
- Smart Import & Data Quality: CSV/XLSX de uma aba, diagnóstico por linha, alertas de possíveis duplicatas e receita zero; erros bloqueiam a análise. Sem correção automática. Limites de arquivo e formato em [Core](core/README.md).
- Professional Workspace: menu lateral responsivo, filtros mensais inclusivos, gráfico de receita/custos, tabela e exportação CSV do período. JSON e histórico preservam a análise completa. [Testes do dashboard](tests/dashboard.test.js).
- **Lilium Finance:** precificação por margem de contribuição, simulação mensal de produto único, custos fixos e variáveis, taxas, ponto de equilíbrio, meta de resultado e exportação JSON de premissas e resultados. Cálculos locais em centavos inteiros; sem armazenamento automático. [Testes do Finance](tests/finance.test.js).
- **Lilium Sales:** CSV de vendas por pedido e produto, receita bruta, ticket médio por pedido distinto, volume, ranking de produtos, filtros mensais e exportação JSON de agregados. Processamento em memória no navegador, sem persistência. [Testes Sales](tests/sales.test.js).
- **Lilium Operations:** indicadores por etapa, OEE, disponibilidade, performance, qualidade, produtividade, retrabalho, lead time informado, capacidade teórica e gargalo estimado em linha serial, simulação de redução de paradas e exportação JSON. Processamento local sem persistência automática. [Testes Operations](tests/operations.test.js).
- **Lilium Strategy:** metas e OKRs ponderados, avaliação de prazos, comparação de cenários hipotéticos, priorização impacto × urgência ÷ esforço e exportação JSON. Entrada manual via CSV colado; sem integração automática de outros módulos ou persistência. [Testes Strategy](tests/strategy.test.js).
- **Lilium Reports:** seleção de seis fontes da sessão, relatório executivo com escopo e natureza dos dados, prévia, exportação JSON/TXT e impressão pelo navegador (opção de salvar PDF). Sem soma entre módulos, persistência automática ou IA. [Testes Reports](tests/reports.test.js).
- **Lilium Forecast:** previsão mensal de 1–12 meses, três modelos estatísticos, validação temporal de um passo, MAE/RMSE/WAPE, seleção automática ou manual, importação de receita do Insights e exportação JSON. Sem intervalos de confiança, persistência ou IA externa. [Testes Forecast](tests/forecast.test.js).
- **Lilium Flow:** regras condicionais sobre seis indicadores, avaliação manual, propostas com evidências, fila de aprovação humana, deduplicação na sessão, conclusão manual declarada e exportação JSON de eventos. Sem execução externa, agendamento ou persistência. [Testes Flow](tests/flow.test.js).
- **Lilium Connect:** mapeamento de colunas CSV/TSV, conversão decimal opcional, validação de destino, prévia, exportação CSV/pacote JSON v1.0 e transferência confirmada para Insights, Sales ou Forecast. Sem conectores externos ou persistência. [Testes Connect](tests/connect.test.js).
- **Lilium Copilot:** assistente determinístico local com oito tópicos guiados, indicadores com fontes e escopos, limites de alerta configuráveis, sugestões com evidências, encaminhamento confirmado ao Flow com revalidação e exportação JSON. Sem IA generativa, voz ou conexão externa. [Testes Copilot](tests/copilot.test.js).
- **Lilium Desktop v0.14:** inicializador local com abertura automática no navegador, porta dinâmica loopback, histórico em `%LOCALAPPDATA%`, ícone oficial e receita de empacotamento portátil Windows x64 com PyInstaller. [Instruções Desktop](desktop/README.md) · [Validação Windows](https://github.com/Kgasil/lilium/actions/workflows/desktop-windows.yml). Executável ainda não confirmado, sem instalador assinado ou lançamento público.
- **Preparação do piloto:** tela inicial guiada, reinício da sessão sem apagar histórico, cabeçalhos de segurança do Workspace, teste de navegador Chromium configurado no workflow e [critérios de liberação e feedback](docs/pilot-readiness.md). Ainda não há V1.0 pública; testes Windows e navegador pendentes de confirmação.

## Lilium Mini — extensão gratuita / free extension

[Instalação para testes / Test installation](extension/README.md) · [Código / Source](extension/)

Prévia v0.1.0 para Chromium (Chrome/Edge): resultado e margem, preço por margem desejada e ponto de equilíbrio. Sem permissões de acesso a sites, armazenamento, conta ou IA conectada. Doze verificações de cálculo passaram; instalação e interface ainda não testadas em navegador. Não publicada nas lojas de extensões.

Estratégia: manter a extensão útil e gratuita; desenvolver uma aplicação web com funções básicas gratuitas, futura instalação Windows e recursos profissionais opcionais pagos somente após validação. Nenhum preço definido.

## Repository
`index.html` — bilingual responsive website. GitHub Pages: main / root (requires activation in repository settings). Future commercial implementation may be maintained privately. License terms are not yet specified.

## Identidade K&G Vision / K&G Vision identity

<p align="center"><a href="https://kgasil.github.io/"><img src="https://raw.githubusercontent.com/Kgasil/kgasil.github.io/main/assets/brand-banner.svg" alt="K&amp;G Vision — institutional identity" width="420"></a></p>

[Versão vertical / Vertical lockup](https://github.com/Kgasil/kgasil.github.io/blob/main/assets/brand-stacked.svg) · [Escudo / Shield](https://github.com/Kgasil/kgasil.github.io/blob/main/assets/kg-symbol.svg)

Official visual lockup: **K&G** above **Vision**; individual project symbols are retained. / Assinatura visual oficial: **K&G** acima de **Vision**, mantendo os símbolos individuais dos projetos.

**Genesis (purple) · Vision (blue) · Aeris (green) · Lilium (rose)**

[Experimentar Lilium Insights / Try Lilium Insights (PT-BR)](https://kgasil.github.io/lilium/demo.html) — local prototype, no connected AI or commercial offering.

## Product direction / Direção do produto

[Product vision and roadmap](docs/product-vision.md) — proposed product scope, MVP, integration and AI principles; not available features.

### Validação técnica da prévia v0.14
295 testes de módulos e 12 verificações estáticas do Workspace aprovados em V8 (307 verificações). Controlador JavaScript separado do HTML, CSP bloqueando scripts inline, aviso de inicialização e cobertura adicional no workflow. A execução Python, Chromium e Windows ainda precisa ser confirmada. [Critérios do piloto](docs/pilot-readiness.md).

### Backup e recuperação do histórico
Exporte e recupere análises salvas no Workspace. JSON versionado de até 16 MiB, validação de consistência, recuperação por adição sem sobrescrita, deduplicação e reversão transacional em caso de conflito. Nove novos testes Python aprovados localmente (arquivos idênticos aos publicados); testes da API e do navegador da versão atual ainda pendentes. Não inclui os dados originais nem os resultados de outros módulos; arquivo sem criptografia. [Guia Desktop](desktop/README.md).
