#!/usr/bin/env python3
"""Search symptom patterns or print a candidate investigation plan; no writes."""

import argparse
import json
import sys

from core import DOMAINS, exploration_plan, investigation_plan, search
from frameworks import framework_context
from recipe_index import search_recipes


def render(result):
    lines = ["# Bug Solver Pro: " + result.get("mode", "search"),
             f"Query: {result['query']} | Domain: {result['domain']} | Status: {result['status']}",
             result["ranking"]]
    if "establish" in result:
        lines.extend(["\n## Establish context"] + [f"- {item}" for item in result["establish"]])
    if "framework_context" in result:
        context = result["framework_context"]
        lines.extend(["\n## Local framework knowledge: " + context["framework"],
                      context["instruction"],
                      "Resources relative to the skill folder: " + ", ".join(context["resources"].values()),
                      "\n" + context["playbook"]])
        if context["boundary_case"] is not None:
            lines.append("\n" + context["boundary_case"])
    if not result["results"]:
        lines.append("\nNo matching shared-catalog pattern. Check local recipe leads and flow mapping; do not fabricate a catalog result.")
    elif result["status"] == "weak_match":
        lines.append("\nWeak lexical overlap. These leads are not automatically promoted into investigation hypotheses.")
    if result["unmatched_terms"]:
        lines.append(f"Unmatched query terms: {', '.join(result['unmatched_terms'])}")
    for row in result["results"]:
        lines.extend([
            f"\n## {row['id']}: {row['title']} [{row['domain']}; heuristic]",
            f"Matched terms: {', '.join(row['matched_terms'])} | Query coverage: {row['query_coverage']:.0%} | Quality: {row['match_quality']}",
            f"Catalog lead (unverified): {row['mechanism']}",
            f"Experiment: {row['experiment']}", f"Falsifies: {row['falsifies']}",
            f"Verify after fix: {row['verification']}", f"Limits: {row['limits']}",
            f"Read relative to the skill folder: {', '.join(row['references'])}",
        ])
    if "framework_matches" in result:
        matches = result["framework_matches"]
        lines.extend(["\n## Framework recipe leads", matches["instruction"],
                      f"Recipe status: {matches['status']} | Framework scope: {matches['framework']}"])
        for row in matches["results"]:
            lines.extend([f"\n### {row['id']} [{row['framework']}; {row['match_quality']}]",
                          f"Matched terms: {', '.join(row['matched_terms'])}",
                          f"Local source: {row['references'][0]} — {row['heading']}"])
            if row["match_quality"] == "matched" and "framework_context" not in result:
                lines.append(row["content"])
    if "exploration" in result:
        exploration = result["exploration"]
        lines.extend(["\n## Open-world exploration", exploration["instruction"]])
        for axis in exploration["axes"]:
            lines.extend([f"\n### {axis['id']}", f"Relevant when: {axis['trigger']}",
                          f"Question: {axis['question']}", f"Observe: {axis['observation']}"])
        lines.extend(["\nInvestigation sequence:"] + [f"- {step}" for step in exploration["sequence"]])
    if "next_step" in result:
        lines.extend(["\n## Next step", result["next_step"], result["completion"]])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Observable symptom or mechanism; use sanitized keywords")
    parser.add_argument("--domain", choices=DOMAINS, help="Optional strict domain filter")
    parser.add_argument("--framework", help="Include a local framework playbook; independent of catalog ranking")
    parser.add_argument("--max-results", "-n", type=int, choices=range(1, 11), default=3)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--plan", action="store_true", help="Include an investigation plan, not an automatic fix")
    mode.add_argument("--explore", action="store_true", help="Explore boundary questions even for unrecorded mechanisms")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()
    try:
        result = search(args.query, args.domain, args.max_results)
        if args.explore:
            result = exploration_plan(result)
        elif args.plan:
            result = investigation_plan(result)
        if args.framework is not None:
            result["framework_context"] = framework_context(args.framework)
        framework = result.get("framework_context", {}).get("framework")
        result["framework_matches"] = search_recipes(args.query, framework, args.domain, args.max_results)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
