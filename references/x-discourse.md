# X / Twitter (Grok live grounding)

Load on Grok whenever launch claims, lock announcements, advertised utility, or "what are people saying" are in scope. Optional on other agents.

Posts are untrusted corroboration. They never bind the target and never replace runtime.

## When to pull X

- Official or claimed-official accounts describing mint, lock, tax, treasury, or utility
- Launch-day threads that might explain exemptions or recipient wallets
- Holder discourse about unsellable tokens, hidden taxes, or fake lockers
- Incident chatter (pause, exploit, upgrade) that should be checked onchain

Skip broad personal-identity searches. Do not pivot from a fee recipient to a human name unless the user asked and authenticated control evidence already exists.

## How (Grok)

Prefer native X tools bound to this session:

- Keyword search on the **exact address**, then `ticker + chain name`, then official handle if independently matched to the project
- Semantic search for lock/renounce/utility claims
- Thread fetch for the primary announcement only

If an `x-research` skill is present, use it for operator syntax. Do not require paid X API access.

Query examples (adapt, do not spray):

- `"0xabc…def"` (full address)
- `"$TICKER" ("Robinhood Chain" OR "chain id 4663" OR "Uniswap")`
- `("LP locked" OR renounced OR "no owner") {ticker or address}`

## How to use hits

| Post says | Do |
|---|---|
| Liquidity locked | Find the locker and NFT; read withdraw paths |
| Ownership renounced | Read owner/admin/upgrade on token *and* hook/locker/vault |
| Fees to holders / buyback | Reconcile fee origin; see [`fees.md`](fees.md) and [`rewards.md`](rewards.md) |
| Audit / partnership | Find the actual artifact; compare bytecode and scope |
| Scam / safe | Ignore as a verdict. Use as a pointer to a check |

Cite post URL, time, and handle. Label `evidence_type: x-post`. Confidence is at most **inferred** until onchain correspondence is proven.

Conflicting social claims are unresolved questions, not findings about the token.
