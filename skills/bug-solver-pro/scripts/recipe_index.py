"""Validated per-language/framework retrieval indexes; Markdown owns the working knowledge."""

from pathlib import Path
import re

from core import DOMAINS, SKILL_ROOT, load_json, search, validate_references

RECIPE_FIELDS = {"id", "domain", "keywords", "references", "heading", "evidence_kind"}
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"


def markdown_structure(path):
    """Return ATX headings outside fenced examples; authored recipe headings are unindented."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    headings = []
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not marker.group(2).strip():
                fence = None
            continue
        if fence is None and re.match(r"^#{1,6} ", line):
            headings.append((index, line.rstrip(), len(line) - len(line.lstrip("#"))))
    return lines, headings


def read_section(path, heading):
    """Read an exact, unambiguous Markdown section, ignoring headings inside code fences."""
    lines, headings = markdown_structure(path)
    matches = [(index, depth) for index, text, depth in headings if text == heading]
    if len(matches) != 1:
        raise ValueError(f"Missing or ambiguous recipe heading in {path.name}: {heading}")
    start, depth = matches[0]
    end = next((index for index, _, level in headings if index > start and level <= depth), len(lines))
    if not "".join(lines[start + 1:end]).strip():
        raise ValueError(f"Empty recipe section in {path.name}: {heading}")
    return "".join(lines[start:end]).strip()


def validate_recipe_index(data, root=SKILL_ROOT):
    if not isinstance(data, dict) or set(data) != {"schema_version", "language", "framework", "recipes"}:
        raise ValueError("Recipe index must contain schema_version, language, framework and recipes")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Unsupported recipe index schema_version")
    for key in ("language", "framework"):
        if not isinstance(data[key], str) or not re.fullmatch(SLUG, data[key]):
            raise ValueError(f"Invalid recipe index {key}")
    if not isinstance(data["recipes"], list) or not data["recipes"]:
        raise ValueError("recipes must be a nonempty list")
    owner = f"references/languages/{data['language']}/frameworks/{data['framework']}"
    seen = set()
    targets = set()
    rows = []
    for row in data["recipes"]:
        if not isinstance(row, dict) or set(row) != RECIPE_FIELDS:
            raise ValueError("Each recipe must contain every index field")
        for key in RECIPE_FIELDS - {"references"}:
            if not isinstance(row[key], str) or not row[key].strip():
                raise ValueError(f"Recipe {key} must be a nonempty string")
        identity = row["id"]
        if not re.fullmatch(SLUG, identity) or identity in seen:
            raise ValueError(f"Invalid or duplicate recipe id: {identity}")
        seen.add(identity)
        if row["domain"] not in DOMAINS or row["evidence_kind"] != "heuristic":
            raise ValueError(f"{identity}: invalid domain or evidence_kind")
        if not re.fullmatch(r"#{1,6} [^\r\n]+", row["heading"]):
            raise ValueError(f"{identity}: invalid heading")
        validate_references(row["references"], identity, root)
        if len(row["references"]) != 1 or row["references"][0] not in (
                f"{owner}/playbook.md", f"{owner}/boundary-case.md"):
            raise ValueError(f"{identity}: recipe must point to its owning framework's playbook or boundary case")
        target = (row["references"][0], row["heading"])
        if target in targets:
            raise ValueError(f"{identity}: duplicate recipe section")
        targets.add(target)
        content = read_section(root / target[0], target[1])
        title = re.sub(r"^#{1,6}\s+(?:[0-9]+\.\s+)?", "", row["heading"])
        rows.append({**row, "language": data["language"], "framework": data["framework"],
                     "title": title, "content": content})
    playbook = f"{owner}/playbook.md"
    _, headings = markdown_structure(root / playbook)
    expected = {(playbook, heading) for _, heading, depth in headings
                if depth == 2 and re.match(r"^## [0-9]+\. ", heading)}
    boundary = f"{owner}/boundary-case.md"
    if (root / boundary).is_file():
        _, headings = markdown_structure(root / boundary)
        titles = [heading for _, heading, depth in headings if depth == 1]
        if len(titles) != 1:
            raise ValueError(f"{boundary}: expected exactly one case title")
        expected.add((boundary, titles[0]))
    if targets != expected:
        raise ValueError(f"{data['framework']}: every numbered recipe and boundary case must be indexed exactly once")
    return rows


def load_recipe_catalog(root=SKILL_ROOT):
    root = Path(root)
    paths = sorted((root / "data/frameworks").glob("*/*/recipes.json"))
    if not paths:
        raise ValueError("No framework recipe indexes found")
    rows = []
    owners = set()
    for path in paths:
        data = load_json(path)
        current = validate_recipe_index(data, root)
        owner = (data["language"], data["framework"])
        if owner != (path.parent.parent.name, path.parent.name):
            raise ValueError(f"Recipe index owner differs from its path: {path}")
        owners.add(owner)
        rows.extend(current)
    expected = {(path.parent.parent.parent.name, path.parent.name)
                for path in (root / "references/languages").glob("*/frameworks/*/guide.md")}
    if owners != expected:
        raise ValueError("Framework recipe indexes and module directories must cover the same owners")
    if len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Recipe ids must be unique across framework indexes")
    return rows


def search_recipes(query, framework=None, domain=None, limit=3, root=SKILL_ROOT):
    rows = load_recipe_catalog(root)
    if framework is not None and not any(row["framework"] == framework for row in rows):
        raise ValueError(f"No recipe data for framework: {framework}")
    # Keep term rarity stable; filter before taking the result limit.
    result = search(query, domain, limit, patterns=rows, framework=framework)
    result["catalog"] = "data/frameworks/<language>/<framework>/recipes.json"
    result["framework"] = framework or "all"
    result["instruction"] = "Recipe matches are local lexical leads, not verified applicability or plan hypotheses. Read prerequisites and validate the probe."
    return result
