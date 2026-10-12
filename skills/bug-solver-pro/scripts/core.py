"""Local diagnostic catalog and lexical retrieval; Python standard library only."""

from collections import Counter
import json
import math
from pathlib import Path
import re

SKILL_ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = SKILL_ROOT / "data" / "patterns.json"
ANGLES_PATH = SKILL_ROOT / "data" / "angles.json"
DOMAINS = ("concurrency", "state", "contracts", "performance", "testing", "diagnosis",
           "representation", "lifecycle", "control-flow", "integration", "security")
FIELDS = {
    "id", "domain", "title", "signals", "keywords", "mechanism", "experiment",
    "falsifies", "verification", "limits", "references", "evidence_kind",
}
STOPWORDS = frozenset("a an the is are was were to of in on at for and or with from it this that bug error problem issue please fix investigate".split())


def tokens(text):
    return [term for term in re.findall(r"[^\W_]+", text.lower(), re.UNICODE)
            if term not in STOPWORDS]


def validate_references(refs, identity, root):
    if not isinstance(refs, list) or not refs:
        raise ValueError(f"{identity}: references must be a nonempty list")
    for ref in refs:
        if not isinstance(ref, str) or not ref.startswith("references/"):
            raise ValueError(f"{identity}: reference must point into references/")
        target = (root / ref).resolve()
        if not target.is_relative_to((root / "references").resolve()) or not target.is_file():
            raise ValueError(f"{identity}: invalid reference: {ref}")


