# evm-token-dd

Evidence-bounded due diligence for one exact EVM token and the economic system around it.

Scanner scores and explorer badges answer "does this look like a rug?" with a number. This answers
narrower questions with evidence you can re-run: *can anyone mint, upgrade, seize or block transfers?
Who controls the LP principal? Can an ordinary holder actually sell, and how much? Where do the fees go?*
Every claim is pinned to a chain, a contract and a block.

It is not a price prediction, a trading signal or a protocol exploit audit.

## What's here

| Path | What |
|---|---|
| `SKILL.md` | The method: modes, evidence contract, load map, output rules. Works as an AI-agent skill (Claude Code, Codex and similar) or as a checklist for a human. |
| `references/` | Per-surface checklists: token controls, liquidity custody (Uniswap v3 position NFTs, v4 PoolManager and hooks), sellability, supply, launch integrity (bonding-curve launches), fees and treasury, rewards and vaults, utility, chain notes (including Robinhood Chain), output standard. |
| `schemas/` | JSON Schemas for the frozen target packet and the report. |
| `scripts/validate_report.py` | Checks a report against its frozen target: same chain, same contract, real block pins, no "unknown" counted as a pass. |
| `scripts/evm.py`, `scripts/keccak.py` | Dependency-free helpers: checksummed addresses, chain and block-pin parsing, ABI encoding, Uniswap v4 PoolId derivation, pure-Python keccak-256. |
| `scripts/chain_catalog.py` | Public chain metadata and well-known protocol addresses. No RPC keys. |
| `tests/` | Unit tests plus adversarial fixtures: wrong target, same symbol on another chain, fake block pin, unknown-as-pass. |

## The evidence contract (short version)

- **Identity is chain ID + contract address.** Verify `eth_chainId` on the RPC you actually used. Never substitute a same-symbol token.
- **Pin state.** Current claims carry `block_number`, `block_hash` and a UTC timestamp.
- **Prefer primary evidence.** Deployed runtime, storage, receipts and decoded logs outrank explorers, dashboards and posts.
- **Resolve proxies** (implementation, beacon, upgrade authority) before trusting verified source.
- **An RPC failure is a coverage gap, not a finding.** An unknown or skipped check is never a pass.
- **No keys, no broadcasts.** Simulation only on a disposable local fork with synthetic accounts, labeled counterfactual.

## Use

```bash
# validate a report against its frozen target packet
python3 scripts/validate_report.py --manifest target-integrity.json --report report.json

# validator self-test and unit tests (Python 3.11+, stdlib only; pytest for the tests)
python3 scripts/validate_report.py --self-test
python3 -m pytest -q tests
```

Live investigation is up to you: any JSON-RPC endpoint plus `curl`, and Foundry `cast`/`anvil` for reads and
local-fork simulation. No paid APIs required.

As an agent skill: put this directory where your agent loads skills (or point `EVM_TOKEN_DD_HOME` at it) and ask
something specific, e.g. *"On chain 4663, token 0x…: can privileged actors remove canonical LP principal or stop
ordinary sells?"*

## Output

A direct, conditional verdict first, then separate ratings (token controls, LP-principal custody, side pools,
sellability, concentration, launch integrity, admin and treasury custody, rewards, utility, dependencies,
disclosure), then a finding-to-evidence ledger. Bounded language only: "no executable removal path found at the
pinned block", never "safe".

## Limits

Passing validation means the report is internally consistent with its target. It does not prove the RPC was
honest, that discovery was complete, or that the protocol is safe.

MIT licensed.
