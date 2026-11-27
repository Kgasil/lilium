# Matriz de homologação — Lilium
Aprovação exige nota ponderada >=9/10, evidência do commit e artefato exatos, nenhuma falha crítica ou alta sem tratamento. Critérios sem evidência não recebem nota; não calcular nota parcial como nota final. CI não equivale à homologação nativa.
| Critério | Peso | Evidência requerida | Estado |
|---|---:|---|---|
| Precisão matemática | 20% | regressões Python/JS, limites, paridade, revisão independente | CI candidata pendente |
| Funcionalidade e estabilidade | 20% | dez módulos, lifecycle, pacote extraído e Windows limpo | CI e aceite manual pendentes |
| Segurança e privacidade | 20% | dependências resolvidas, sessão, arquivos, adversarial, Ollama real, malware/assinatura avaliada | CI e revisão manual pendentes |
| UX e acessibilidade | 15% | teclado, labels, viewport, leitor de tela e contraste real | revisão manual pendente |
| Identidade visual | 10% | logo oficial, rosé escuro, inspeção visual multissuperfície | inspeção manual pendente |
| Desempenho | 10% | benchmark 10k, latência/recursos em hardware alvo | CI e medição manual pendentes |
| Documentação e integração | 5% | versões, hashes, links, instalação, handoff e limites | revisão final pendente |

Registre versão, commit, run, hash interno, ambiente, caso, esperado, observado, evidência, responsável e data. Os artefatos CI expiram; não os promover sem identificação exata. Teste Chrome e Edge instalados e Windows limpo, sem ignorar alertas; use dados fictícios. Não declarar segurança absoluta, certificação, ausência de malware, disponibilidade de modelo ou suporte de produção.
### Ollama real (manual)
Instale serviço confiável local e modelos permitidos de forma independente. Desconecte a rede depois de obter modelos; confira que serviço atende em loopback. Teste perguntas sintéticas claras, ambíguas, fora de domínio, tentativas de pedir valores inventados, falha/indisponibilidade e limpeza; anote tópico esperado/observado, duração, memória e ausência de chamadas externas. O modelo apenas roteia; a resposta financeira sempre vem do motor determinístico. Não envie dados reais. A aprovação requer resultados registrados, não apenas os testes mockados.
