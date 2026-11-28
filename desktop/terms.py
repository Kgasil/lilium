"""Local version-bound terms acceptance; no account, telemetry or legal clearance."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
from datetime import datetime, timezone

TERMS = """PROJECT LILIUM — TERMOS DE USO GRATUITO / FREE-USE TERMS
Revisao 1 — minuta para homologacao / Revision 1 — review draft

Uso gratuito, sem conta ou assinatura obrigatoria. Estes termos nao restringem direitos concedidos pelas licencas de terceiros nem concedem redistribuicao de codigo ou artes proprios. Direitos legais obrigatorios preservados. Previa experimental; mantenha backups e protecoes do sistema ativas.
Exclusivamente para codigo redistribuivel Microsoft: preserve avisos de copyright, marcas e patentes; nao sugira autoria ou endosso Microsoft; nao distribua esse codigo para executar fora de sistemas operacionais, runtimes ou plataformas Microsoft; nao o inclua em programas maliciosos, enganosos ou ilicitos. Distribuidores e usuarios finais devem aceitar protecoes equivalentes as exigidas pela Microsoft para esse codigo.
O aceite e registrado somente neste dispositivo. Nenhum dado pessoal, identificador ou aceite e enviado. Excluir o aceite local exige nova confirmacao. A recusa encerra o aplicativo sem apagar dados.

Free use without mandatory account or subscription. These terms do not restrict third-party license rights or grant redistribution rights to first-party code or artwork. Mandatory legal rights remain unaffected. Experimental preview; keep backups and system protections active.
For Microsoft Distributable Code only: retain copyright, trademark and patent notices; do not imply Microsoft authorship or endorsement; do not distribute that code to run outside Microsoft operating systems, runtime technologies or application platforms; do not include it in malicious, deceptive or unlawful programs. Require equivalent protections from downstream distributors and external end users.
Acceptance is recorded only on this device. No personal data, identifier or acceptance is transmitted. Removing the local receipt requires confirmation again. Declining exits without deleting data.
"""
TERMS_BYTES = TERMS.encode("utf-8")
TERMS_SHA256 = hashlib.sha256(TERMS_BYTES).hexdigest()

def receipt_path(directory):
    return Path(directory) / "terms-acceptance.json"

def accepted(directory):
    try:
        path = receipt_path(directory)
        if path.is_symlink() or path.stat().st_size > 4096:
            return False
        row = json.loads(path.read_text(encoding="utf-8"))
        return (set(row) == {"schema", "terms_sha256", "accepted_utc"} and
                row["schema"] == 1 and row["terms_sha256"] == TERMS_SHA256 and
                isinstance(row["accepted_utc"], str) and
                datetime.fromisoformat(row["accepted_utc"]).utcoffset() == timezone.utc.utcoffset(None))
    except (OSError, ValueError, TypeError, KeyError):
        return False

def record(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = receipt_path(directory)
    if path.is_symlink():
        raise ValueError("Receipt must not be a link")
    row = {"schema": 1, "terms_sha256": TERMS_SHA256,
           "accepted_utc": datetime.now(timezone.utc).isoformat()}
    fd, tmp = tempfile.mkstemp(prefix=".terms-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(row, stream)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def forget(directory):
    receipt_path(directory).unlink(missing_ok=True)

def require_acceptance(directory, explicit=None, *, input_fn=input, output_fn=print):
    if explicit is not None:
        if explicit != TERMS_SHA256:
            return False
        record(directory)
        return True
    if accepted(directory):
        return True
    output_fn(TERMS)
    output_fn("SHA-256: " + TERMS_SHA256)
    try:
        choice = input_fn("Digite ACEITO ou I ACCEPT para continuar / type ACEITO or I ACCEPT: ")
    except (EOFError, KeyboardInterrupt):
        return False
    if choice.strip() not in {"ACEITO", "I ACCEPT"}:
        return False
    record(directory)
    return True
