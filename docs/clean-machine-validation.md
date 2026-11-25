# Lilium — roteiro de aceitação em Windows limpo

**Escopo:** prévia 0.14.0, piloto gratuito com dados fictícios. Este documento é um roteiro de execução, não um certificado ou um resultado de teste. Execute somente depois que um workflow Windows tiver concluído com sucesso e disponibilizado o artefato completo.

## 1. Evidência do pacote

- [ ] Registrar URL e commit do workflow Windows bem-sucedido, versão e SHA-256 do ZIP interno.
- [ ] Baixar o artefato a partir da execução bem-sucedida, extrair o ZIP externo e conferir o hash do ZIP interno com `Get-FileHash -Algorithm SHA256` e o valor da execução confiável.
- [ ] Extrair em pasta nova, mantendo todos os arquivos de `_internal` junto ao executável. Não sobrepor instalação anterior.
- [ ] Usar uma conta Windows comum, sistema atualizado, navegador compatível e máquina sem Python instalado para validar o pacote portátil. Não ignorar alertas do sistema, desativar antivírus ou executar como administrador para contornar erros. O pacote não é assinado; registrar o bloqueio caso haja.
- [ ] Executar `Lilium.exe --diagnostics` em um terminal; verificar os seis resultados. Não compartilhar links de acesso privados, tokens ou caminhos pessoais.

## 2. Primeiro uso

- [ ] Executar Lilium.exe; confirmar abertura do navegador e serviço em 127.0.0.1.
- [ ] Abrir Comece por aqui e carregar cenário fictício do Starter Kit.
- [ ] Executar Insights, Finance, Sales, Operations, Strategy, Forecast, Flow, Connect, Copilot e Reports; conferir as entradas e os resultados com os respectivos escopos.
- [ ] Testar arquivos inválidos (CSV com cabeçalho errado, XLSX com fórmula), conferir mensagem e ausência de resultados antigos.
- [ ] Testar download CSV/JSON/TXT, imprimir um relatório sintético e salvar como PDF pelo navegador. Conferir visualmente a impressão.
- [ ] Confirmar navegação por Tab, Shift+Tab, Enter, foco visível e contraste; testar largura de 390 px e, se disponível, leitor de tela. Registrar barreiras, não declarar conformidade WCAG.

## 3. Persistência, recuperação e encerramento

- [ ] Salvar uma análise sintética, exportar backup e encerrar com Ctrl+C.
- [ ] Reiniciar; verificar análise salva e rejeição de acesso com token anterior. Não divulgar os links.
- [ ] Excluir apenas a análise sintética de teste; recuperar backup, importar novamente e confirmar ausência de duplicatas.
- [ ] Encerrar e abrir novamente; verificar que a análise recuperada permanece.
- [ ] Testar preparação de nova pasta da mesma versão para simular atualização, sem sobrescrever a anterior. Conferir a documentação de compatibilidade; isso não testa migração de banco entre versões diferentes.

## 4. Segurança e aprovação

- [ ] Revisar dependências diretas e transitivas do ambiente de build com base em vulnerabilidades conhecidas; documentar versões, data, ferramenta e resultado. Avaliar achados em contexto, sem ignorar vulnerabilidades.
- [ ] Confirmar que nenhuma entrada do negócio é enviada a serviços externos e que os limites descritos em [Trust & Privacy](trust-privacy.md) estão compreensíveis.
- [ ] Registrar falhas e evidências, corrigir bloqueios, reexecutar os cenários relevantes e identificar o pacote exato aprovado.
- [ ] Confirmar canal de feedback e instruções de privacidade; liberar apenas um piloto controlado com dados fictícios. Uso de dados reais exige avaliação separada.

## Registro de execução (preencher)

| Campo | Valor |
|---|---|
| Data | Pendente |
| Versão do Windows e arquitetura | Pendente |
| URL da execução Windows | Pendente |
| Commit e SHA-256 do ZIP | Pendente |
| Máquina sem Python | Pendente |
| Cenários aprovados / reprovados | Pendente |
| Falhas bloqueantes | Pendente |
| Decisão de liberação | Não aprovada até a evidência |

Use a central de ajuda para gerar um relato sem dados confidenciais. Não inclua token de sessão, planilhas reais, dados pessoais ou caminhos privados.
