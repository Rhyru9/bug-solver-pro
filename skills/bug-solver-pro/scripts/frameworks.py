"""Load local framework working knowledge without inferring a cause or using a network."""

import re

from core import SKILL_ROOT, validate_references


ALIASES = {
    "next-js": "nextjs", "nest-js": "nest", "nestjs": "nest",
    "react-js": "react", "reactjs": "react", "vue-js": "vue", "vuejs": "vue",
    "svelte-kit": "sveltekit", "spring-boot": "spring",
    "asp-net-core": "aspnet-core", "aspnetcore": "aspnet-core",
    "actix": "actix-web", "actixweb": "actix-web",
    "ruby-on-rails": "rails", "gin-gonic": "gin",
}


def framework_context(name, root=SKILL_ROOT):
    """Resolve a declared framework to bundled guides, independently of symptom ranking."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Framework name must be a nonempty string")
    slug = re.sub(r"[\s._]+", "-", name.strip().lower())
    guides = sorted((root / "references/languages").glob("*/frameworks/*/guide.md"))
    canonical_names = {path.parent.name for path in guides}
    if slug not in canonical_names:
        slug = ALIASES.get(slug, slug)
    matches = [path.parent for path in guides if path.parent.name == slug]
    if not matches:
        available = ", ".join(sorted(canonical_names))
        raise ValueError(f"Unknown framework: {name}. Available: {available}")
    if len(matches) != 1:
        raise ValueError(f"Ambiguous framework module: {name}")
    module = matches[0]
    resources = {kind: (module / f"{kind}.md").relative_to(root).as_posix()
                 for kind in ("playbook", "guide", "docs")}
    boundary_case = module / "boundary-case.md"
    if boundary_case.is_file():
        resources["boundary-case"] = boundary_case.relative_to(root).as_posix()
    validate_references(list(resources.values()), slug, root)
    return {
        "framework": slug,
        "language": module.parent.parent.name,
        "evidence_kind": "heuristic",
        "resources": resources,
        "playbook": (root / resources["playbook"]).read_text(encoding="utf-8"),
        "boundary_case": boundary_case.read_text(encoding="utf-8") if boundary_case.is_file() else None,
        "instruction": (
            "Framework selected explicitly; this is local working knowledge, not a symptom match "
            "or a verified diagnosis. Check recipe prerequisites and probe sensitivity. "
            "Unsupported or untriggered probes are inconclusive, not falsifiers."
        ),
    }
