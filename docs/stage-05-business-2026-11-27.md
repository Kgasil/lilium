# Etapa 05 — Business Intelligence
Base 95ca1464bb7bffd149714dddf76687cb4bfbaa21. Candidato, não publicado.
- Finance: DRE gerencial mensal simplificada e caixa mensal independente; centavos BigInt, margem indisponível se receita líquida não positiva. Sem conciliação, balanço, apuração tributária ou DRE oficial. Saldo inicial não negativo, saldo final pode ser negativo.
- Cenários reduzido/base/ampliado variam somente volume, usam simulate existente e não são previsão. JSON local. Resultados invalidados na edição.
- Reports: fonte DRE/caixa independente, cenários da simulação e KPIs adicionais de participação do produto líder, ganho teórico de capacidade, delta de metas. Copilot: tópico DRE/caixa, último mês previsto, mesmas fontes e regras humanas. Sem soma entre módulos, sem dados empresariais enviados ao modelo.
- Mantém dez módulos, identidade e escopos dos pacotes públicos. Sem novas dependências ou custos contratados. Não altera motores Sales, Operations, Strategy ou Forecast; melhorias nesses módulos são de interpretação e relatório, não novos modelos.
- Testes JavaScript e Chromium acrescentados. CI e homologação manual pendentes; 9/10 ainda não comprovada.
