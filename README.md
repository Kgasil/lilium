<p align="center"><a href="https://kgasil.github.io/lilium/"><img src="assets/readme-cover.svg" alt="Project Lilium — official project identity" width="760"></a></p>

# Project Lilium

<!-- kg-personal-portfolio-v1 -->

**Idealizador / Creator:** [Kaio Gabriel da Silva — KG Professional Portfolio 1.0](https://kgasil.github.io/portfolio/) · [GitHub](https://github.com/Kgasil) · [LinkedIn](https://www.linkedin.com/in/kaio-gabriel-da-silva). Portfólio pessoal independente do projeto / Personal portfolio separate from this project.

<!-- kg-current-training -->
**Formação e trajetória do idealizador / Creator's education and experience:** [Currículo público atualizado / Updated public résumé](https://kgasil.github.io/portfolio/resume.html) · [Portfólio / Portfolio](https://kgasil.github.io/portfolio/). A formação pessoal é independente dos produtos e materiais do projeto / Personal training is independent of project products and materials.

**Strategy & Evolution · Estratégia e Evolução**  
*Make smarter decisions. Grow with confidence.*

[Website](https://kgasil.github.io/lilium/) · [K&G Vision](https://kgasil.github.io/) · [Português](#português) · [English](#english)

> **25/11/2026 — Initial development milestone / Desenvolvimento inicial concluído.** Prévia v0.14.0 validada em CI, 501 testes Python e Node.js aprovados, aceitação manual pendente. [Comunicado / Announcement](docs/milestone-2026-11-25.md) · [Interactive Lab](https://kgasil.github.io/lilium/#lab) · [Guia Windows](docs/clean-machine-validation.md) · [Changelog / Histórico](CHANGELOG.md).

> **Marco 1.0 — Lilium Web Lab.** Demonstrações públicas de inteligência empresarial; Desktop v0.14.0 continua em prévia controlada e Mini v0.1.1 é experimental. [Experimente / Try the Web Lab](https://kgasil.github.io/lilium/#lab).

**Papel no ecossistema / Ecosystem role:** No ecossistema K&G Vision, o Lilium explora como transformar dados e cenários em informação útil para decisões estratégicas. / Within the K&G Vision ecosystem, Lilium explores how to turn data and scenarios into useful information for strategic decisions.

## Lilium Web Lab 1.0 — public edition / edição pública

[**Experimentar Web Lab 1.0 / Try Web Lab 1.0**](https://kgasil.github.io/lilium/#lab) · [Launch announcement / Comunicado](docs/web-lab-v1.0.md). Public synthetic-data demonstrations of financial analytics, pricing, scenarios and forecasts. Version 1.0 applies to the web lab only; Desktop remains v0.14.0 and the Desktop pilot is closed.

| Product / Produto | Version / Versão | Scope / Escopo |
| --- | --- | --- |
| [Web Lab](https://kgasil.github.io/lilium/#lab) | 1.0 | Public browser demonstrations / Demonstrações públicas no navegador |
| [Desktop](docs/clean-machine-validation.md) | 0.14.0 | Controlled Windows preview; manual results pending / Prévia Windows controlada; resultados manuais pendentes |
| [Mini](extension/README.md) | 0.1.1 | Experimental Chrome/Edge extension; not in stores / Extensão experimental Chrome/Edge; não publicada nas lojas |

## Current release status / Estado atual da liberação

> **Copilot candidate / Candidato Copilot:** [Etapa 04](docs/stage-04-copilot-2026-11-27.md). Free-text topic routing by rules or optional local Ollama model; deterministic evidence and human-reviewed suggestions. No generative financial claims, external cloud integration or public package change. Local model execution still requires validation.

> **Data Intelligence candidate / Candidato de dados:** [Etapa 03](docs/stage-03-data-2026-11-27.md). CSV brasileiro explícito, colunas canônicas reordenadas, meta de margem, gráfico de resultado e diagnóstico JSON. Desktop source preview only; public Web Lab and Mini downloads unchanged. No release approval.

> **Experience development / Desenvolvimento visual:** [Etapa 02 — escopo e critérios](docs/stage-02-experience-2026-11-27.md). The dark Workspace and Mini 0.1.2 are development candidates, not the approved distributed packages. / Workspace escuro e Mini 0.1.2 são candidatos de desenvolvimento, não os pacotes distribuídos aprovados. Current public links and versions below remain unchanged.

**v0.14.0 — controlled acceptance only / somente aceitação controlada.** The designated Windows artifact is the remediated build from [run 45722415976](https://github.com/Kgasil/lilium/actions/runs/45722415976). Automated build, independent portable verification and focused browser review passed. Manual Windows acceptance, manual security/accessibility review and pilot approval remain open. The unsigned preview must not be used with real data; do not bypass OS warnings.

**Next action / Próxima ação:** [Windows acceptance guide](docs/clean-machine-validation.md) · [23-case manual acceptance matrix](docs/manual-acceptance-matrix.md) · [Release gate tracker #1](https://github.com/Kgasil/lilium/issues/1) · [Pilot handbook](docs/pilot-handbook.md).

The following technical milestones record historical results as of each checkpoint; earlier references to pending CI do not supersede the latest successful candidate evidence. Additional reference suites are published; their full Windows CI results remain unconfirmed. No Desktop V1.0 release or open Desktop pilot.

## Português
Lilium é uma iniciativa independente da K&G Vision para desenvolver uma aplicação web de inteligência empresarial, com foco inicial em pequenas e médias empresas. A proposta é transformar planilhas em indicadores verificáveis, relatórios executivos e apoio a decisões. 

**Status:** Web Lab 1.0 público, demonstração CSV do Insights, extensão Mini v0.1.1 experimental e Workspace local v0.14.0 com módulos iniciais implementados em código. [Experimente o laboratório](https://kgasil.github.io/lilium/#lab) · [Demonstração Insights](https://kgasil.github.io/lilium/demo.html). Prévia Windows v0.14.0 corrigida aprovada na CI e na auditoria de dependências; disponível somente para aceitação manual com dados fictícios. Não há versão comercial, IA conectada ou data de lançamento anunciada para o Desktop.

### Lilium Business Suite
| Módulo | Escopo atual e futuro |
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
Python/FastAPI e SQLite no histórico local atual; DuckDB em avaliação futura, PostgreSQL para futura operação multiempresa, React/TypeScript para interface e adaptadores de modelos de IA no backend. O motor de cálculo determinístico será separado do modelo de linguagem. A IA receberá apenas dados autorizados e minimizados, citará métricas e fontes, não executará SQL arbitrário ou ações externas sem autorização. Isolamento por organização, permissões, testes e trilhas de auditoria são requisitos antes de qualquer piloto real.

### Roadmap
1. Importação CSV, validação de esquema, indicadores determinísticos e relatório exportável.
2. XLSX, histórico de períodos, visualizações e testes automatizados.
3. Copilot com evidências, adaptador de IA e avaliação de respostas.
4. Integrações, autenticação, isolamento multiempresa e piloto controlado.
5. Avaliação comercial; eventual SaaS e serviços de implantação.

## English
Lilium is built around a clear ambition: empower small businesses to make smarter decisions, operate with confidence and grow sustainably. This independent K&G Vision initiative is developing a modular business intelligence web application. The initial focus is validated spreadsheet analytics and executive reporting; future AI capabilities will explain verified metrics, with source references and human oversight. Explore the interactive business lab and the local Workspace v0.14.0 source preview. Initial analytics modules are implemented; external integrations, connected AI and production deployment remain planned. The remediated Windows preview passed dependency review and full functional CI; clean-machine acceptance remains pending. No commercial services or production release are offered.

## GRAAL — Ecosystem / Ecossistema · Marco 01

| Project | Website | Repository | Current stage / Etapa atual |
| --- | --- | --- | --- |
| K&G Vision | [Institutional](https://kgasil.github.io/) | [Source](https://github.com/Kgasil/kgasil.github.io) | Independent initiative / Iniciativa independente |
| Project Genesis | [Wisdom & Application / Sabedoria e Aplicação](https://kgasil.github.io/genesis/) | [Source](https://github.com/Kgasil/genesis) | **1.0 — Editorial & Library / Acervo e biblioteca.** 75 private study PDFs; [public interactive library](https://kgasil.github.io/genesis/biblioteca.html) / 75 PDFs privados; biblioteca pública interativa, sem cursos ou certificados. · [Genesis Mini — complemento gratuito](https://kgasil.github.io/genesis/mini/) · [Instalar extensão / Install extension](https://kgasil.github.io/genesis/#instalar-extensao) |
| Project Rubedo | [Science & Innovation / Ciência e Inovação](https://kgasil.github.io/rubedo/) | [Source](https://github.com/Kgasil/rubedo) | **Marco 01 — Public Lab 1.0.** [Research Workspace 1.0](https://kgasil.github.io/rubedo/research/) · [Mini Lab 1.0.0](https://kgasil.github.io/rubedo/mini/) · [Instalação manual / Manual installation](https://kgasil.github.io/rubedo/#instalar); experimental, no store distribution. |
| Project Argus | [Security & Development / Segurança e Desenvolvimento](https://kgasil.github.io/argus/) | [Source](https://github.com/Kgasil/argus) | **1.0 — Public Research Lab / Laboratório público.** Technical baseline V10.2; local demonstrations / Base técnica V10.2; demonstrações locais, não serviços de produção. [Argus Mini — amostra complementar / complementary sample](https://kgasil.github.io/argus/mini/), v0.1.0; original milestone unchanged / marco original preservado. · [Instalar extensão / Install extension](https://kgasil.github.io/argus/#instalar-extensao) |
| Project Aeris | [Efficiency & Simplicity / Eficiência e Simplicidade](https://kgasil.github.io/aeris/) | [Source](https://github.com/Kgasil/aeris) | **1.0 — Extension 1.0.0; Desktop 1.1.0 RC1.** Public experimental preview, not stable / Prévia pública experimental, não estável. [Desktop e extensão — instalação, avisos e evidências / installation, warnings and evidence](https://kgasil.github.io/aeris/#instalacao) |
| Project Lilium | [Strategy & Evolution / Estratégia e Evolução](https://kgasil.github.io/lilium/) | [Source](https://github.com/Kgasil/lilium) | **1.0 — Web Lab.** Public demo / demonstração pública; Desktop v0.14.0 controlled preview / prévia controlada; [Mini v0.1.1](https://github.com/Kgasil/lilium/tree/main/extension) experimental. |

**Version note / Nota de versão:** 1.0 identifies the first completed public-facing project milestone of the ecosystem, not a uniform software release tag. Genesis is an editorial milestone; Argus retains technical baseline V10.2; Aeris 1.0.0 applies to Extension; Lilium 1.0 applies to Web Lab. / 1.0 identifica o primeiro marco público do ecossistema, não uma tag de software uniforme. Genesis é um marco editorial; Argus mantém a base V10.2; Aeris 1.0.0 refere-se à extensão; Lilium 1.0 refere-se ao Web Lab. Desktop previews are not stable releases / Prévias Desktop não são versões estáveis.

**Learn · Build · Protect · Simplify · Evolve / Aprender · Construir · Proteger · Simplificar · Evoluir**

## Protótipo local / Local prototype

- `demo.html`: CSV restrito (`date,revenue,cost`), valores BRL não negativos com até duas casas decimais, datas ISO, agregação mensal, receita, custos, resultado, margem e exportação TXT. Processamento no navegador, sem conexão com IA. Use dados sintéticos.
- Oito verificações unitárias do cálculo executadas antes do commit: totais, receita zero, precisão decimal, data inválida, cabeçalho inválido, valores negativos, precisão inválida e agregação mensal. Não são testes de segurança ou de interface no navegador.
- **Lilium Core v0.14.0:** Python/FastAPI, contrato de métricas, validação de CSV, API local e Workspace inicial. 30 testes Python/API aprovados na v0.3; 295 testes JavaScript reexecutados com sucesso na v0.14 em V8. A regressão completa, o executável Windows corrigido e a geração automatizada de PDF foram aprovados em CI; aceitação manual e inspeção visual pendentes. Histórico opcional em SQLite (até 200 análises consolidadas, sem armazenar CSV original); banco não criptografado pelo aplicativo.
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
- **Preparação do piloto:** tela inicial guiada, reinício da sessão sem apagar histórico, cabeçalhos de segurança do Workspace, teste de navegador Chromium configurado no workflow e [critérios de liberação e feedback](docs/pilot-readiness.md). Ainda não há V1.0 pública; CI Windows e Chromium do candidato designado aprovadas, aceitação manual pendente.

## Lilium Mini — extensão gratuita / free extension

[**Instalar no Chrome ou Edge — tutorial / Installation guide**](extension/README.md) · [Baixar código v0.1.1 / Download source ZIP](https://github.com/Kgasil/lilium/archive/447d7414f20e28f6c0440647f2b7be71fc44e71d.zip) · [Privacidade / Privacy](https://kgasil.github.io/lilium/mini-privacy.html) · [Código / Source](extension/)

Prévia v0.1.1 distribuída exclusivamente pelo GitHub, com instalação manual no Chrome/Edge: resultado e margem, preço por margem desejada e ponto de equilíbrio. Sem permissões de acesso a sites, armazenamento, conta ou IA conectada. Doze verificações de cálculo passaram; o responsável relatou ter testado a v0.1.0. A aceitação detalhada da v0.1.1 permanece pendente. Não publicada nas lojas de extensões.

Estratégia: manter a extensão útil e gratuita; desenvolver uma aplicação web com funções básicas gratuitas, prévia portátil Windows e eventuais recursos profissionais opcionais somente após validação. Nenhum preço definido.

## Repository
`index.html` — bilingual responsive website. GitHub Pages: main / root (requires activation in repository settings). Future commercial implementation may be maintained privately. License terms are not yet specified.

## Identidade K&G Vision / K&G Vision identity

<p align="center"><a href="https://kgasil.github.io/"><img src="https://raw.githubusercontent.com/Kgasil/kgasil.github.io/main/assets/brand-banner.svg?v=20261127-graal" alt="K&amp;G Vision — institutional identity" width="420"></a></p>

[Versão vertical / Vertical lockup](https://github.com/Kgasil/kgasil.github.io/blob/main/assets/brand-stacked.svg) · [Escudo / Shield](https://github.com/Kgasil/kgasil.github.io/blob/main/assets/kg-symbol.svg)

Official visual lockup: **K&G** above **Vision**; individual project symbols are retained. / Assinatura visual oficial: **K&G** acima de **Vision**, mantendo os símbolos individuais dos projetos.

**Genesis (purple) · Rubedo (orange/gold) · Argus (blue) · Aeris (green) · Lilium (rose)**

O escudo institucional preserva as quatro cores laterais e o núcleo branco; Rubedo ocupa apenas as pontas centrais superior (laranja) e inferior (dourado). / The institutional shield preserves its four side colors and white core; Rubedo occupies only the upper (orange) and lower (gold) central tips.


[Interactive Lab / Laboratório interativo](https://kgasil.github.io/lilium/#lab) · [Insights CSV demo](https://kgasil.github.io/lilium/demo.html) — synthetic exercises, no connected AI or commercial offering.

## Product direction / Direção do produto

[Product vision and roadmap](docs/product-vision.md) — proposed product scope, MVP, integration and AI principles; not available features.

### Validação técnica da prévia v0.14
295 testes de módulos e 12 verificações estáticas do Workspace aprovados em V8 (307 verificações). Controlador JavaScript separado do HTML, CSP bloqueando scripts inline, aviso de inicialização e cobertura adicional no workflow. A execução Python, Chromium e Windows ainda precisa ser confirmada. [Critérios do piloto](docs/pilot-readiness.md).

### Backup e recuperação do histórico
Exporte e recupere análises salvas no Workspace. JSON versionado de até 16 MiB, validação de consistência, recuperação por adição sem sobrescrita, deduplicação e reversão transacional em caso de conflito. Nove novos testes Python aprovados localmente (arquivos idênticos aos publicados); testes da API e do navegador da versão atual ainda pendentes. Não inclui os dados originais nem os resultados de outros módulos; arquivo sem criptografia. [Guia Desktop](desktop/README.md).

### Setup & Diagnostics
Inicializador de código-fonte para Windows x64/Python 3.12, identificação de alterações em requirements.txt por SHA-256, reparo manual confirmado e diagnóstico local sem ler histórico real. Oito testes Python aprovados em Linux, com instalação simulada; hashes dos três arquivos testados coincidem com o GitHub. A validação do executável e do workflow Windows permanece pendente. [Guia de manutenção](desktop/README.md).

### Release & Update Manager
Gerenciador offline de pacote ZIP portátil, manifesto versionado, SHA-256, validação de caminhos Windows e preparação em pasta nova sem substituir a versão anterior. Nove testes Python aprovados em Linux com arquivos sintéticos; código publicado idêntico ao testado. CI Windows configurada para empacotar, validar e testar a cópia extraída antes de disponibilizar o artefato. Sem atualização automática, assinatura digital ou lançamento público. [Guia de versões](desktop/README.md).

### Trust & Privacy
Desktop usa token aleatório por execução, validação de origem e bloqueio de requisições sem autorização na API; o navegador remove o token da URL e o mantém na sessão da aba. Doze testes de política aprovados localmente, cinco testes integrados adicionados (execução pendente). Modo direto de desenvolvimento sem proteção; sem contas, criptografia de arquivos ou certificação de conformidade. [Privacidade e limites](docs/trust-privacy.md).

### Quality Assurance — histórico e sessões
Corrigida falha de histórico inconsistente: leitura, exportação e recuperação com conflito retornam erro estruturado, sem reparo automático ou exclusão. Sete novos testes integrados. Nesta revisão, 83 testes Python passaram em Linux (Python 3.13.5, cópia local com backend e testes conferidos por hash; 12 casos dependentes de assets excluídos, testes Desktop não executados) e 307 verificações JavaScript/estáticas passaram em V8 a partir do GitHub. A compilação Windows, Chromium e validação final continuam pendentes. [Registro QA e critérios do piloto](docs/pilot-readiness.md).

### User Experience & Accessibility
Navegação agrupada por objetivo, seis atalhos de tarefas, glossário, foco de teclado, link para pular navegação, estado de âncora ativa e acessibilidade estrutural das 12 tabelas. Onze verificações novas aprovadas em V8; testes reais de navegador, leitor de tela e Windows pendentes. [Critérios do piloto](docs/pilot-readiness.md).

### Business Starter Kit
Cinco cenários totalmente fictícios (comércio, serviços, indústria, restaurante e loja virtual), cada um com sete conjuntos de exercício para Insights, Sales, Finance, Operations, metas e prioridades Strategy, Forecast. Receita mensal coerente entre Insights, Sales e Forecast; pedidos agregados sintéticos e hipóteses independentes nos demais exercícios. Carregamento confirmado por conjunto ou completo, exportação CSV/JSON e preservação de histórico e fila Flow. 47 testes de cenários e 23 verificações estáticas/UX aprovados em V8. Integração real no navegador e Windows ainda pendente. [Guia de exercícios](docs/starter-kit.md).

### Help Center e encerramento do escopo inicial
Central de ajuda offline com 15 guias, busca local sem acentos, atalhos para os módulos e modelo TXT de relato sem dados confidenciais. 13 novos testes de ajuda e 23 verificações anteriores de interface aprovados em V8. Teste real no navegador pendente. Proposta de congelar novas funcionalidades até completar três etapas: validação integrada e pacote Windows; validação manual, segurança e acessibilidade; piloto gratuito controlado com dados fictícios. [Critérios e resultados](docs/pilot-readiness.md).

### Validação integrada — fase final 1 (parcial)
86 testes Python aprovados em Linux (14 casos dependentes da interface atual excluídos); 342 testes de módulos e 36 verificações estruturais aprovados em V8. Novo teste HTTP real de três inicializações, rotação de token, persistência e recuperação de backup aprovado localmente. Workflow exige esses testes no código-fonte e no executável e testes Chromium em ambos. A fase permanece aberta: falta confirmação do workflow Windows, regressão completa e artefato. [Validação Windows](https://github.com/Kgasil/lilium/actions/workflows/desktop-windows.yml) · [Critérios](docs/pilot-readiness.md).

### Interactive Lab / Laboratório público
Formação de preços, simulação mensal, ponto de equilíbrio e metas, cinco cenários sintéticos com receita, custos, resultado, previsão e CSV para testar Insights. Reutiliza os motores Finance, Starter, Sales e Forecast; funciona no navegador sem API. 12 testes de cálculo e 11 verificações simuladas de DOM aprovados em V8. Publicação Pages e Chromium confirmados. O laboratório é uma demonstração separada do Desktop; não é uma oferta comercial.

[Public lab validation workflow](https://github.com/Kgasil/lilium/actions/workflows/public-lab.yml) · [Windows validation workflow](https://github.com/Kgasil/lilium/actions/workflows/desktop-windows.yml). The two gates are independent; a successful public demo does not validate the executable. Insights demo now rejects invalid UTF-8 and prevents a stale file read from replacing newer input.

### Resultado mais recente — Windows CI aprovada (25/11/2026)
100 testes Python, 401 verificações Node, Chromium real no código-fonte e executável, diagnóstico, reinicialização e recuperação, empacotamento e teste da cópia extraída aprovados. O laboratório público também passou no Chromium e o Pages confirmou a publicação. [Execução Windows bem-sucedida](https://github.com/Kgasil/lilium/actions/runs/45721198729) · Artefato anterior substituído como candidato (não utilizar) · [Roteiro de aceitação em máquina limpa](docs/clean-machine-validation.md). Não é um instalador assinado nem V1.0 liberada. Use apenas dados fictícios.

> **Revisão de segurança (25/11/2026):** a auditoria [45722053818](https://github.com/Kgasil/lilium/actions/runs/45722053818) apontou advisories em Pillow 12.0.0, Starlette 0.50.0 e pip 25.0.1. Os pacotes anteriores não estão aprovados para instalação. Candidato de correção: FastAPI 0.165.0, Starlette 1.10.0, Pillow 13.0.0 e pip 26.3; nova auditoria e regressão concluídas com sucesso no candidato corrigido. [Auditoria](https://github.com/Kgasil/lilium/actions/workflows/dependency-audit.yml).

### Candidato atual — CI e auditoria aprovadas
[Execução Windows #45722415976](https://github.com/Kgasil/lilium/actions/runs/45722415976) · [Prévia portátil corrigida](https://github.com/Kgasil/lilium/actions/runs/45722415976/artifacts/15071874653) · [Conferência SHA-256 e roteiro de teste](docs/clean-machine-validation.md). 100 testes Python e 401 verificações Node aprovados, Chromium real no código-fonte e executável, auditoria do build sem vulnerabilidades conhecidas detectadas. Artefato expira em 09/12/2026 UTC. Os anteriores continuam desaconselhados. Não é V1.0 pública nem instalador assinado; não use dados reais. Aceitação manual permanece pendente.

### Preparação final do piloto
[Manual do piloto controlado](docs/pilot-handbook.md) · [Aceitação do pacote em runner Windows independente](https://github.com/Kgasil/lilium/actions/workflows/portable-acceptance.yml) · [Roteiro manual em máquina limpa](docs/clean-machine-validation.md). A publicação Pages e os testes do site e Windows após a atualização de documentação foram confirmados. A prévia de referência continua sendo a execução 45722415976, com seu hash próprio. Nenhum piloto público foi aberto; a decisão depende da aceitação manual.

**Aceitação automatizada do pacote:** [execução independente aprovada #45723844030](https://github.com/Kgasil/lilium/actions/runs/45723844030), Windows Server 2025, ZIP exato baixado e conferido, seis diagnósticos e autoteste aprovados sem chamada a Python externo. A aceitação manual e a abertura do piloto continuam pendentes.

### Revisão técnica final
[Revisão de segurança, acessibilidade e impressão](docs/final-review.md) · [Validação complementar do pacote](https://github.com/Kgasil/lilium/actions/runs/45724967459). Revisão de primeira parte; não é auditoria independente nem certificação. A decisão de abertura do piloto permanece condicionada à aceitação manual.

**Aeris Extension 1.0.0** — 16 ferramentas, 50 testes automatizados aprovados; instalação manual disponível pelo GitHub. / 16 tools, 50 automated tests passed; manual installation available on GitHub. [Instalação / Installation](https://kgasil.github.io/aeris/extension-preview.html) · [Notas / Release notes](https://github.com/Kgasil/aeris/blob/main/release/extension-1.0.0-notes.md).

[![K&G Vision — GRAAL](https://raw.githubusercontent.com/Kgasil/kgasil.github.io/main/assets/kg-symbol.svg?v=20261126-2)](https://kgasil.github.io/) **GRAAL · Marco 01** — identidade integrada / integrated identity.

**GRAAL — Construir / Build (Rubedo):** [Rubedo Research Workspace](https://kgasil.github.io/rubedo/research/) · [Precisão / Precision (R06)](https://kgasil.github.io/rubedo/research/#precisao) · [Monte Carlo (R07)](https://kgasil.github.io/rubedo/research/#monte-carlo). Novos modelos experimentais; validação atual pendente / Experimental additions; current validation pending.

**Rubedo — edição 1.0 / 1.0 edition:** [Research Workspace 1.0](https://kgasil.github.io/rubedo/research/) · [Mini Lab 1.0.0](https://kgasil.github.io/rubedo/mini/) · [Mini Extension 1.0.0 — instalação manual / manual installation](https://kgasil.github.io/rubedo/#instalar). Edição experimental / Experimental edition.


**[Central de distribuição GRAAL / GRAAL distribution center](https://kgasil.github.io/distribuicao.html)** — versões, canais oficiais, limitações e estado de segurança / versions, official channels, limitations and security status.

<!-- graal-governance-v1:start -->
## Governança GRAAL / GRAAL governance

[**Catálogo central de componentes, versões, segurança e maturidade / Central catalog of components, versions, security and maturity**](https://github.com/Kgasil/kgasil.github.io/blob/main/docs/graal-catalog.md) · [Central de distribuição / Distribution center](https://kgasil.github.io/distribuicao.html)

O catálogo é a referência institucional para o estado atual; registros históricos e avisos específicos deste repositório permanecem aplicáveis. Em caso de divergência, prevalece o estado mais restritivo. / The catalog is the institutional reference for current status; this repository's historical records and specific notices remain applicable. If records disagree, the most restrictive state prevails.
<!-- graal-governance-v1:end -->
