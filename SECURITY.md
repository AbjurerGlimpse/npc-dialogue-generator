# Security Policy — npc-dialogue-generator

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.9.x   | Yes       |
| 0.8.x   | Yes       |
| < 0.8   | No        |

## Reporting a vulnerability

Email `security@npc-dialogue-generator.dev` or open a private security
advisory on GitHub. Do not file public issues for exploitable bugs.

Include: affected version, reproduction steps, and the impact you believe
it has. We aim to acknowledge within 72 hours and ship a patch within 14
days for high-severity issues.

## Threat model

`npc-dialogue-generator` runs as a desktop utility that loads user-supplied
`.npcpack` files. The attack surface is:

1. **Pack deserialization** — YAML and JSON parsers. We use `ruamel.yaml`
   in safe mode and `json` with a size cap. Malicious packs must not be
   able to execute code, escape the pack directory, or write outside the
   project cache.
2. **Model weight loading** — `.gguf` and `.onnx` files provided by the
   user. We do not bundle weights. Weight files are opened read-only and
   memory-mapped; parsers are hardened against size and offset overruns.
3. **Plugin hooks** — the exporter plugin API is intentionally not a
   sandbox. Plugins run with full user privileges. Only load plugins from
   sources you trust.
4. **Exporters** — generated runtime code is written to the pack's
   `export/` subdirectory. Path traversal in exporter templates is
   rejected.

## Out of scope

- Denial of service from absurdly large packs on the authoring machine
  (that is the author's own machine and their own pack).
- Anything requiring the attacker to already have code execution as the
  user.

## Hardening notes for pack authors

If you publish a pack, pin the `npcpack_version` field. Consumers of your
pack that run an older loader will get a clear version-mismatch error
instead of a partially-parsed tree.