# Changelog

## 1.1.0

- Add eight language groups and 22 framework/library modules with 66 debugging recipes, 22 deeper boundary cases, and direct official documentation maps.
- Make all 88 techniques searchable through per-language/framework data indexes. Add `--framework`, local source excerpts, and separate `framework_matches` output while preserving existing shared-result fields and flags.
- Expand the shared catalog from 48 to 54 heuristic patterns and exploration from 14 to 20 angles, covering data/query semantics, stale cache refills, lease fencing, retry multiplication, and probe validity.
- Add causal decision gates, composed-failure guidance, and tracked coverage/data audits with explicit evidence limits.
- Reject duplicate JSON keys, stale or cross-framework routes, and missing recipe indexes. Test retrieval, corruption handling, copied installations, and extracted ZIPs; add bounded SQL and optional FastAPI runtime probes.
- Rewrite the README around the investigation workflow, practical examples, installation, and upgrades. Bump the plugin version so existing marketplace installations can receive the new package.

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
