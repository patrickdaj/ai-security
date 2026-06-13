# Module 20 — Cryptography & Data Security

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/patrickdaj/ai-security?quickstart=1)

> Opens a ready-to-build cloud environment (Python + scanners pre-installed). Build in `project/`; the worked answer is in `reference/`.

Phase: **Architecture, Identity, Crypto, Network.** Crypto fails in the *using*,
not the math: ECB mode, a hardcoded IV, MD5 for passwords, a static key, a cert
that expired Saturday. And data security is the discipline of knowing where
sensitive data is and keeping it encrypted, classified, and minimized. AI is
strong at spotting crypto misuse and reasoning about key/secret sprawl.

## Tools you tour

- **Cloud KMS / HSM** — managed keys, envelope encryption, rotation.
- **PKI** — `step-ca` / `cfssl`: issue, rotate, and revoke certificates.
- **HashiCorp Vault / SOPS / age** — secrets management and encryption at rest.
- **DLP & data classification** — find and label sensitive data; tokenization.

### Tour tasks

```bash
step-ca init && step ca certificate svc svc.crt svc.key   # stand up a CA, issue a cert
sops -e -i secrets.yaml                                    # encrypt a file with KMS/age
```

## AI augmentation: crypto-misuse scanner + key/data risk

Build a tool that scans code/config and returns crypto-misuse findings — each as
a normalized `Finding` with a [`Remediation`](../../aug/models.py) (the correct
construction + a diff). Extend it to reason over key/secret sprawl (who can
decrypt what, what hasn't rotated) and to assist data classification. See
[`project/`](./project) / [`reference/`](./reference). This sharpens the SAST
module (01) with crypto-specific judgment.

## Exercises

1. Scan a codebase for ECB/weak-hash/static-key/weak-RNG misuse; produce fixes.
2. Design envelope encryption for a data store and write the KMS key policy +
   rotation; have the model review the blast radius of the key.
3. Classify a sample dataset (PII/secret/public) and recommend controls per class.

## Done when

- You can find crypto misuse and produce correct fixes, design a key-management +
  rotation scheme, and reason about who can decrypt what — the data-protection
  story end to end.

## Resources

Curated entry points to learn the tools and concepts for this module — official docs and authoritative references. They get you grounded; the build is still yours.

- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST SP 800-57 (key management)](https://csrc.nist.gov/projects/key-management/key-management-guidelines)
- [HashiCorp Vault](https://developer.hashicorp.com/vault/docs) · [SOPS](https://github.com/getsops/sops) · [smallstep/step-ca](https://smallstep.com/docs/step-ca/)
- [OWASP ASVS — Cryptography (V6)](https://owasp.org/www-project-application-security-verification-standard/)
- [Cryptographic Right Answers (Latacora)](https://www.latacora.com/blog/2018/04/03/cryptographic-right-answers/)
