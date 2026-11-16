---
artifact: requirements.md
verdict: changes-requested
reviewed_at: 2026-11-16
---

# Review: requirements.md

## Sync drift: 2026-11-16

- FR-2 ("CLI output shall respect the system locale setting", requirements.md:24) is not implemented. Language resolution in `agent/i18n.py:11-12,232-245` is explicit `lang=` > `HERMES_LANGUAGE` env > `display.language` config > `en`. There is no OS/system-locale auto-detection, so CLI output does not follow the system locale.
- NFR-1 ("Adding a new locale shall require only a new translation file, no code changes", requirements.md:31) holds only for profile overlay files and plugin language packs. Bundled locales must also have their id added to the hardcoded `SUPPORTED_LANGUAGES` tuple in `agent/i18n.py:33-36`, because `supported_languages()` builds the accepted set from that tuple plus overlay/pack layers only (`agent/i18n_layers.py:264-266`). Dropping a new `locales/<lang>.yaml` alone is not enough for `hermes config set display.language <lang>` to accept it.