def validate_catalog(catalog, root=SKILL_ROOT):
    """Reject incomplete records, false evidence labels, and broken resource paths."""
    if not isinstance(catalog, dict) or set(catalog) != {"schema_version", "patterns"}:
        raise ValueError("Catalog must contain schema_version and patterns")
    if type(catalog["schema_version"]) is not int or catalog["schema_version"] != 1:
        raise ValueError("Unsupported catalog schema_version")
    patterns = catalog["patterns"]
    if not isinstance(patterns, list) or not patterns:
        raise ValueError("patterns must be a nonempty list")
    seen = set()
    for row in patterns:
        if not isinstance(row, dict) or set(row) != FIELDS:
            raise ValueError("Each pattern must contain every schema field")
        for key in FIELDS - {"references"}:
            if not isinstance(row[key], str) or not row[key].strip():
                raise ValueError(f"{key} must be a nonempty string")
        identity = row["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identity) or identity in seen:
            raise ValueError(f"Invalid or duplicate pattern id: {identity}")
        seen.add(identity)
        if row["domain"] not in DOMAINS:
            raise ValueError(f"Unknown domain: {row['domain']}")
        if row["evidence_kind"] != "heuristic":
            raise ValueError("Seed patterns must remain heuristic, not verified incidents")
        validate_references(row["references"], identity, root)
    return patterns


def load_catalog(path=CATALOG_PATH):
    with path.open(encoding="utf-8") as stream:
        return validate_catalog(json.load(stream))


def validate_angles(data, root=SKILL_ROOT):
    if not isinstance(data, dict) or set(data) != {"schema_version", "axes"}:
        raise ValueError("Angle data must contain schema_version and axes")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("Unsupported angle schema_version")
    if not isinstance(data["axes"], list) or not data["axes"]:
        raise ValueError("axes must be a nonempty list")
    seen = set()
    covered = set()
    for axis in data["axes"]:
        if not isinstance(axis, dict) or set(axis) != {"id", "domains", "trigger", "question", "observation", "references"}:
            raise ValueError("Each angle must contain all schema fields")
        for key in ("id", "trigger", "question", "observation"):
            if not isinstance(axis[key], str) or not axis[key].strip():
                raise ValueError(f"Angle {key} must be a nonempty string")
        identity = axis["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", identity) or identity in seen:
            raise ValueError(f"Invalid or duplicate angle id: {identity}")
        seen.add(identity)
        domains = axis["domains"]
        if (not isinstance(domains, list) or not domains
                or any(not isinstance(domain, str) or domain not in DOMAINS for domain in domains)):
            raise ValueError(f"{identity}: invalid domains")
        covered.update(domains)
        validate_references(axis["references"], identity, root)
    if set(DOMAINS) - covered:
        raise ValueError("Angle data must route every declared diagnostic domain")
    return data["axes"]


def load_angles(path=ANGLES_PATH):
    with path.open(encoding="utf-8") as stream:
        return validate_angles(json.load(stream))


def search(query, domain=None, limit=3, patterns=None):
    """BM25 lexical ranking over symptoms, not generic experiment boilerplate."""
    query_terms = sorted(set(tokens(query)))
    if not query_terms:
        raise ValueError("Use observable symptom or mechanism terms, not only generic bug words")
    if domain is not None and domain not in DOMAINS:
        raise ValueError(f"Unknown domain: {domain}")
    if type(limit) is not int or not 1 <= limit <= 10:
        raise ValueError("limit must be between 1 and 10")
    rows = load_catalog() if patterns is None else patterns
    # Rank against the whole catalog so filtering does not change term rarity.
    docs = [Counter(tokens(" ".join([row["title"]] * 2 + [row["signals"]] * 2
                                    + [row["keywords"], row["mechanism"]]))) for row in rows]
    lengths = [sum(doc.values()) for doc in docs]
    average = sum(lengths) / len(docs) if docs else 1
    frequencies = Counter(term for doc in docs for term in doc)
    results = []
    for row, doc, length in zip(rows, docs, lengths):
        if domain is not None and row["domain"] != domain:
            continue
        matched = [term for term in query_terms if term in doc]
        if not matched:
            continue
        score = 0.0
        for term in matched:
            rarity = math.log(1 + (len(docs) - frequencies[term] + 0.5) / (frequencies[term] + 0.5))
            frequency = doc[term]
            score += rarity * frequency * 2.5 / (frequency + 1.5 * (0.25 + 0.75 * length / average))
        coverage = len(matched) / len(query_terms)
        match_quality = "weak_match" if len(query_terms) < 2 or coverage <= 0.5 else "matched"
        results.append({**row, "score": round(score, 4), "matched_terms": matched,
                        "query_coverage": round(coverage, 4), "match_quality": match_quality})
    results.sort(key=lambda row: (-row["score"], row["id"]))
    status = "no_match"
    if results:
        # A small overlap is a retrieval lead, not a ready-made hypothesis.
        status = results[0]["match_quality"]
    return {
        "status": status,
        "query": query, "domain": domain or "all", "catalog": "data/patterns.json",
        "ranking": "Lexical relevance only; score and coverage are not causal confidence.",
        "unmatched_terms": [term for term in query_terms if term not in frequencies],
        "results": results[:limit],
    }


def investigation_plan(result):
    """Compose catalog guidance without inventing observations or proven causes."""
    applicable = [row for row in result["results"] if row["match_quality"] == "matched"] if result["status"] == "matched" else []
    plan = {
        **result,
        "mode": "investigation_plan",
        "establish": [
            "Record expected versus actual behavior and an independent correctness oracle.",
            "Identify executing source/build, runtime versions, inputs, and failing versus healthy conditions.",
        ],
        "hypotheses": [{
            "pattern_id": row["id"], "status": "ASSUMED",
            "candidate_mechanism": row["mechanism"], "experiment": row["experiment"],
            "falsifying_observation": row["falsifies"], "verification": row["verification"],
            "limits": row["limits"], "references": row["references"],
        } for row in applicable],
        "next_step": (
            "Inspect the relevant path and choose one experiment that distinguishes applicable hypotheses."
            if applicable else
            "No sufficiently matched candidate. Map the actual failing flow using the exploration angles; do not force a catalog mechanism."
        ),
        "completion": "Report observations, cause confidence, before/after checks, impact, and untested boundaries. A catalog match does not establish the cause.",
    }
    if not applicable:
        plan["exploration"] = exploration_angles(result["domain"])
    return plan


def exploration_angles(domain="all"):
    if domain != "all" and domain not in DOMAINS:
        raise ValueError(f"Unknown domain: {domain}")
    axes = load_angles()
    return {
        "source": "data/angles.json", "status": "questions_only",
        "instruction": "Select angles implicated by the actual path. This list is not exhaustive and no angle is a verified diagnosis.",
        "axes": [axis for axis in axes if domain == "all" or domain in axis["domains"]],
        "sequence": [
            "Establish an independent oracle and preserve the failure signature.",
            "Locate the last-correct and first-incorrect boundary, including prior history.",
            "List relevant assumptions and compare equivalent failing/healthy controls.",
            "Form a mechanism-specific prediction and falsifier even if absent from the catalog.",
            "Run one safe discriminator; retain evidence and rejected/inconclusive outcomes.",
        ],
    }


def exploration_plan(result):
    plan = investigation_plan(result)
    plan["mode"] = "exploration_plan"
    plan["hypotheses"] = []
    plan["exploration"] = exploration_angles(result["domain"])
    plan["next_step"] = "Use actual boundary evidence to select an angle and formulate a new falsifiable mechanism. Catalog results remain optional lexical leads."
    return plan
