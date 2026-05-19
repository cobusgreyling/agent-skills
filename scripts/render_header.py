#!/usr/bin/env python3
"""Render the repo header image: a cross-link graph of the skills.

Edges are extracted from each skill's `## Related skills` section, which
references peers via `[[name]]`. The result is a directed graph that shows
how the skills compose — the differentiator the README claims.

Output: assets/header.png (wide aspect, designed for top of README).
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
OUT = REPO / "assets" / "header.png"

LINK_RE = re.compile(r"\[\[([a-z0-9-]+)\]\]")
RELATED_RE = re.compile(r"## Related skills(.*?)(?=\n## |\Z)", re.DOTALL)


def extract_edges() -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for skill_dir in sorted(SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8")
        m = RELATED_RE.search(text)
        if not m:
            continue
        for target in LINK_RE.findall(m.group(1)):
            edges.append((skill_dir.name, target))
    return edges


SHORT = {
    "agent-architecture-patterns": "architecture\npatterns",
    "agent-cost-modeling": "cost\nmodeling",
    "agent-evaluation-harness": "evaluation\nharness",
    "agent-observability": "observability",
    "guardrails-and-safety": "guardrails\n& safety",
    "latency-budgeting": "latency\nbudgeting",
    "prompt-caching": "prompt\ncaching",
    "rag-vs-context-engineering": "rag vs\ncontext",
    "tool-use-schema-design": "tool-use\nschema",
}


def short_label(name: str) -> str:
    return SHORT.get(name, name.replace("-", "\n", 1))


def render(edges: list[tuple[str, str]]) -> None:
    G = nx.DiGraph()
    G.add_edges_from(edges)

    # Circular layout — symmetric, no overlap, scales cleanly to a banner.
    pos = nx.circular_layout(G, scale=1.0)

    # Spread the circle slightly to wide-aspect; multiply x by 1.7.
    pos = {n: (x * 1.7, y) for n, (x, y) in pos.items()}

    # Node sizing by total degree (in + out).
    deg = dict(G.degree())
    sizes = [3200 + deg[n] * 280 for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(14, 6.5), dpi=180)
    ax.set_facecolor("#0e1116")
    fig.patch.set_facecolor("#0e1116")

    # Edges: thin, slight curvature, low-contrast colour so nodes dominate.
    nx.draw_networkx_edges(
        G,
        pos,
        ax=ax,
        edge_color="#3b4252",
        width=1.0,
        arrows=True,
        arrowsize=10,
        arrowstyle="-|>",
        connectionstyle="arc3,rad=0.12",
        node_size=sizes,
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        ax=ax,
        node_color="#e6edf3",
        edgecolors="#88c0d0",
        linewidths=1.6,
        node_size=sizes,
    )

    labels = {n: short_label(n) for n in G.nodes()}
    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        ax=ax,
        font_size=7.5,
        font_color="#0e1116",
        font_family="monospace",
        font_weight="bold",
    )

    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.35, 1.35)
    ax.set_axis_off()

    # Title + subtitle, set in the negative space.
    fig.text(
        0.04, 0.90,
        "agent-skills",
        color="#e6edf3",
        fontsize=22,
        fontweight="bold",
        family="monospace",
    )
    fig.text(
        0.04, 0.84,
        "skills that change agent behaviour on the same prompt",
        color="#88c0d0",
        fontsize=11,
        family="monospace",
    )
    fig.text(
        0.04, 0.10,
        f"{len(G.nodes())} skills · {len(G.edges())} cross-links · production-triage briefs",
        color="#6c7a89",
        fontsize=9,
        family="monospace",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight", facecolor=fig.get_facecolor(), pad_inches=0.25)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    edges = extract_edges()
    render(edges)
