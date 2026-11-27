# Lilium — Etapa 02 / Experience
Data: 27/11/2026. Base: PR #2, 63183662e3bc04648909e6a4985906394fe46e0f. Mudanças em candidato separado; sem publicação.
## Design
- Paleta de tela alinhada ao site: fundo #30242F, painel #3D2E3A, texto #F0E1E8, destaque #E3B1C5. Tema escuro independente do sistema operacional. Impressão conserva estilos existentes.
- Visão executiva primeiro, quatro indicadores sem dados mostrados como traços, atalhos para importar, amostras e histórico. Resultados continuam usando o cálculo existente de Insights e o filtro de período. Sem consolidação de módulos de escopos diferentes.
- Navegação e 10 módulos mantidos; rótulo Strategy & Evolution. Logo SVG, ícones e cálculos existentes preservados.
- Mini 0.1.2 candidato visual: mesmos três cálculos, sem permissão nova. Verificador histórico de Mini 0.1.1 continua usando o commit público exato em checkout separado.
- Site, demonstração e privacidade: color-scheme escuro em tela; links públicos e versões distribuídas mantidos.
## Validação
Testes atualizados de navegação, estado vazio, tema computado e largura do popup. CI a confirmar. Revisão visual manual, contraste abrangente, leitor de tela, teclado, impressão e Windows/Chrome/Edge nativos continuam necessários. Não há nova aprovação de pacote, assinatura, Defender ou piloto. Sem contratação paga.
## Gate
Nota 9/10 não comprovada. Não promover novo Desktop/Mini ou alterar a distribuição até aceitar o novo candidato com hash próprio. PR #2 ainda requer conclusão de CI; este ramo incorpora as alterações daquela PR sem modificar main.
