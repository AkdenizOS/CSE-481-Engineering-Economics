# Week 1 — BIST 100 and Yahoo Finance

**Next:** [Week 2](02-algorithmic-trading-and-agentic-harness.md)

## Goals
- Understand how BIST stocks are represented as time-series data.
- Download BIST stock prices with Python and Yahoo Finance.
- Read Open, High, Low, Close and Volume (OHLCV) data.
- Explain the logic of support/resistance and pivot points.
- Understand how an MCP-based AI agent can call financial tools.

## Key concepts
- **BIST 100**: benchmark index of major companies on Borsa İstanbul. Yahoo symbols use the `.IS` suffix (`ASELS.IS`, `THYAO.IS`).
- The goal is not to guess prices manually — it is to design **repeatable algorithms**: data → rules → signals → backtest → tools → AI agent.
- **Data sources**: Yahoo Finance (OHLCV, index data), Fintables (financial statements, valuation ratios), TCMB / TÜİK (rates, inflation, FX).
- **OHLCV**: one row = one trading day. Green candle: Close > Open.
- **Support/resistance** is a zone, not one exact price: local highs/lows → pivot points → cluster nearby prices (tolerance ≈ 1.5%) → count reactions → strength score (touches, recent touches, high-volume reactions, reversal size).
- First indicators: SMA, RSI, MACD, volume. Example rule `SMA20 > SMA50 → BUY` — rule-based ≠ guaranteed profit.
- **Backtest** with `Signal.shift(1)` to avoid look-ahead bias; compare against the BIST 100 return.
- Fundamental score from Fintables: revenue growth, ROE, Net Debt/EBITDA, P/E vs sector.
- **MCP agent**: the AI discovers and calls Python tools (`get_stock_history`, `find_support_resistance`, `calculate_indicators`, `run_backtest`, `get_fundamental_metrics`) and explains the result.

## Reading
- [Week 1 slides — BIST 100 Financial Analytics with Python & MCP AI Agents](../resources/2026-2027-fall/week-01-bist-python-mcp.pdf)

## Practice
- [ ] `pip install yfinance pandas matplotlib` in a virtual environment
- [ ] Download `ASELS.IS` from 2024-01-01 and print `df.head()`
- [ ] Detect pivot highs/lows with a 5-day window and group them into zones
- [ ] Backtest `SMA20 > SMA50` with `shift(1)` and compare with buy-and-hold

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
