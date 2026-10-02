# H — Utility, dependencies, and development

Load for advertised utility, oracles, bridges, audits, or "is this real" questions.

## Utility

Determine whether advertised utility is live, token-linked, and enforceable.

A gated function that never checks the token, or that any address can call, is not token utility. A UI that displays a number is not a redemption right.

## Dependencies

Inspect material external assets, oracles, bridges, APIs, keepers, lending systems, collateral, and redemption dependencies.

For each: what fails if it stalls, who can change it, and whether holders have an enforceable exit without it.

On sequencer-operated L2s (including Robinhood Chain), the sequencer is an external dependency. Note it; do not treat it as a token defect unless the question is chain liveness.

## Development and disclosure

Assess source correspondence, reproducible builds, tests, audit scope, release controls, governance, disclosure accuracy, and actual operating behavior.

Polished marketing, copied templates, and awkward code do not establish safety, fraud, or AI authorship.

If X/Twitter or a website claims a lock, audit, or partnership, corroborate onchain. Load [`x-discourse.md`](x-discourse.md) on Grok or when those claims are in scope.
