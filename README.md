# Project Lilium
**Where strategy meets intelligence.** · Business Intelligence & Innovation

[Website](https://kgasil.github.io/lilium/) · [K&G Vision](https://kgasil.github.io/) · [Português](#português) · [English](#english)

## Português
Lilium é uma iniciativa independente da K&G Vision para desenvolver uma aplicação web de inteligência empresarial, com foco inicial em pequenas e médias empresas. A proposta é transformar planilhas em indicadores verificáveis, relatórios executivos e apoio a decisões. 

**Status:** website institucional e conceito de produto. Não há aplicação comercial disponível, integração de IA ativa, consultoria oferecida ou data de lançamento anunciada. O site pode incluir demonstrações locais com dados fictícios.

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
Lilium is an independent K&G Vision initiative exploring a modular business intelligence web application. The initial focus is validated spreadsheet analytics and executive reporting; future AI capabilities will explain verified metrics, with source references and human oversight. The proposed modules and architecture above are planned, not production-ready. No commercial services or public application release are currently offered.

## Ecosystem / Ecossistema
| Project | Website | Repository |
| --- | --- | --- |
| K&G Vision | [Institutional](https://kgasil.github.io/) | [Source](https://github.com/Kgasil/kgasil.github.io) |
| Genesis | [O Princípio](https://kgasil.github.io/genesis/) | [Source](https://github.com/Kgasil/genesis) |
| Vision | [Beyond Boundaries](https://kgasil.github.io/vision/) | [Source](https://github.com/Kgasil/vision) |
| Aeris | [Naturalmente bom.](https://kgasil.github.io/aeris/) | [Source](https://github.com/Kgasil/aeris) |
| Lilium | [Where strategy meets intelligence.](https://kgasil.github.io/lilium/) | [Source](https://github.com/Kgasil/lilium) |

**Learn · Build · Simplify · Transform / Aprender · Construir · Simplificar · Transformar**

## Repository
`index.html` — bilingual responsive website. GitHub Pages: main / root (requires activation in repository settings). Future commercial implementation may be maintained privately. License terms are not yet specified.
