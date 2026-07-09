"""Mermaid lineage diagrams for fusion workflows."""

from __future__ import annotations


def build_mermaid_lineage(
    *,
    sources: list[dict[str, str]],
    join_spec: dict[str, str],
    output_name: str,
    anomalies: dict | None = None,
) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for index, source in enumerate(sources):
        node_id = f"S{index}"
        lines.append(f'    {node_id}["{source["name"]}<br/>{source.get("rows", "?")} rows"]')

    left_node = "S0"
    right_node = "S1" if len(sources) > 1 else "S0"
    join_id = "J1"
    out_id = "O1"

    how = join_spec.get("how", "left")
    left_key = join_spec.get("left_key", "")
    right_key = join_spec.get("right_key", "")
    lines.append(f'    {join_id}{{"join {how}<br/>{left_key} = {right_key}"}}')
    lines.append(f'    {out_id}["{output_name}<br/>fused export"]')
    lines.append(f"    {left_node} --> {join_id}")
    if len(sources) > 1:
        lines.append(f"    {right_node} --> {join_id}")
    lines.append(f"    {join_id} --> {out_id}")

    if anomalies:
        orphan_count = len(anomalies.get("orphan_keys", {}).get("orphan_keys_in_right", []))
        if orphan_count:
            lines.append(f'    {join_id} -. "{orphan_count} orphan keys" .-> AN1["anomaly review"]')

    lines.append("```")
    return "\n".join(lines)