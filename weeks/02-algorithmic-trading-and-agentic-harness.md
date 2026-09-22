# Week 2 — Algorithmic Trading and the Agentic Harness

**Previous:** [Week 1](01-bist-100-and-yahoo-finance.md) · **Next:** [Week 3](03-technical-indicators.md)

## Goals
- Explain what a harness is and why an AI agent needs one.
- Describe the project's final output: result + why + risks + human review.

## Key concepts
- **Harness** = the control layer around an AI agent: steps, tool permissions, evidence, risk gates, memory, logging, human review. *The agent decides what seems useful; the harness decides what is allowed next.*
- **Main principle**: LLM reasons and explains · Python tools calculate · harness controls the workflow · backtest verifies · human makes the final decision. The LLM must never estimate RSI, ROE or Net Debt/EBITDA itself.
- Three metaphors: **OS kernel** (agent = process, MCP tools = system calls), **finite state machine** (START → LOAD DATA → CHECK QUALITY → … → HUMAN REVIEW → CLOSE), **CI/CD pipeline** (no strong conclusion if data quality or backtest fails).
- **Final output** is an educational analytical state (e.g. `POTENTIAL_CATCH_UP_CANDIDATE`), never a bare BUY/SELL, with evidence, warnings and an Accept / Modify / Reject human review.
- **MCP**: the agent sees only approved tools, each with a known input/output schema.
- Specialized agents: Orchestrator, Market & Sector, Fundamental & Macro, News & Speech, Strategy & Backtest, Risk & Data Quality. Reasoning agents interpret; deterministic services calculate.

## Reading
- [Week 2 slides — Agentic Harness](../resources/2026-2027-fall/week-02-agentic-harness.pdf)
- [Meta-Harness: End-to-End Optimization of Model Harnesses](../resources/2026-2027-fall/papers/meta-harness-2603.28052.pdf) (Lee et al., arXiv 2603.28052)
- [Code as Agent Harness](../resources/2026-2027-fall/papers/code-as-agent-harness-2605.18747.pdf) (Ning et al., arXiv 2605.18747)
- [Harness-G: A Graph-Structured Harness for Search Agents](../resources/2026-2027-fall/papers/harness-g-2607.27652.pdf) (Hou et al., arXiv 2607.27652)

## Practice
- [ ] Draw the harness state machine from memory
- [ ] For "Is THYAO a catch-up candidate?", list which tool each state calls

## Checklist
- [ ] Lecture attended
- [ ] Slides read
- [ ] Code run
- [ ] Notes written

---

This file is the shared plan — improve it if the course changes, but keep it general.
Personal notes go below, one `## Notes — <Name> (<term>)` section per person.

## Notes — Efe (2026-2027 Fall)

### Lecture
<!-- What was actually covered, and what the lecturer emphasised. -->

### Code
<!-- What you ran, what it printed, what it means. -->

### Questions
<!-- Unclear things. Ask, then answer them here. -->

### Exam-worthy
<!-- Definitions, formulas, pitfalls. -->
