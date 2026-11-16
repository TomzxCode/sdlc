---
artifact: specification.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: specification.md

## Sync drift: 2026-11-16

- Architecture diagram (specification.md:10-17) shows per-locale directories `en/`, `es/`, `zh-CN/`, `<locale>/`. The code uses flat per-language files `locales/<lang>.yaml` with optional surface variants `<lang>.tui.yaml` / `<lang>.desktop.yaml` and key manifests `_keys.tui.json` / `_keys.desktop.json`. There are no locale subdirectories, and Chinese is split as `zh` (Simplified) plus `zh-hant` (Traditional), not `zh-CN`.
- Technical decision "Storage | Directory-based locale files" (specification.md:32) is wrong: catalogs are flat YAML files resolved through four layers (plugin packs > profile overlay `<home>/locales/<lang>.yaml` > bundled `locales/<lang>.yaml` > English), with one merged dict cached per `(home, lang)` (`agent/i18n.py:3-9,154-199`).
- Technical decision "CLI locale detection | System locale or config setting" (specification.md:34) is wrong: resolution is `HERMES_LANGUAGE` env > `display.language` config > `en` (`agent/i18n.py:11-12,232-245`); there is no system-locale detection.
- The architecture lists only English, Spanish and Simplified Chinese. The implementation bundles 17 languages (`en, zh, zh-hant, ja, de, es, fr, tr, uk, af, ko, it, ga, pt, ru, hu, ar`; `agent/i18n.py:33-36`) plus alias tags and any overlay/pack-supplied language (`agent/i18n.py:43-64,95-107`).
- The "Locale file format" table (specification.md:21-26) describes literal dotted keys. The files are nested YAML mappings that are flattened into dotted keys at load time (`locales/en.yaml`, `agent/i18n_layers.py:51,73`).
