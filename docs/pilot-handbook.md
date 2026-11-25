# Lilium — piloto gratuito controlado

**Estado: preparado, ainda não aberto.** A versão de referência é a prévia portátil 0.14.0 corrigida. Não há lançamento comercial ou promessa de suporte contínuo.

## Objetivo e escopo
Avaliar se o Lilium ajuda pequenos empreendedores a compreender indicadores, simular decisões e preparar relatórios. A primeira rodada será restrita a dados inteiramente fictícios. Os participantes não devem importar registros reais de clientes, vendas, folha, estoque ou finanças.

## Antes do convite
O responsável pelo projeto deve registrar o resultado da [aceitação em computador Windows limpo](clean-machine-validation.md), incluindo o hash do ZIP testado, diagnóstico, navegação, impressão, backup e revisão de segurança. A [matriz de liberação](pilot-readiness.md) deve ser aprovada. A revisão de dependências não equivale a uma auditoria independente da aplicação, das bibliotecas nativas ou do sistema operacional. Caso existam bloqueios, não iniciar o piloto.

## Roteiro sugerido para o participante
1. Ler as limitações e abrir a prévia portátil somente após conferir o SHA-256 e o diagnóstico. Não ignorar alertas do Windows.
2. Em **Comece por aqui**, selecionar um cenário fictício do Business Starter Kit.
3. Calcular receitas e custos em Insights e responder: qual mês teve maior resultado? O que a margem representa?
4. Simular a formação de preços e o ponto de equilíbrio em Finance; conferir as hipóteses.
5. Em Sales e Operations, comparar produtos e etapas; tratar os pedidos agregados como exercícios, não transações reais.
6. Em Strategy e Forecast, comparar metas e projeções; revisar os limites de cada cálculo.
7. Gerar um relatório, testar exportação e consultar o Copilot guiado. O assistente não usa IA externa.
8. Avaliar uma regra em Flow, revisar a proposta e testar normalização de um CSV fictício em Connect. Não há execução externa automática.
9. Salvar uma análise, exportar backup, reiniciar, confirmar persistência e experimentar recuperação. Ao terminar, fechar o processo Desktop.

## Feedback e critérios de decisão
Use o modelo da central de ajuda ou [GitHub Issues](https://github.com/Kgasil/lilium/issues/new/choose), que é público. Informe versão, sistema, módulo, reprodução sintética, resultado esperado/observado e gravidade. Não envie tokens, links privados, dados pessoais ou empresariais, caminhos locais ou detalhes de exploração de vulnerabilidades.

Avaliar: facilidade de inicialização, compreensão dos indicadores, utilidade das simulações, clareza de erros, navegação por teclado, confiabilidade dos arquivos exportados e persistência.

- **Bloqueante:** falha de segurança, perda/corrupção de dados de teste, resultado financeiro incorreto, impossibilidade de abrir ou recuperar dados. Suspender a distribuição até corrigir e revalidar.
- **Importante:** funcionalidade principal indisponível ou barreira grave de usabilidade. Registrar e resolver antes de expandir o grupo.
- **Menor/sugestão:** melhoria que não compromete o uso planejado. Registrar para avaliação posterior.

## Limitações e privacidade
Desktop usa acesso temporário por sessão e armazenamento local sem criptografia do aplicativo. Não é sistema contábil, ERP, CRM integrado, recomendação financeira ou serviço de IA conectado. Não há telemetria no Workspace, contas, sincronização ou execução automática de propostas. O pacote não é assinado. O piloto não autoriza dados reais. Consulte [Trust & Privacy](trust-privacy.md).

## Registro de abertura (a preencher pelo responsável)
- Candidato aprovado e hash:
- Data e evidência de aceitação manual:
- Resultado da revisão de segurança e acessibilidade:
- Bloqueios remanescentes:
- Grupo autorizado e canal de feedback (sem publicar dados pessoais):
- Decisão: **pendente**.

Nenhum participante foi convidado por este documento. Não publicar V1.0 nem alterar o status até a decisão registrada.
