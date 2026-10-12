# Changelog

## 1.0.1

- README install commands use the latest Skills CLI (`npx skills`). Pinning `@1.7.2` is documented as an option.
- User-facing install docs, after-install prompt, upgrade/remove, and compatibility notes for destination projects.
- Scan and usage helpers skip `.env` and credential-like names.
- Plugin description matches the skill's backend-or-application-logic scope.

## 1.0.0

- Installable Agent Skills package with a 48-pattern heuristic catalog, fourteen observation angles, and optional Python search (`--plan`, `--explore`).
- User README covers GitHub and local-clone install into a destination project, after-install prompt, upgrade, and remove. Skills CLI examples pin 1.7.2.
- `SKILL.md` routes catalog search to `17-structured-tooling.md`. Plugin and marketplace descriptions match the skill's backend-or-application-logic scope.
- Shell scan and usage search skip credential-like names (`.env`, `*.pem`, `secret`/`credential` paths) and fail when `timeout`/`gtimeout` is missing.
- CI validates package metadata, Markdown links, catalog schema, retrieval ranking, helper fixtures, and extracted ZIP behavior. Live install into every agent is outside that suite.
