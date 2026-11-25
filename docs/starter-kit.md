# Lilium Business Starter Kit

Development preview 0.14.0. All examples are synthetic, not benchmarks or advice.

| Scenario | Exercise focus |
|---|---|
| Comércio de bairro | Margens e mix de produtos |
| Prestação de serviços | Preço por serviço e capacidade |
| Pequena indústria | Custos variáveis e gargalos |
| Restaurante | Ticket médio e capacidade |
| Loja virtual | Mix e taxas de venda |

## Getting started
In Comece por aqui, select a scenario and one of the seven input sets or all of them. Confirm before replacing inputs. Run each module manually; nothing is saved automatically. Export a selected CSV (Insights, Sales, Operations, goals, actions, Forecast), Finance JSON, or full exercise JSON. The full exercise JSON is a reference bundle, not a Connect import package. Finance pricing form is separate from the monthly simulator and is not replaced.

## Suggested route
1. Analyze Insights and compare monthly margins.
2. Analyze Sales and compare products. There are three aggregate synthetic orders per month, not individual purchases; the ticket average is demonstrative only.
3. Compare Forecast baselines using the nine historical months January–September 2026. Revenue matches Sales and Insights in these examples.
4. Simulate Finance using its independent single-product assumptions.
5. Compare serial stages in Operations; evaluate Strategy goals and priorities.
6. Generate Reports or consult Copilot after the calculations. Review Flow suggestions manually.

Loading a model clears affected results, existing Reports and Copilot answers and the Flow evaluation table. Existing Flow proposals and saved Insights history are retained; they may refer to earlier inputs. Review scope and provenance before combining results. Other modules can still contain previous scenario data. Reloading returns to the built-in initial samples. No personal or real company data is needed.

47 scenario tests passed in V8, along with 12 static Workspace and 11 UX checks. Actual browser/Windows package validation remains pending.
