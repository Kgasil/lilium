# Lilium Mini v0.1.1 — extensão experimental

**Strategy & Evolution · Estratégia e Evolução**  
*Make smarter decisions. Grow with confidence.*

> Distribuição experimental exclusivamente pelo GitHub. A extensão é gratuita, não está publicada na Chrome Web Store nem no Microsoft Edge Add-ons e não requer conta ou pagamento. A instalação manual destina-se a testes com dados fictícios; não é uma certificação de segurança.

**Marco 1.0 do Project Lilium:** corresponde ao [Web Lab público](https://kgasil.github.io/lilium/#lab), não à extensão Mini, que permanece v0.1.1. [Visão geral](../README.md).

## Como instalar no Chrome ou Edge (Windows)

### 1. Baixar e extrair
- [**Baixar o código da versão v0.1.1 (ZIP)**](https://github.com/Kgasil/lilium/archive/447d7414f20e28f6c0440647f2b7be71fc44e71d.zip). Este link aponta para o commit de referência e baixa o repositório completo, incluindo a pasta `extension`.
- No Explorador de Arquivos, clique com o botão direito no ZIP e selecione **Extrair Tudo**.
- Abra a pasta extraída e localize a subpasta `extension`. Confirme que ela contém `manifest.json`, `icon128.png`, `popup.html`, `popup.css`, `popup.js` e `math.js`. Não selecione a raiz do repositório nem execute arquivos do Desktop.

### 2. Abrir o gerenciador de extensões
- Chrome: digite `chrome://extensions` na barra de endereços.
- Edge: digite `edge://extensions` na barra de endereços.
- Ative **Modo do desenvolvedor**, se permitido pelas políticas do seu navegador. Não contorne restrições administrativas ou alertas de segurança.
- Clique em **Carregar sem compactação** (Load unpacked) e selecione a subpasta `extension` que contém o manifesto.

### 3. Abrir e usar
No menu de extensões (ícone de quebra-cabeça), localize **Lilium Mini** e, se desejar, fixe-o na barra de ferramentas. Abra a extensão, escolha uma ferramenta, preencha os valores e clique em **Calcular**.

| Ferramenta | Exemplo fictício | Resultado esperado |
|---|---|---|
| Resultado e margem | Receita R$ 1.000; custos R$ 700 | Resultado R$ 300; margem 30% |
| Formação de preço | Custo R$ 60; margem desejada 40% | Preço mínimo R$ 100 |
| Ponto de equilíbrio | Fixos R$ 1.000; preço R$ 100; variável R$ 60 | 25 unidades |

Os cálculos não equivalem necessariamente ao lucro contábil; leia as premissas na interface. A extensão não importa planilhas, não salva histórico e não acessa os sites visitados.

### 4. Atualizar ou desinstalar
Para atualizar, obtenha uma versão identificada no GitHub, extraia-a em uma pasta permanente, revise o manifesto e carregue a nova pasta após remover a versão anterior. Para desinstalar, abra o gerenciador de extensões e clique em **Remover** no Lilium Mini. O navegador não atualiza automaticamente uma extensão carregada sem compactação. Não exclua a pasta enquanto a extensão estiver instalada.

### 5. Solução de problemas
Se aparecer erro de manifesto ausente, confira se selecionou a pasta `extension` extraída. Se o navegador bloquear a instalação, respeite a política e não prossiga. Se houver erro nos cálculos, registre versão, navegador, valores fictícios, resultado esperado e observado em [GitHub Issues](https://github.com/Kgasil/lilium/issues/new); o canal é público, portanto não inclua dados reais ou detalhes de exploração de vulnerabilidades.

[Política de privacidade](https://kgasil.github.io/lilium/mini-privacy.html) · [Web Lab 1.0](https://kgasil.github.io/lilium/#lab)

## English — manual installation
Download the [pinned source ZIP](https://github.com/Kgasil/lilium/archive/447d7414f20e28f6c0440647f2b7be71fc44e71d.zip), extract it, open `chrome://extensions` or `edge://extensions`, enable Developer mode if permitted, and select **Load unpacked** with the extracted `extension` folder. Pin the toolbar icon if desired. Use synthetic data only and respect browser or organization warnings. Remove it via the extensions manager; updates are manual. No store publication or production security claim.

Three local tools: result and margin, target-margin pricing, break-even quantity. Monetary values use BRL and up to two decimal places. No required browser permissions, background scripts, content scripts, storage, analytics, or remote AI. The explicit Insights link opens the public website in a new tab without passing calculation values. Run `node extension/math.test.js` from the repository root. The owner reported testing v0.1.0; detailed case results and installed v0.1.1 acceptance remain unconfirmed.

## Experimental ZIP / Pacote experimental

The dedicated [Mini validation workflow](https://github.com/Kgasil/lilium/actions/workflows/mini-validation.yml) is configured to run the calculation and popup-page regression checks, build the minimal ZIP twice, compare both builds and upload the archive and SHA-256 as an Actions artifact only after success. The latest workflow outcome must be checked before using its artifact. It is not a store release.

To build locally from a trusted checkout, run `python extension/package_mini.py --output mini-preview` with Python 3.12 or newer. The v0.1.1 archive contains only icon128.png, manifest.json, math.js, popup.css, popup.html and popup.js; it excludes development scripts and tests. Extract the ZIP, compare its SHA-256 with the generated digest from a trusted build, and select the extracted folder containing manifest.json in the browser's unpacked-extension tester. Do not bypass organization policy or security warnings. Archive checks and popup-page regression are not actual installed-extension acceptance. Chrome/Edge toolbar installation and store review remain separate gates.

## Local packaging evidence — 25/11/2026 (Brazil time)

Two local builds of the experimental v0.1.0 ZIP using Python 3.13.5 and the published packager (Git blob d9a3bf1ee04e0d1f2839591cd9bf20ff7e18d93e) produced identical 3,952-byte files. All five runtime blobs matched GitHub; ZIP CRC and byte-for-byte entry comparison passed. SHA-256: `24a44cb18c0774745deac414bc319173e8cab48996ff73dd3f08d82897083e15`. This digest describes the local build, not necessarily the Actions artifact (compression versions may differ). The local Chromium environment denied access to the installed-extension URL and loopback popup page; neither browser test passed or failed on application behavior. Store review and installed Chrome/Edge acceptance remain open, as does verification of the latest Actions workflow. No feature or version change.

## Historical store preparation — v0.1.1
The owner reported testing the v0.1.0 extension; case-by-case evidence is not recorded. Version 0.1.1 adds a 128px branded PNG icon and updates the displayed version, with unchanged calculator code and no new permissions. It was prepared for future store submission; distribution is now GitHub-only at the owner's direction. No store listing or submission has been made. Re-test the final ZIP as an installed extension before submission. Local Chromium navigation was blocked by environment policy; capture real screenshots on the owner's device. [Privacy policy](https://kgasil.github.io/lilium/mini-privacy.html) (confirm public deployment before submission). [Developer dashboard](https://chrome.google.com/webstore/devconsole/). Any future store submission is the owner's responsibility. No store listing URL exists yet. The local candidate ZIP SHA-256 is `b72dc762b7d9341bb4337ceff462a1d6441ab8bfff98ec2ad045dcdd22f7f797`; this is not an Actions artifact digest.
