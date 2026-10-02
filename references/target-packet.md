# Target packet and cheap architecture pass

Load first. Freeze the packet before other lanes run.

## Packet fields

- Requested chain ID and address; observed chain ID from `eth_chainId` on the RPC actually used; observed address.
- Name, symbol, decimals, total supply, `metadata_status`. Unresolved fields stay listed.
- Pin: `block_number`, `block_hash`, UTC timestamp, captured header. Extra chains: extra pins.
- Runtime code hash; proxy kind, implementation, admin/upgrade authority.
- Deployment or launch transaction when available (create tx, factory, salt).
- Candidate pools and related contracts, each with role and provenance.
- User decision question, mode, materiality rules, known limitations.
- Safety: no real signing, no broadcast, fork restrictions if any.

Write `target-integrity.json` using [`schemas/target-integrity.schema.json`](../schemas/target-integrity.schema.json).

Cache key: `{chain_id}:{address}:{block}:{query}`. Reuse identical code hashes instead of re-decoding.

## Architecture pass (cheap)

Enumerate every contract or key that can:

- mint, burn, rebase, or rewrite balances
- restrict, tax, pause, or gate transfers
- remove LP principal or reprice a curve
- upgrade or `delegatecall` out
- collect, split, or redirect fees
- allocate or claim rewards
- enforce advertised utility or redemption

For each: address, chain, role, provenance (`requested | derived-from-runtime | log-decoded | factory-computed | explorer-candidate | user-supplied`), runtime status, and whether it is in scope for this mode.

Explorer-candidate addresses stay candidates until runtime or logs bind them to the target.

## Parallel lanes

If authorized, copy the frozen packet into every lane. Return evidence rows, findings, and unresolved questions — not a report.

Suggested independent lanes (∥):

- A token controls
- B liquidity custody
- C sellability
- D supply / launch
- E fees / treasury / rewards
- F utility / dependencies

Ordered work: triggered deep tracks → after the screening finding that fired them. Formal report → after reconciliation.

Sequential execution uses the same packet and the same row format.

## Query hygiene

Batch independent `eth_call` / storage reads. Do not wait on one lane to start another unless the address is still unknown.

Do not apply monetary materiality thresholds to discovery of mint, upgrade, seizure, transfer restriction, arbitrary-call, or LP-removal authority. Size thresholds may rank *depth* of sellability or holder concentration after those authorities are mapped.
