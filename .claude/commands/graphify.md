Build or update the Quantum Cube knowledge graph using graphify.

Run this bash command from the project root:

```bash
cd /Users/qnc/Projects/quantumcube && graphify extract . 2>&1
```

Once complete:
1. Read `graphify-out/GRAPH_REPORT.md` and summarise the key findings — god nodes, community structure, surprising connections
2. Report how many nodes and edges were built
3. Note any fragile areas or unexpected dependency clusters

If ANTHROPIC_API_KEY is not set, run the AST-only update instead:
```bash
cd /Users/qnc/Projects/quantumcube && graphify update . 2>&1
```
