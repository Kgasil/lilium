# Matriz de homologação de candidatos exatos / Exact candidate acceptance
Status: BLOCKED. No release authorization. Prior tests do not transfer to new bytes.

| Gate | Evidence required on exact candidate | Aeris | Lilium |
|---|---|---|---|
| Identity | commit, version, SHA-256, size, manifest, exact bytes | Pending | Pending |
| Provenance and licensing | native inventory, upstream hashes, REDIST entitlement, notices inside ZIP/setup, owner-reviewed terms | Pending | Pending |
| Defender | current definitions, each exact file fully scanned, zero skipped/detections | Pending | Pending |
| ClamAV | signed current definitions <=24h, full scans, zero skipped/detections | Blocked (46087821793) | Pending |
| Retention | independently reviewed scan/rights, restricted owner destination, hash verification | Draft workflow prepared; no candidate | Synthetic test only; no candidate |
| Windows acceptance | clean machine, install/portable, decline/reaccept, accessibility, uninstall/data preservation | Pending | Pending |
| Features | all 50 tools, local AI, voice, screen, meetings, privacy | Pending | N/A |
| Features | 10 modules, browser extension Chrome/Edge, Ollama, history, backup | N/A | Pending |
| Performance | measured startup, resource use, stability; no invented scores | Pending | Pending |
| Release | documented >=9/10 with no mandatory gate failures and explicit authorization | Blocked | Blocked |

Windows retention: read-only DACL checks require fixed local NTFS, no reparse points on destination path, owner SID, protected root DACL, full inheritable owner rights, only current user/SYSTEM/Administrators allow entries; children checked before final rename. Does not protect against privileged admins, compromised owner, parent ACL deletion, concurrent tampering or synced folders. Owner must choose non-synced private directory and independently review source scans/rights. No execution policy bypass. CI uses synthetic bytes only; no real artifacts retained. 
