# Lilium — direitos de distribuição / Distribution rights
27 Nov 2026 BRT. REVIEW_REQUIRED — no release or legal clearance.

Historical run 46076360257, artifact 15235636135 SHA-256 4209ddbeda6b84ed2a8264c2a1d925ee2a3c6cb5e8d1801acd94e18f4580f357 CRC PASS; four DLL pairs match in source.json/bundle.json. Actual candidate ZIP not retained. Notice fix cce671b / 46088584888 SUCCESS, not final package evidence.

- CPython 3.14.10: PSF license plus exact Windows CRT conditions https://github.com/python/cpython/blob/v3.14.10/PC/crtlicense.txt . Preserve installed license, exact notices. Conditional redistribution of Windows Python interpreter, not blanket rights for separately sourced Microsoft DLLs.
- OpenSSL 3.5.9: Apache-2.0; libcrypto-3.dll and libssl-3.dll hash pairs match. Preserve license, applicable NOTICE/attribution and modification notices. https://www.openssl-library.org/source/license/
- SQLite 3.50.4: sqlite3.dll hash pair matches; core public domain https://www.sqlite.org/copyright.html . Confirm extension scope and provenance.
- libffi 3.4.4 and XZ 5.2.5: official CPython build references https://github.com/python/cpython/blob/v3.14.10/PCbuild/get_externals.bat , not measured Lilium binary versions. libffi permissive license retained. _lzma.vcxproj and liblzma.vcxproj show static liblzma, not command-line tools. XZ COPYING distinguishes public-domain library from LGPL getopt and GPL scripts. Preserve exact XZ and LGPL reference texts; determine actual linked code/obligations, not blanket LGPL.
- PyInstaller 6.16.0: existing exact COPYING.txt, generated executable exception subject to dependencies. No first-party license assigned.
- MSVC/UCRT: current evidence only covers four DLLs, not CRT inventory; older candidate versions not transferable. Confirm provenance, versions, hashes, applicable entitlement/REDIST and downstream protections https://learn.microsoft.com/cpp/windows/redistributing-visual-cpp-files . Inno Setup not evidenced for Lilium portable ZIP.

## Minuta de termos / Draft terms — owner review required
Uso gratuito, sem assinatura obrigatória. Não restringe direitos das licenças de terceiros, nem concede redistribuição de código/artes próprios. Direitos legais obrigatórios preservados. / Intended for free use without mandatory subscription. No restriction on third-party license rights or grant to redistribute first-party code/art. Mandatory legal rights preserved.

Exclusivamente para código redistribuível Microsoft: preservar avisos de copyright, marcas e patentes; não sugerir autoria/endosso Microsoft; não distribuir esse código para executar fora de sistemas operacionais, runtimes ou plataformas Microsoft; não incluir em programas maliciosos, enganosos ou ilícitos. Distribuidores e usuários finais devem aceitar proteções equivalentes às exigidas pela Microsoft para esse código. / For Microsoft Distributable Code only: retain copyright, trademark and patent notices; do not imply Microsoft authorship or endorsement; do not distribute that code to run outside Microsoft operating systems, runtimes or application platforms; do not include in malicious, deceptive or unlawful programs. Require equivalent protections from downstream distributors and end users.

Draft does not confer entitlement. Owner review, acceptance mechanism, exact inventory, final package inclusion and AV/acceptance gates remain mandatory. No new cost, release, runtime change, or main update.
