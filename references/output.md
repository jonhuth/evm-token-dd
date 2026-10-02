# Output standard

Load before writing a broad or formal report.

## Lead

Direct, conditional verdict answering the user's actual question.

Examples of bounded language:

- "No current executable removal path found at the pinned block."
- "Sellable at the tested sizes under the quoted state."
- "Unknown because historical state was unavailable."
- "NO-GO under the stated requirement for rug resistance."

Do not issue an unconditional "safe" verdict. Do not imply a favorable review predicts returns. Do not average a critical finding away with unrelated positive checks.

## Ratings

Rate these separately. For broad reports include severity, likelihood, confidence, coverage, and time basis.

- Token controls
- Canonical LP-principal custody
- Side-pool removal risk
- Sellability and exit depth
- Current concentration
- Historical launch integrity
- Admin, treasury, and reward custody
- Reward accounting and liveness
- Utility and redemption rights
- External dependencies
- Development and disclosure

Unknown coverage on one surface cannot be used to pass another.

## Body

1. Main reasons for the verdict
2. Strongest contrary evidence
3. Unresolved questions
4. Specific evidence that would change the conclusion
5. Recommendations that address observed deficiencies only

## Ledger

Every material claim gets a row:

`finding ID | exact proposition | chain | address | pin or tx | artifact/query | decoding basis | evidence type | confidence | alternatives | coverage | stale-if`

Discovery claims also record search universe, block ranges or pagination, inclusion rules, and materiality thresholds.

Write the machine-readable report against [`schemas/report.schema.json`](../schemas/report.schema.json) and validate:

```bash
python3 "$SKILL_HOME/scripts/validate_report.py" --manifest target-integrity.json --report report.json
```

Passing validates internal consistency, not RPC honesty, discovery completeness, or protocol safety.
