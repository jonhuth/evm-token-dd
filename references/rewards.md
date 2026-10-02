# G — Rewards, vaults, backing, and redemption

Load for vault, dividend, buyback, backing, redemption, or "is this solvent" questions.

## Separate

| Thing | Not the same as |
|---|---|
| Vault token balance | Available backing for holders |
| Synthetic reward / points / shares | Redeemable underlying |
| Promise / docs / tweet | Enforceable onchain right |
| Unclaimed fees in a pool | Assets in a treasury |

Identify who can claim, the actual asset received, conversion units, fees, timing, caps, approvals, admin dependencies, and the exit route.

## LP-fee origin questions

Reconcile balances and transfers to receipt-level fee collections and forwarding:

- pool / hook / escrow collect
- fee split
- forward to the named vault
- vault opening + inflows − outflows = closing, with unexplained delta bounded

Distinguish vault holdings, pool inventory, and unclaimed fees. A vault that holds synthetic claims without a proven underlying exit is not backing. See [`examples.md`](examples.md).

## Distributions

When material, test conservation, entitlement rules, cumulative caps, duplicate payments, unpaid amounts, retained inventory, and processing liveness.

Do not assume distributed amounts must be less than purchases if prefunding, donations, carryover, or minting exist.

An upgradeable reward layer around an immutable token can still seize economic value. Rate the layers separately.
