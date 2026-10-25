"""Gemini用CAの指紋・TLS検証をPC上のOpenSSLで検査する（APIキー不要）。
実機のTLSスタックや音声対話の確認を代替するものではない。
"""
import hashlib
import os
from pathlib import Path
import re
import shutil
import ssl
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "D947432ABDE7B7FA90FC2E6B59101B1280E0E1C7E4E40FA3C6887FFF57A7F4CF",
    "8D25CD97229DBF70356BDA4EB3CC734031E24CF00FAFCFD32DC76EB5841C7EA8",
    "34D8A73EE208D9BCDB0D956520934B4E40E69482596E8B6F73C8426B010A6F48",
    "349DFA4058C5E263123B398AE795573C4E1313C83FE68F93556CD5E8031B3C7D",
]
PATTERN = r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----"


def main():
    openssl = shutil.which("openssl")
    if not openssl:
        candidate = Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/usr/bin/openssl.exe"
        if candidate.is_file():
            openssl = str(candidate)
    if not openssl:
        raise RuntimeError("OpenSSL not found. Install Git for Windows or set PATH.")

    def run(args, expected_error=None):
        result = subprocess.run([openssl, *map(str, args)], input="", capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=30)
        output = result.stdout + result.stderr
        if expected_error is None:
            if result.returncode != 0:
                raise RuntimeError(output)
        elif result.returncode == 0 or not re.search(rf"error {expected_error} at", output):
            raise RuntimeError(f"Expected certificate verification error {expected_error}:\n{output}")
        return output

    header = (ROOT / "firmware/src/rootCA/rootCAgoogleGemini.h").read_text(encoding="utf-8")
    certs = re.findall(PATTERN, header, re.S)
    hashes = [hashlib.sha256(ssl.PEM_cert_to_DER_cert(cert)).hexdigest().upper() for cert in certs]
    if hashes != EXPECTED:
        raise RuntimeError("Embedded CA fingerprint mismatch")
    print("PASS: four embedded roots match official GTS fingerprints")

    with tempfile.TemporaryDirectory(prefix="gemini-tls-") as temp:
        folder = Path(temp)
        bundle = folder / "roots.pem"
        bundle.write_text("\n".join(certs) + "\n", encoding="ascii")
        for index, cert in enumerate(certs, 1):
            root = folder / f"root{index}.pem"
            root.write_text(cert + "\n", encoding="ascii")
            run(["verify", "-check_ss_sig", "-CAfile", root, root])
        print("PASS: all four root self-signatures and validity periods")

        host = "generativelanguage.googleapis.com"
        output = run(["s_client", "-connect", f"{host}:443", "-servername", host,
                      "-showcerts", "-verify_return_error", "-verify_hostname", host,
                      "-CAfile", bundle, "-no-CApath", "-no-CAstore"])
        chain = re.findall(PATTERN, output, re.S)
        if len(chain) < 2:
            raise RuntimeError("Google did not supply the expected certificate chain")
        print("PASS: live Google TLS handshake with embedded roots (no API key sent)")
        leaf = folder / "leaf.pem"
        intermediate = folder / "intermediates.pem"
        leaf.write_text(chain[0] + "\n", encoding="ascii")
        intermediate.write_text("\n".join(chain[1:]) + "\n", encoding="ascii")
        verify = ["verify", "-CAfile", bundle, "-no-CApath", "-no-CAstore", "-untrusted", intermediate]
        run([*verify, "-verify_hostname", host, leaf])
        run([*verify, "-verify_hostname", "invalid.example", leaf], expected_error=62)
        print("PASS: wrong hostname rejected")
        run([*verify, "-attime", "0", leaf], expected_error=9)
        print("PASS: unset clock (1970) rejected")
        run([*verify, "-attime", "2208988800", leaf], expected_error=10)
        print("PASS: expired chain (2040) rejected")

        fake = folder / "untrusted.pem"
        run(["req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
             "-subj", f"/CN={host}", "-addext", f"subjectAltName=DNS:{host}",
             "-keyout", folder / "temporary-test.key", "-out", fake])
        run(["verify", "-CAfile", bundle, "-no-CApath", "-no-CAstore", fake], expected_error=18)
        print("PASS: untrusted self-signed certificate rejected")
    print("PC checks complete. Device TLS / audio / reconnect checks still required.")


if __name__ == "__main__":
    main()
